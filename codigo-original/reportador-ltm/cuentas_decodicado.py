import os, json, sys
try:
    from telethon.sync import TelegramClient
    from prettytable import PrettyTable
except ImportError:
    os.system("pip install telethon prettytable -q")
    os.execv(sys.executable, [sys.executable] + sys.argv)

rd  = '\033[00;31m'
gn  = '\033[00;32m'
lgn = '\033[01;32m'
lrd = '\033[01;31m'
cn  = '\033[00;36m'
k   = '\033[90m'
g   = '\033[38;5;130m'
rs  = '\033[0m'

# Guardar sesiones en carpeta permanente
SESSIONS_DIR = os.path.expanduser("~/.ltm_sessions")
CUENTAS_FILE = os.path.expanduser("~/.ltm_cuentas.json")

os.makedirs(SESSIONS_DIR, exist_ok=True)

def cargar_cuentas():
    if not os.path.exists(CUENTAS_FILE): return []
    try: return json.load(open(CUENTAS_FILE))
    except: return []

def guardar_cuentas(cuentas):
    with open(CUENTAS_FILE, "w") as f:
        json.dump(cuentas, f, indent=2)

def mostrar_tabla(cuentas):
    t = PrettyTable([cn + "#" + lrd, cn + "Alias" + lrd, cn + "Nombre" + lrd, cn + "Telefono" + lrd])
    for i, c in enumerate(cuentas, 1):
        t.add_row([lgn + str(i) + lrd, gn + c["alias"] + lrd,
                   gn + c["nombre"] + lrd, k + c["phone"] + lrd])
    print("\n" + lrd)
    print(t)

def agregar_cuenta():
    print("\n" + lrd + "[" + lgn + "+" + lrd + "] " + gn + "Agregar nueva cuenta" + rs + "\n")
    api_id   = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "API ID   : " + g).strip()
    api_hash = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "API Hash : " + g).strip()
    phone    = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Telefono : " + g).strip()
    password = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "2FA (enter si no tienes): " + g).strip() or None
    alias    = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Alias    : " + g).strip()

    # Guardar sesión en carpeta permanente
    session = os.path.join(SESSIONS_DIR, "session_" + alias)

    print("\n" + lrd + "[" + lgn + "+" + lrd + "] " + gn + "Conectando y guardando sesion..." + rs)

    try:
        with TelegramClient(session, int(api_id), api_hash) as client:
            client.start(phone, password)
            me     = client.get_me()
            nombre = "@" + me.username if me.username else me.first_name

        cuentas = cargar_cuentas()
        cuentas = [c for c in cuentas if c["alias"] != alias]
        cuentas.append({
            "alias":    alias,
            "nombre":   nombre,
            "phone":    phone,
            "api_id":   api_id,
            "api_hash": api_hash,
            "session":  session,
        })
        guardar_cuentas(cuentas)
        print(lrd + "[" + lgn + "v" + lrd + "] " + gn + "Cuenta '" + alias + "' (" + nombre + ") guardada permanentemente." + rs + "\n")

    except Exception as e:
        print(lrd + "[!] Error: " + str(e) + rs + "\n")

def eliminar_cuenta():
    cuentas = cargar_cuentas()
    if not cuentas:
        print("\n" + lrd + "[!] No hay cuentas." + rs); return
    mostrar_tabla(cuentas)
    try:
        num = int(input("\n" + lrd + "[" + lgn + "?" + lrd + "] " + gn + "Numero a eliminar : " + k).strip()) - 1
        if num < 0 or num >= len(cuentas): raise ValueError
    except ValueError:
        print(lrd + "[!] Numero invalido." + rs); return

    c  = cuentas.pop(num)
    sf = c["session"] + ".session"
    if os.path.exists(sf): os.remove(sf)
    guardar_cuentas(cuentas)
    print(lrd + "[" + lgn + "v" + lrd + "] " + gn + "Cuenta '" + c["alias"] + "' eliminada." + rs + "\n")

def seleccionar_cuenta():
    cuentas = cargar_cuentas()
    if not cuentas:
        print("\n" + lrd + "[!] No hay cuentas. Ve a 'Gestionar cuentas' para agregar una." + rs + "\n")
        return None
    mostrar_tabla(cuentas)
    try:
        num = int(input("\n" + lrd + "[" + lgn + "?" + lrd + "] " + gn + "Elige cuenta : " + k).strip()) - 1
        if num < 0 or num >= len(cuentas): raise ValueError
        return cuentas[num]
    except ValueError:
        print(lrd + "[!] Numero invalido." + rs); return None

def menu_cuentas():
    while True:
        print("\n" + lrd + ("─" * 40))
        print(lrd + "[" + lgn + "1" + lrd + "] " + gn + "Agregar cuenta")
        print(lrd + "[" + lgn + "2" + lrd + "] " + gn + "Ver cuentas")
        print(lrd + "[" + lgn + "3" + lrd + "] " + gn + "Eliminar cuenta")
        print(lrd + "[" + lgn + "0" + lrd + "] " + rd + "Volver" + rs)
        print(lrd + ("─" * 40))
        op = input("\n" + lrd + "[" + lgn + "?" + lrd + "] " + gn + "Opcion : " + k).strip()
        if   op == "1": agregar_cuenta()
        elif op == "2":
            c = cargar_cuentas()
            if c: mostrar_tabla(c)
            else: print("\n" + lrd + "[!] No hay cuentas." + rs)
        elif op == "3": eliminar_cuenta()
        elif op == "0": break
        else: print(lrd + "[!] Invalido." + rs)
