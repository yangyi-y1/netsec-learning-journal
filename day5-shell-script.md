# Day 5：Shell 脚本基础 + 三个实战脚本

> 2026-07-11 | Ubuntu 22.04 VM | jkhsj

## 新学语法

### 命令替换 `$(command)`
```bash
echo "User: $(whoami)"   # 把 whoami 的输出嵌入字符串
```

### 条件判断 `if [ -f file ]; then ... fi`
```bash
if [ -f /etc/passwd ]; then
    echo "文件存在"
fi
```
`-f` 测试文件是否存在，`fi` 是 if 倒写表示结束。

### for 循环
```bash
for i in $(seq 1 5); do
    echo "Host .$i"
done
```
`seq 1 5` 生成 1 到 5，每次循环 `$i` 取一个值。

### 脚本传参 `${1:-默认值}`
```bash
LOGFILE="${1:-/var/log/auth.log}"   # 有参数用参数，没参数用默认
```

### 退出码 `$?`
```bash
ping -c 1 10.0.2.2
echo $?    # 0 = 通了，非 0 = 没通
```

### 后台并发 `&` + `wait`
```bash
time (sleep 2 & sleep 2 & sleep 2 & wait)   # 三个同时跑，总耗时 2 秒
time (sleep 2; sleep 2; sleep 2)             # 串行，总耗时 6 秒
```

### `&&` vs `;`
- `cmd1 && cmd2` — 前一条成功(exit 0)才执行后一条
- `cmd1; cmd2` — 无论成败都继续

### sort 排序规则
```bash
echo -e "10\n2\n1" | sort      # 1, 10, 2（字母序：1 < 2，所以 10 在 2 前）
echo -e "10\n2\n1" | sort -n   # 1, 2, 10（数值序）
echo -e "10\n2\n1" | sort -nr  # 10, 2, 1（数值倒序）
```
必须加 `-n` 才能按数值排，否则 10 排在 2 前面。

---

## 三个实战脚本

### 1. sysinfo.sh — 系统信息采集
- 文件：[scripts/sysinfo.sh](scripts/sysinfo.sh)
- 新学：`$(command)` 命令替换、`awk` 列提取、`xargs` 去空格
- 核心命令：`nproc`（CPU 核数）、`free -h`（内存）、`df -h --total`（磁盘）

### 2. logscan.sh — SSH 爆破 IP 分析
- 文件：[scripts/logscan.sh](scripts/logscan.sh)
- 新学：`$1` 参数、`${1:-默认值}`、`if [ -f ]` 文件检查
- 核心管道：`grep` → `awk` 取 IP → `sort` 排序 → `uniq -c` 统计 → `sort -nr` 倒序排行 → `head -5` Top 5

### 3. pingscan.sh — IP 段存活扫描
- 文件：[scripts/pingscan.sh](scripts/pingscan.sh)
- 新学：`for + seq` 循环、`ping -c 1 -W 1` 单包探测、`$?` 退出码判断、`( ... ) &` 后台并发、`wait` 等待汇总
- 效果：254 个 IP 同时扫描，2 秒出结果（串行要 254 秒）

---

## 踩坑记录

### 坑 1：nano 编辑器不能粘贴
正常。用 `curl` 从宿主机 HTTP 服务器下载文件代替手动输入。

### 坑 2：VM 与主机传文件
VM 用 NAT(10.0.2.15)，主机无法直连 VM。解决方案：Windows 开 `python -m http.server 8888`，VM 用 `curl http://10.0.2.2:8888/file.sh` 反向拉取。

### 坑 3：VM 不支持 UTF-8 中文
脚本用英文标签，避免乱码。

### 坑 4：自己造假日志做测试
`/var/log/auth.log` 没被人攻击过为空，用 `cat > file << 'EOF'` 手动造测试数据。

---

## 面试话术

> "我在 Ubuntu 上搭过运维环境。Shell 写了三个脚本：系统信息采集(sysinfo.sh)、SSH 爆破 IP 分析(logscan.sh)、C 段存活扫描(pingscan.sh)。分析脚本用 grep→awk→sort→uniq 管道链做日志统计，扫描脚本用 for 循环并发 ping 提高效率。核心语法掌握了命令替换、条件判断、循环、退出码判断和后台并发。"

---

## 回顾 Day 1-4 要点

| 命令 | 用途 | 记忆点 |
|------|------|--------|
| `ls -l` | 长格式看权限 | `-l` = long |
| `mkdir -p` | 创建目录+父目录 | `-p` = parents |
| `>`  vs `>>` | 覆盖/追加写文件 | `>` 清空再写，`>>` 追加 |
| `dmesg` | 内核启动日志 | 不用管路径，直接看 |
| `ss -tlnp` | 查看监听端口 | `t`=tcp `l`=listen `n`=数字 `p`=进程 |
| `systemctl status ssh` | 服务状态 | 开关/查状态都用 systemctl |
| `journalctl -u sshd -n 10` | 查服务日志 | 不翻文本文件，直接按服务名查数据库 |
| `ufw status verbose` | 防火墙规则 | 入站默认拒绝，按需开端口 |
| `crontab -l` | 定时任务列表 | `-l` = list |
