import os
import sys
import json
import time
import random
import platform
from telethon.sync import TelegramClient
from telethon.tl import types
from telethon import functions
from prettytable import PrettyTable

# --- CONFIGURACIÓN DE RUTAS ---
SESSIONS_DIR = os.path.expanduser("~/.ltm_sessions")
CUENTAS_FILE = os.path.expanduser("~/.ltm_cuentas.json")
os.makedirs(SESSIONS_DIR, exist_ok=True)

# --- COLORES ---
rd, gn, lgn, lrd, cn, k, g, yw, rs = (
    '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;31m',
    '\033[00;36m', '\033[90m', '\033[38;5;130m', '\033[01;33m', '\033[0m'
)

BANNER = g + r"""
  _____      __      _   _________     ____    
 (_   _)    /  \    / ) (_   _____)   / __ \   
   | |     / /\ \  / /    ) (___     / /  \ \  
   | |     ) ) ) ) ) )   (   ___)   ( ()  () ) 
   | |    ( ( ( ( ( (     ) (       ( ()  () ) 
  _| |__  / /  \ \/ /    (   )       \ \__/ /  
 /_____( (_/    \__/      \_/         \____/
""" + rs + f"\n{k}      [ Versión Limpia - Sin Rastreadores ]\n"

# --- LÓGICA DE REPORTES ---
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

# --- FUNCIONES DE APOYO ---
def clear(): os.system("cls" if platform.system() == "Windows" else "clear")

def cargar_cuentas():
    if not os.path.exists(CUENTAS_FILE): return []
    try: return json.load(open(CUENTAS_FILE))
    except: return []

def guardar_cuentas(cuentas):
    with open(CUENTAS_FILE, "w") as f: json.dump(cuentas, f, indent=2)

def resolver_peer(client, objetivo):
    import re as _re
    m = _re.match(r'(?:https?://)?t\.me/(\+[A-Za-z0-9_-]+)', objetivo)
    if m:
        inv = m.group(1)
        try: return client.get_input_entity(objetivo), None
        except:
            result = client(functions.messages.ImportChatInviteRequest(inv.lstrip("+")))
            chat = result.chats[0]
            return client.get_input_entity(chat.id), chat
    entity = client.get_entity(objetivo)
    return client.get_input_entity(entity), entity

# --- MÓDULOS DEL SISTEMA ---
def gestionar_cuentas():
    while True:
        clear(); print(BANNER)
        cuentas = cargar_cuentas()
        t = PrettyTable([cn+"#", cn+"Alias", cn+"Nombre", cn+"Telefono"])
        for i, c in enumerate(cuentas, 1):
            t.add_row([lgn+str(i), gn+c["alias"], gn+c["nombre"], k+c["phone"]])
        print(t)
        print(f"\n{lgn}1. Agregar | {lrd}2. Eliminar | {yw}0. Volver")
        op = input(f"\n{lrd}[?]{gn} Opcion: {rs}").strip()
        
        if op == "1":
            api_id = input(f"{gn}API ID: {rs}"); api_hash = input(f"{gn}API Hash: {rs}")
            phone = input(f"{gn}Telefono: {rs}"); alias = input(f"{gn}Alias: {rs}")
            session = os.path.join(SESSIONS_DIR, "session_" + alias)
            try:
                with TelegramClient(session, int(api_id), api_hash) as client:
                    client.start(phone)
                    me = client.get_me()
                    nombre = "@" + me.username if me.username else me.first_name
                cuentas.append({"alias": alias, "nombre": nombre, "phone": phone, "api_id": api_id, "api_hash": api_hash, "session": session})
                guardar_cuentas(cuentas); print(f"{lgn}✔ Cuenta guardada!")
            except Exception as e: print(f"{lrd}Error: {e}")
            time.sleep(2)
        elif op == "2":
            idx = int(input(f"{lrd}Numero a eliminar: {rs}")) - 1
            if 0 <= idx < len(cuentas):
                c = cuentas.pop(idx)
                if os.path.exists(c["session"]+".session"): os.remove(c["session"]+".session")
                guardar_cuentas(cuentas); print(f"{lgn}✔ Eliminada")
            time.sleep(1)
        elif op == "0": break

def iniciar_reporte(tipo_txt):
    clear(); print(BANNER)
    cuentas = cargar_cuentas()
    if not cuentas: print(f"{lrd}No hay cuentas registradas."); time.sleep(2); return
    
    # Seleccionar Cuenta
    for i, c in enumerate(cuentas, 1): print(f"{lgn}{i}. {gn}{c['alias']} ({c['nombre']})")
    acc_idx = int(input(f"\n{lrd}[?]{gn} Selecciona cuenta: {rs}")) - 1
    acc = cuentas[acc_idx]

    # Seleccionar Método
    t = PrettyTable([cn+"#", cn+"Metodo"])
    for km, v in METODOS.items(): t.add_row([lgn+km, gn+v[0]])
    print(t)
    method = input(f"\n{lrd}[?]{gn} Elige metodo: {rs}").strip()
    
    objetivo = input(f"{lrd}[+]{gn} @objetivo o link: {rs}").strip()
    cantidad = int(input(f"{lrd}[+]{gn} Cantidad de reportes: {rs}"))
    
    nombre_m, razon_cls, mensaje_def = METODOS[method]
    motivo = input(f"{lrd}[+]{gn} Motivo (Enter para default): {rs}").strip() or (mensaje_def or "")

    try:
        with TelegramClient(acc["session"], int(acc["api_id"]), acc["api_hash"]) as client:
            peer, entity = resolver_peer(client, objetivo)
            print(f"\n{lgn}Iniciando reportes sobre {objetivo}...")
            
            enviados = 0
            for i in range(cantidad):
                try:
                    client(functions.account.ReportPeerRequest(peer=peer, reason=razon_cls(), message=motivo))
                    enviados += 1
                    # --- DELAY INTELIGENTE AGREGADO ---
                    wait = random.uniform(3, 7) 
                    print(f"{lrd}[{enviados}]{gn} Reporte enviado. {k}Esperando {wait:.1f}s...")
                    time.sleep(wait)
                except Exception as e:
                    print(f"{lrd}[!] Error: {e}")
                    if "flood" in str(e).lower(): break
            print(f"\n{lgn}✔ Proceso finalizado. Total: {enviados}")
            time.sleep(3)
    except Exception as e: print(f"{lrd}Error de conexión: {e}"); time.sleep(2)

# --- MENÚ PRINCIPAL ---
if __name__ == "__main__":
    while True:
        clear(); print(BANNER)
        print(f"{lrd}[{lgn}1{lrd}] {gn}Reportar Canal")
        print(f"{lrd}[{lgn}2{lrd}] {gn}Reportar Cuenta")
        print(f"{lrd}[{lgn}3{lrd}] {gn}Reportar Grupo")
        print(f"{lrd}[{lgn}4{lrd}] {gn}Gestionar Cuentas")
        print(f"{lrd}[{lgn}0{lrd}] {rd}Salir")
        
        op = input(f"\n{lrd}[?]{gn} Opcion: {cn}").strip()
        if op == "1": iniciar_reporte("Canal")
        elif op == "2": iniciar_reporte("Cuenta")
        elif op == "3": iniciar_reporte("Grupo")
        elif op == "4": gestionar_cuentas()
        elif op == "0": print(f"{k}Hasta luego."); break
