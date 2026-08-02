#!/bin/bash

TARGET="${1:-0.0.0.0}"

echo "========== 端口监听 =========="
ss -tlnp 2>/dev/null | awk -v ip="$TARGET" '$4 ~ ip || NR==1 {print}'

echo ""
echo "========== 进程Top5 CPU =========="
ps aux --sort=-%cpu | head -6
