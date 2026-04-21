import os, sys, json, time, platform, subprocess, hmac, hashlib

def _k_sys():
    _a, _b, _c = "ltm_", "darkz", "full_2026"
    return _a + _b + _c

def _k_hmac():
    _x, _y, _z = "x9f2kLTM_", "dark_hmac_2", "026_zfull"
    return _x + _y + _z

API_URL    = "http://172.233.164.213:8080"
SECRET_KEY = _k_sys()
HMAC_KEY   = _k_hmac()
UID_FILE   = os.path.expanduser("~/.ltm_uid")
AUTH_CACHE = os.path.expanduser("~/.ltm_cache.json")

if sys.gettrace() is not None or "PYCHARM_HOSTED" in os.environ:
    sys.exit(0)

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests

def get_uid():
    if os.path.exists(UID_FILE):
        uid = open(UID_FILE).read().strip()
        if uid: return uid
    import random, string
    info = platform.node() + platform.machine() + platform.system()
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    uid  = hashlib.md5((info + salt).encode()).hexdigest()[:16]
    with open(UID_FILE, "w") as f:
        f.write(uid)
    return uid

def get_ip():
    try: return requests.get("https://api.ipify.org", timeout=5).text.strip()
    except: return "Desconocida"

def get_bateria():
    try:
        p = "/sys/class/power_supply/battery/capacity"
        if os.path.exists(p): return open(p).read().strip() + "%"
        r = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=3)
        if r.returncode == 0:
            d = json.loads(r.stdout)
            return str(d.get("percentage","?")) + "%"
    except: pass
    return "N/A"

def get_device():
    return f"{platform.system()} {platform.machine()} | {platform.node()}"

def cargar_cache():
    if not os.path.exists(AUTH_CACHE): return {}
    try:
        with open(AUTH_CACHE) as f: return json.load(f)
    except: return {}

def guardar_cache(data):
    try:
        with open(AUTH_CACHE, "w") as f:
            json.dump(data, f)
    except: pass

def hacer_payload(uid, extra=None):
    timestamp = str(int(time.time()))
    mensaje   = uid + timestamp + SECRET_KEY
    firma     = hmac.new(HMAC_KEY.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    payload   = {
        "key":       SECRET_KEY,
        "uid":       uid,
        "timestamp": timestamp,
        "firma":     firma,
    }
    if extra: payload.update(extra)
    return payload

def consultar_servidor(uid):
    try:
        r = requests.post(f"{API_URL}/estado_uid", json=hacer_payload(uid), timeout=10)
        return r.json().get("status", "")
    except: return None

def registrar_solicitud(uid):
    try:
        extra = {"ip": get_ip(), "device": get_device(), "bateria": get_bateria()}
        r = requests.post(f"{API_URL}/solicitar", json=hacer_payload(uid, extra), timeout=10)
        return r.json().get("status", "")
    except: return None

def solicitar_aprobacion():
    uid   = get_uid()
    cache = cargar_cache()

    if cache.get(uid) == "aprobado":
        return True

    if cache.get(uid) == "rechazado":
        print("\033[01;31m[x] Acceso denegado permanentemente.\033[0m")
        sys.exit(1)

    print("\033[01;33m[...] Verificando credenciales con el servidor...\033[0m")
    status = consultar_servidor(uid)

    if status == "aprobado":
        cache[uid] = "aprobado"
        guardar_cache(cache)
        print("\033[01;32m[ok] Acceso concedido!\033[0m")
        return True

    if status == "rechazado":
        cache[uid] = "rechazado"
        guardar_cache(cache)
        print("\033[01;31m[x] Acceso denegado.\033[0m")
        sys.exit(1)

    if status == "pendiente":
        print("\033[01;33m[!] Solicitud en revisión. Intenta más tarde.\033[0m")
        sys.exit(0)

    if status is None:
        print("\033[01;31m[x] Error de red. Verifica tu conexión.\033[0m")
        sys.exit(1)

    res = registrar_solicitud(uid)
    if res in ("enviado", "pendiente"):
        print("\033[01;32m[ok] Solicitud de acceso enviada al administrador.\033[0m")
        print(f"\033[01;36m[i] Tu UID: {uid}\033[0m")
        print("\033[01;33m[!] Espera la aprobación para usar el script.\033[0m")
    else:
        print("\033[01;31m[x] El servidor rechazó la solicitud inicial.\033[0m")

    sys.exit(0)
