#!/usr/bin/env bash
# Host Discover paralelistmo 254 tareas en paralelo

for i in $(seq 1 254); do
    ping -c1 -w 1 192.168.91.$i &>/dev/null && echo "[+] La ip 192.168.91.$i esta activa" &
done; wait

echo -e "\n[+] Todas las tareas ya fueron ejecutadas\n"
