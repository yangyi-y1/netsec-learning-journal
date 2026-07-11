#!/bin/bash
# ============================================
# pingscan.sh - IP ???????
# Day 5 Shell ???? #3
# ??????? C ? (x.x.x.1-254)???????
# ???./pingscan.sh 192.168.1
# ============================================

if [ -z "$1" ]; then
    echo "Usage: $0 <first 3 octets>"
    echo "Example: $0 192.168.1"
    exit 1
fi

PREFIX="$1"

echo "========== Scanning $PREFIX.0/24 =========="
echo "Online hosts:"
echo ""

for i in $(seq 1 254); do
    (
        ping -c 1 -W 1 "$PREFIX.$i" &>/dev/null
        if [ $? -eq 0 ]; then
            echo "$PREFIX.$i  [UP]"
        fi
    ) &
done

wait

echo ""
echo "Scan complete."
