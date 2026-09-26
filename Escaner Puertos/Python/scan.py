#!/usr/bin/env python3
# https://github.com/wvverez
# Contributions: @JVJIXFMCQ=

import os
import re
import signal
import subprocess
import sys

GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"


def salir(sig, frame):
    print(f"\n{GREEN}[+] Saliendo...{RESET}")
    sys.exit(1)


def mostrar_banner():
    banner = r"""
⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀
⠀⢀⣤⣾⣿⣾⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀
⢠⣾⣿⢛⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀
⣾⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⢿⡵
⢸⡇⠀⠀⠉⠛⠛⣿⣿⠛⠛⠉⠀⠀⣿⡇
⢸⣿⣀⠀⢀⣠⣴⡇⠹⣦⣄⡀⠀⣠⣿⡇
⠈⠻⠿⠿⣟⣿⣿⣦⣤⣼⣿⣿⠿⠿⠟⠀
⠀⠀⠀⠀⠸⡿⣿⣿⢿⡿⢿⠇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠁⠈⠁⠀⠀⠀⠀⠀⠀
"""
    print(f"{GREEN}{banner}{RESET}")


def instalar_arp_scan():
    if subprocess.call(["bash", "-c", "command -v arp-scan &>/dev/null"]) != 0:
        print(f"{GREEN}[+] Instalando arp-scan...{RESET}")
        os.system("sudo apt update && sudo apt install -y arp-scan")


def obtener_mac_local(interfaz):
    salida = subprocess.run(
        ["ip", "link", "show", interfaz],
        capture_output=True, text=True
    ).stdout
    coincidencia = re.search(r"ether (\S+)", salida)
    return coincidencia.group(1) if coincidencia else ""


def escanear_red(interfaz, mac_local):
    salida = subprocess.run(
        ["sudo", "arp-scan", "-I", interfaz, "--localnet", "--ignoredups"],
        capture_output=True, text=True
    ).stdout
    resultados = []
    for linea in salida.splitlines():
        if mac_local and mac_local in linea:
            continue
        if re.search(r"00:0c|08:00", linea):
            resultados.append(linea)
    return resultados


def obtener_ttl(ip):
    salida = subprocess.run(
        ["ping", "-c1", "-W1", ip],
        capture_output=True, text=True
    ).stdout
    coincidencia = re.search(r"ttl=(\d+)", salida, re.IGNORECASE)
    return int(coincidencia.group(1)) if coincidencia else None


def escanear_con_nmap(ip):
    print(f"{GREEN}[+] Escaneando {ip}...{RESET}")
    salida = subprocess.run(
        ["sudo", "nmap", "-p-", "--open", "-sS", "-sC", "-sV",
         "--min-rate", "5000", "-n", "-Pn", ip],
        capture_output=True, text=True
    ).stdout
    for linea in salida.splitlines():
        if re.match(r"^\d+/tcp|^PORT", linea):
            print(linea)
    print(f"{GREEN}[+] Escaneo completado{RESET}")


def procesar_host(ip, mac):
    print(f"{GREEN}[+] IP: {RED}{ip}{RESET} {GREEN}| MAC: {RED}{mac}{RESET}")
    ttl = obtener_ttl(ip)
    if ttl is None:
        print(f"{GREEN}[+] TTL no disponible{RESET}\n")
        return
    so = "Linux" if ttl == 64 else "Windows"
    print(f"{GREEN}[+] {ip} -> {so}{RESET}")
    respuesta = input(f"{GREEN}[+] ¿Escanear {ip} con nmap? (y/n): {RESET}")
    if respuesta.lower().startswith("y"):
        escanear_con_nmap(ip)
    print()


def main():
    signal.signal(signal.SIGINT, salir)
    mostrar_banner()
    instalar_arp_scan()

    interfaces = input(f"{GREEN}[+] Interfaces (ej: eth0,ens33): {RESET}")
    lista_ifaces = [i.strip() for i in interfaces.split(",") if i.strip()]

    if not lista_ifaces:
        print(f"{GREEN}[+] Interfaz no válida{RESET}")
        sys.exit(1)

    for interfaz in lista_ifaces:
        print(f"{GREEN}[+] Escaneando {interfaz}{RESET}")
        mac_local = obtener_mac_local(interfaz)
        resultados = escanear_red(interfaz, mac_local)

        if not resultados:
            print(f"{GREEN}[+] Sin resultados en {interfaz}{RESET}")
            continue

        for linea in resultados:
            partes = linea.split()
            if len(partes) >= 2:
                procesar_host(partes[0], partes[1])


if __name__ == "__main__":
    main()
