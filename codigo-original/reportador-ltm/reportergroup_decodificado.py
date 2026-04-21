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

BANNER = g + r"""
  _____      __      _   _________     ____    
 (_   _)    /  \    / ) (_   _____)   / __ \   
   | |     / /\ \  / /    ) (___     / /  \ \  
   | |     ) ) ) ) ) )   (   ___)   ( ()  () ) 
   | |    ( ( ( ( ( (     ) (       ( ()  () ) 
  _| |__  / /  \ \/ /    (   )       \ \__/ /  
 /_____( (_/    \__/      \_/         \____/
""" + rs

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
    "4":  ("Abuso Infantil",     types.InputReportReasonChildAbuse,       "Contenido de abuso infantil"),
    "5":  ("Otro",               types.InputReportReasonOther,            None),
    "6":  ("Derechos de Autor",  types.InputReportReasonCopyright,        "Viola derechos de autor"),
    "7":  ("Falso/Suplantacion", types.InputReportReasonFake,             "Cuenta falsa o suplantacion"),
    "8":  ("Geo Irrelevante",    types.InputReportReasonGeoIrrelevant,    "Contenido geo irrelevante"),
    "9":  ("Drogas Ilegales",    types.InputReportReasonIllegalDrugs,     "Promueve drogas ilegales"),
    "10": ("Datos Personales",   types.InputReportReasonPersonalDetails,  "Filtra datos personales"),
}

TIPO = {"reporter": "Canal", "report": "Cuenta", "reportergroup": "Grupo"}["reportergroup"]

def mostrar_tabla():
    t = PrettyTable([cn + "Numero" + lrd, cn + "Metodo" + lrd])
    for km, v in METODOS.items():
        t.add_row([lgn + km + lrd, gn + v[0] + lrd])
    print(lrd)
    print(t)

def resolver_peer(client, objetivo):
    import re as _re
    m = _re.match(r'(?:https?://)?t\.me/(\+[A-Za-z0-9_-]+)', objetivo)
    if m:
        inv = m.group(1)
        try:
            return client.get_input_entity(objetivo), None
        except:
            result = client(functions.messages.ImportChatInviteRequest(inv.lstrip("+")))
            chat   = result.chats[0]
            return client.get_input_entity(chat.id), chat
    entity = client.get_entity(objetivo)
    return client.get_input_entity(entity), entity

def main(cuenta=None):
    if platform.system() == "Windows":
        try:
            from colorama import init; init()
        except: pass

    clear()
    re(BANNER)
    re("\n" + k + "         Reportador de " + TIPO + "s\n")
    re(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Creado por : " + lgn + "@DarkZFull" + rs + "\n\n")

    if cuenta:
        api_id   = int(cuenta["api_id"])
        api_hash = cuenta["api_hash"]
        phone    = cuenta["phone"]
        session  = cuenta["session"]
        password = None
        print(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Cuenta: " + lgn + cuenta["nombre"] + " (" + phone + ")" + rs + "\n")
    else:
        api_id   = int(input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "API ID   : " + g).strip())
        api_hash = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "API Hash : " + g).strip()
        phone    = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Telefono : " + g).strip()
        password = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "2FA (enter si no tienes): " + g).strip() or None
        session  = "session_reportergroup"

    mostrar_tabla()

    method = input("\n" + lrd + "[" + lgn + "?" + lrd + "] " + gn + "Elige metodo : " + k).strip()
    if method not in METODOS:
        print(lrd + "[!] Metodo invalido." + rs); return

    objetivo = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "@objetivo o link : " + k).strip()
    try:
        cantidad = int(input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Cantidad : " + k).strip())
    except ValueError:
        print(lrd + "[!] Cantidad invalida." + rs); return

    nombre_m, razon_cls, mensaje_def = METODOS[method]
    motivo = input(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Motivo (enter para default): " + k).strip()
    if not motivo:
        motivo = mensaje_def or ""

    print("\n" + lrd + "[" + lgn + "+" + lrd + "] " + gn + "Conectando..." + rs)

    try:
        with TelegramClient(session, api_id, api_hash) as client:
            client.start(phone, password if not cuenta else None)

            try:
                peer, entity = resolver_peer(client, objetivo)
                nombre_obj   = getattr(entity, 'title', None) or getattr(entity, 'username', objetivo) if entity else objetivo
            except Exception as e:
                print(lrd + "[!] No se encontro el objetivo: " + str(e) + rs); return

            print(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Objetivo: " + lgn + str(nombre_obj) + rs)
            print(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Iniciando " + str(cantidad) + " reportes..." + rs + "\n")

            enviados = errores = 0
            for i in range(cantidad):
                try:
                    client(functions.account.ReportPeerRequest(
                        peer=peer, reason=razon_cls(), message=motivo))
                    enviados += 1
                    print(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Reporte " + lgn + str(i+1) + "/" + str(cantidad) + rs)
                except Exception as e:
                    errores += 1
                    print(lrd + "[!] Error " + str(i+1) + ": " + str(e) + rs)

    except Exception as e:
        print(lrd + "[!] Error de conexion: " + str(e) + rs); return

    print("\n" + k + ("─" * 40))
    print(lrd + "[" + lgn + "v" + lrd + "] " + gn + "Completado - Enviados: " + lgn + str(enviados) + " " + rd + "Errores: " + str(errores) + rs)
    print(k + ("─" * 40) + rs + "\n")

if __name__ == "__main__":
    main()
