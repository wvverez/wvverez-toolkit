#!/usr/bin/env python3
# Script para seleccionar, descargar y desplegar una máquina aleatoria de la plataforma Dockerlabs
# Author: @wvverez

import requests
import random
import os
import sys
import subprocess
import zipfile
import glob
import unicodedata

# los colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"



def verificar_sudo():
    try:
        subprocess.run(['sudo', '-v'], check=True, capture_output=True)
        return True
    except:
        return False



def normalizar_texto(texto):
    # Eliminar tildes y convertir a minúsculas para comparación
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto.lower()




def obtener_dificultades_unicas(data):
    # Diccionario para mapear variantes a una versión canónica
    mapa_dificultades = {}



    for maquina in data['info_maquinas']:
        dificultad_original = maquina['dificultad']
        dificultad_normalizada = normalizar_texto(dificultad_original)

        # Si ya existe una versión canónica, mantenerla
        if dificultad_normalizada not in mapa_dificultades:
            mapa_dificultades[dificultad_normalizada] = dificultad_original
        else:
            # Si ya existe, mantener la que tenga mejor formato (con tilde si es posible)
            # Priorizar la que tenga tilde o mayúsculas
            if 'á' in dificultad_original or 'é' in dificultad_original or 'í' in dificultad_original or 'ó' in dificultad_original or 'ú' in dificultad_original:
                mapa_dificultades[dificultad_normalizada] = dificultad_original


    # Ordenar las dificultades únicas
    dificultades_unicas = sorted(mapa_dificultades.values(), key=lambda x: normalizar_texto(x))
    return dificultades_unicas




def mostrar_dificultades(dificultades):
    print(f"{AMARILLO}Dificultades disponibles:{RESET}")
    for i, dificultad in enumerate(dificultades, 1):
        print(f"  {i}. {dificultad}")




def seleccionar_dificultad(dificultades):
    while True:
        try:
            print(f"\n{VERDE}[+] ¿Quieres filtrar por dificultad? (s/n): {RESET}", end="")

            filtrar = input().lower()

            if filtrar == 'n':
                return None
            elif filtrar == 's':
                mostrar_dificultades(dificultades)
                print(f"{VERDE}[+] Selecciona el número de la dificultad: {RESET}", end="")
                seleccion = input().strip()

                try:
                    seleccion_num = int(seleccion)
                    if 1 <= seleccion_num <= len(dificultades):
                        return dificultades[seleccion_num - 1]
                    else:
                        print(f"{ROJO}[+] Número inválido. Intenta de nuevo.{RESET}")
                except ValueError:
                    print(f"{ROJO}[+] Por favor, ingresa un número válido.{RESET}")
            else:
                print(f"{ROJO}[+] Responde 's' o 'n'.{RESET}")
        except KeyboardInterrupt:
            print(f"\n{ROJO}[+] Cancelado{RESET}")
            sys.exit(1)



def main():
    print(f"{AZUL}" + r'''
         .         .
       ":"
     ___:____     |"\/"|
   ,'        `.    \  /
   |  O        \___/  |
 ~^~^~^~^~^~^~^~^~^~^~^~^~
    ''' + f"{RESET}")

    if not verificar_sudo():
        print(f"{ROJO}[+] Usar: sudo python3 ruletadockerlabs.py{RESET}")
        sys.exit(1)

    try:
        data = requests.get('https://dockerlabs.es/api').json()

        # Obtengo dificultades únicas (agrupando variantes)
        dificultades = obtener_dificultades_unicas(data)
        dificultad_seleccionada = seleccionar_dificultad(dificultades)

        # Filtro máquinas según dificultad seleccionada
        if dificultad_seleccionada:
            # Filtrar comparando normalizado
            dificultad_normalizada = normalizar_texto(dificultad_seleccionada)
            maquinas_filtradas = [m for m in data['info_maquinas'] if normalizar_texto(m['dificultad']) == dificultad_normalizada]
            if not maquinas_filtradas:
                print(f"{ROJO}[+] No hay máquinas con la dificultad seleccionada.{RESET}")
                sys.exit(1)
            print(f"{VERDE}[+] Mostrando máquinas con dificultad: {dificultad_seleccionada}{RESET}")
        else:
            maquinas_filtradas = data['info_maquinas']
            print(f"{VERDE}[+] Mostrando todas las máquinas disponibles{RESET}")

        # Seleccionamos máquina aleatoria
        m = random.choice(maquinas_filtradas)

        # Info de cada máquina más relevante
        print(f"\n{AMARILLO}[+] Nombre: {m['nombre']}{RESET}")
        print(f"{AMARILLO}[+] Creador: {m['autor']}{RESET}")
        print(f"{AMARILLO}[+] Dificultad: {m['dificultad']}{RESET}")
        print(f"{AMARILLO}[+] Descripcion: {m['descripcion'][:60]}...{RESET}")

        if input(f"\n{VERDE}[+] Descargar? (s/n): {RESET}").lower() == 's':
            zip_file = f"{m['nombre']}.zip"
            print(f"{VERDE}[+] Descargando {zip_file}...{RESET}")

            r = requests.get(m['link_descarga'], stream=True, timeout=30)
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0

            with open(zip_file, 'wb') as f:
                for chunk in r.iter_content(8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            print(f"\r{VERDE}[+] {downloaded/total*100:.1f}%{RESET}", end="", flush=True)

            if input(f"{VERDE}\n[+] Desplegar? (s/n): {RESET}").lower() == 's':
                with zipfile.ZipFile(zip_file, 'r') as z:
                    z.extractall('.')

                tar_files = glob.glob('*.tar')
                if tar_files and os.path.exists('auto_deploy.sh'):
                    subprocess.run(['sudo', 'bash', 'auto_deploy.sh', tar_files[0]])
                    print(f"{VERDE}[+] Entorno ya desplegado{RESET}")
                else:
                    print(f"{ROJO}[+] Error: auto_deploy.sh o .tar no los encuentra{RESET}")

    except PermissionError:
        print(f"{ROJO}[+] Ejecutar con sudo plz: sudo python3 {sys.argv[0]}{RESET}")
    except KeyboardInterrupt:
        print(f"{ROJO}[+] Cancelado{RESET}")
    except Exception as e:
        print(f"{ROJO}[+] Error: {e}{RESET}")

if __name__ == "__main__":
    main()
