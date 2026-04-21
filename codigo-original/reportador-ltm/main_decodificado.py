import os, time, platform, sys

# ── Auth ───────────────────────────────────────────────────────
try:
    from auth import solicitar_aprobacion
    solicitar_aprobacion()
except SystemExit:
    sys.exit(1)
except Exception as e:
    print("\033[01;31m[!] Error en auth: " + str(e) + "\033[0m")
    sys.exit(1)

try:
    from prettytable import PrettyTable
    from cuentas import seleccionar_cuenta, menu_cuentas
    from reporter import main as reportar_canal
    from report import main as reportar_cuenta
    from reportergroup import main as reportar_grupo
except ImportError as e:
    os.system("pip install prettytable telethon requests -q")
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

if platform.system() == "Windows":
    try:
        from colorama import init; init()
    except:
        pass

clear()

BANNER = g + r"""
  _____      __      _   _________     ____    
 (_   _)    /  \    / ) (_   _____)   / __ \   
   | |     / /\ \  / /    ) (___     / /  \ \  
   | |     ) ) ) ) ) )   (   ___)   ( ()  () ) 
   | |    ( ( ( ( ( (     ) (       ( ()  () ) 
  _| |__  / /  \ \/ /    (   )       \ \__/ /  
 /_____( (_/    \__/      \_/         \____/
""" + rs

re(BANNER)
re("\n" + k + "         Reportador de Telegram\n")
re(lrd + "[" + lgn + "+" + lrd + "] " + gn + "Creado por : " + lgn + "@DarkZFull" + rs + "\n")
re(yw + "Advertencia: Todo esta bajo tu responsabilidad" + rs + "\n\n")

while True:
    t = PrettyTable([cn + "Numero" + lrd, cn + "Opcion" + lrd])
    t.add_row([lgn + "1" + lrd, gn + "Reportar Canal"   + lrd])
    t.add_row([lgn + "2" + lrd, gn + "Reportar Cuenta"  + lrd])
    t.add_row([lgn + "3" + lrd, gn + "Reportar Grupo"   + lrd])
    t.add_row([lgn + "4" + lrd, gn + "Gestionar cuentas"+ lrd])
    t.add_row([lgn + "0" + lrd, rd + "Salir"            + lrd])
    print(lrd)
    print(t)

    opcion = input("\n" + lrd + "[" + lgn + "?" + lrd + "] " + gn + "Opcion : " + cn).strip()

    if opcion in ("1", "2", "3"):
        cuenta = seleccionar_cuenta()
        if not cuenta:
            continue
        if opcion == "1":
            reportar_canal(cuenta=cuenta)
        elif opcion == "2":
            reportar_cuenta(cuenta=cuenta)
        elif opcion == "3":
            reportar_grupo(cuenta=cuenta)

    elif opcion == "4":
        menu_cuentas()

    elif opcion == "0":
        print("\n" + k + "Hasta luego - @DarkZFull" + rs + "\n")
        break

    else:
        print("\n" + lrd + "[!] Opcion invalida." + rs)
