import os, time, platform, sys
try:
    from telethon.sync import TelegramClient
    from telethon.tl import types
    from telethon import functions
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
yw  = '\033[01;33m'
rs  = '\033[0m'

def re(text, delay=0.001):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

METODOS = {
    "1":  ("Spam",               types.InputReportReasonSpam,            ""),
    "2":  ("Pornografia",        types.InputReportReasonPornography,      ""),
    "3":  ("Violencia",          types.InputReportReasonViolence,         ""),
    "4":  ("Abuso Infantil",     types.InputReportReasonChildAbuse,       "Este grupo tiene contenido de abuso infantil"),
    "5":  ("Otro",               types.InputReportReasonOther,            None),
    "6":  ("Derechos de Autor",  types.InputReportReasonCopyright,        "Este grupo viola derechos de autor"),
    "7":  ("Falso/Suplantacion", types.InputReportReasonFake,             "Este grupo es falso o suplanta identidad"),
    "8":  ("Geo Irrelevante",    types.InputReportReasonGeoIrrelevant,    "Contenido geo irrelevante"),
    "9":  ("Drogas Ilegales",    types.InputReportReasonIllegalDrugs,     "Este grupo promueve drogas ilegales"),
    "10": ("Datos Personales",   types.InputReportReasonPersonalDetails,  "Este grupo filtra datos personales"),
}

def mostrar_tabla():
    t = PrettyTable([f'{cn}Numero{lrd}', f'{cn}Metodo{lrd}'])
    for km, v in METODOS.items():
        t.add_row([f'{lgn}{km}{lrd}', f'{gn}{v[0]}{lrd}'])
    print(f'{lrd}')
    print(t)

def resolver_peer(client, objetivo):
    """Resuelve el peer de un grupo público, privado o por link de invitación."""
    import re
    # Link privado tipo t.me/+XXXX
    m = re.match(r'(?:https?://)?t\.me/(\+[A-Za-z0-9_-]+)', objetivo)
    if m:
        inv = m.group(1)
        try:
            # Intentar obtenerlo directo
            return client.get_input_entity(objetivo)
        except:
            # Unirse al grupo para obtener el peer
            result = client(functions.messages.ImportChatInviteRequest(inv.lstrip("+")))
            chat   = result.chats[0]
            return client.get_input_entity(chat.id)

    # @username o link público
    entity = client.get_entity(objetivo)
    return client.get_input_entity(entity), entity

def main(cuenta=None):
    if platform.system() == "Windows":
        try:
            from colorama import init; init()
        except: pass

    clear()
    banner = (g + r"""
  _____      __      _   _________     ____    
 (_   _)    /  \    / ) (_   _____)   / __ \   
   | |     / /\ \  / /    ) (___     / /  \ \  
   | |     ) ) ) ) ) )   (   ___)   ( ()  () ) 
   | |    ( ( ( ( ( (     ) (       ( ()  () ) 
  _| |__  / /  \ \/ /    (   )       \ \__/ /  
 /_____( (_/    \__/      \_/         \____/
""" + rs)
    re(banner)

    re(f"\n{k}         Reportador de Grupos\n")
    re(f"{lrd}[{lgn}+{lrd}] {gn}Creado por : {lgn}@DarkZFull{rs}\n\n")

    if cuenta:
        api_id   = int(cuenta["api_id"])
        api_hash = cuenta["api_hash"]
        phone    = cuenta["phone"]
        session  = cuenta["session"]
        nombre   = cuenta["nombre"]
        password = None
        print(f"{lrd}[{lgn}+{lrd}] {gn}Cuenta: {lgn}{nombre} ({phone}){rs}\n")
    else:
        api_id   = int(input(f"{lrd}[{lgn}+{lrd}] {gn}API ID    : {g}").strip())
        api_hash = input(f"{lrd}[{lgn}+{lrd}] {gn}API Hash  : {g}").strip()
        phone    = input(f"{lrd}[{lgn}+{lrd}] {gn}Telefono  : {g}").strip()
        password = input(f"{lrd}[{lgn}+{lrd}] {gn}2FA (enter si no tienes): {g}").strip() or None
        session  = "session_grupo"

    mostrar_tabla()

    method = input(f"\n{lrd}[{lgn}?{lrd}] {gn}Elige metodo : {k}").strip()
    if method not in METODOS:
        print(f"{lrd}[!] Metodo invalido.{rs}"); return

    objetivo = input(f"{lrd}[{lgn}+{lrd}] {gn}@grupo o link : {k}").strip()
    try:
        cantidad = int(input(f"{lrd}[{lgn}+{lrd}] {gn}Cantidad  : {k}").strip())
    except ValueError:
        print(f"{lrd}[!] Cantidad invalida.{rs}"); return

    nombre_m, razon_cls, mensaje_def = METODOS[method]
    if razon_cls == types.InputReportReasonOther:
        mensaje = input(f"{lrd}[{lgn}+{lrd}] {gn}Motivo    : {k}").strip()
    else:
        mensaje = input(f"{lrd}[{lgn}+{lrd}] {gn}Motivo (enter para usar default): {k}").strip()
        if not mensaje:
            mensaje = mensaje_def

    print(f"\n{lrd}[{lgn}+{lrd}] {gn}Conectando...{rs}")

    try:
        with TelegramClient(session, api_id, api_hash) as client:
            client.start(phone, password if not cuenta else None)

            try:
                result = resolver_peer(client, objetivo)
                if isinstance(result, tuple):
                    peer, entity = result
                    nombre_grupo = getattr(entity, 'title', getattr(entity, 'username', objetivo))
                else:
                    peer = result
                    nombre_grupo = objetivo
            except Exception as e:
                print(f"{lrd}[!] No se encontro el grupo: {e}{rs}"); return

            print(f"{lrd}[{lgn}+{lrd}] {gn}Grupo encontrado: {lgn}{nombre_grupo}{rs}")
            print(f"{lrd}[{lgn}+{lrd}] {gn}Iniciando {cantidad} reportes...{rs}\n")

            enviados = errores = 0
            for i in range(cantidad):
                try:
                    client(functions.account.ReportPeerRequest(
                        peer=peer, reason=razon_cls(), message=mensaje))
                    enviados += 1
                    print(f"{lrd}[{lgn}+{lrd}] {gn}Reporte {lgn}{i+1}/{cantidad}{rs}")
                except Exception as e:
                    errores += 1
                    print(f"{lrd}[!] Error {i+1}: {e}{rs}")

    except Exception as e:
        print(f"{lrd}[!] Error de conexion: {e}{rs}"); return

    print(f"\n{k}{'━'*40}")
    print(f"{lrd}[{lgn}✓{lrd}] {gn}Completado — Enviados: {lgn}{enviados} {rd}Errores: {errores}{rs}")
    print(f"{k}{'━'*40}{rs}\n")

if __name__ == "__main__":
    main()
