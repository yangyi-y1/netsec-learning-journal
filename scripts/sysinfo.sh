#!/bin/bash

echo "========== System Info =========="
echo "Hostname: $(hostname)"
echo "User: $(whoami)"
echo ""
echo "--- CPU ---"
echo "Cores: $(nproc)"
echo "Model: $(grep model.name /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)"
echo ""
echo "--- Memory ---"
free -h | head -2
echo ""
echo "--- Disk ---"
df -h --total | grep total
