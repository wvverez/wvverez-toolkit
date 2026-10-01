#!/usr/bin/env python3

import argparse
import subprocess
import re # para las regex
from termcolor import colored
import signal
import sys

def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo del programa\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler) # para cuando se hace Ctrl+C

def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para cambiar la dirección MAC de una interfaz de red")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la interfaz de red")
    parser.add_argument("-m", "--mac", required=True, dest="mac_address", help="Nueva dirección MAC para la interfaz de red")

    return parser.parse_args()

def is_valid_input(interface, mac_address):
    is_valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
    is_valid_mac_address = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$', mac_address) # 00:0c:29:4d:18:eb <- ejemplo de mac

    return is_valid_interface and is_valid_mac_address

def change_mac_address(interface, mac_address):
    if is_valid_input(interface, mac_address):
        subprocess.run(["ifconfig", interface, "down"]) # aquí se evitan inyecciones de comandos
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
        subprocess.run(["ifconfig", interface, "up"])
        print(colored(f"\n[+] la MAC ha sido cambiada exitosamente", 'green'))
    else:
        print(colored("Los datos introducidos no son correctos", 'red'))

def main():
    args = get_arguments()
    change_mac_address(args.interface, args.mac_address)

if __name__ == '__main__':
    main()
