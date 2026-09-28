#!/usr/bin/env python3
# @wvverez
# Calculadora subnetting

import ipaddress

def calcular(ip, mascara, n=None):

    red = ipaddress.IPv4Network(f"{ip}{mascara}", strict=False)

    libres = 32 - red.prefixlen        
    n = n or 2 ** libres               
    if n > 2 ** libres:               
        raise ValueError("[!] Demasiadas subredes")

    nuevo = red.prefixlen + (n - 1).bit_length()   

    resultado = []
    for s in list(red.subnets(new_prefix=nuevo))[:n]:  
        resultado.append({
            "Dirección de red": s.network_address,      
            "Host inicial": s.network_address + 1,      
            "Host final": s.broadcast_address - 1,       
            "Broadcast": s.broadcast_address,           
            "Siguiente": s.broadcast_address + 1,        
        })
    return resultado

def main():
    while True:                                       
        op = input("\n1. Calcular subredes\n2. Salir\n> ")
        if op == "2":                                  
            break
        if op != "1":                                 
            print("[!] Opción no válida")
            continue                                  
        try:
            ip = input("> IP: ")
            mascara = input("> Máscara (CIDR, ej. /24): ")
            n = input("> Nº de subredes (ENTER = todas): ")
            for s in calcular(ip, mascara, int(n) if n else None):  
                for clave, valor in s.items():         
                    print(f"[+] {clave}: {valor}")
                print("-" * 20)                          
        except ValueError as e:                          
            print(f"[!] Error: {e}")

if __name__ == "__main__":   
    main()
