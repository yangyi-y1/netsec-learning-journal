# Day 1-4 回顾：Linux 基础命令复习 + 第一个 Shell 脚本

> 2026-07-11 | Ubuntu 22.04 VM | jkhsj

## 复习覆盖

快速回顾了之前学过的核心命令：

### Day 1 - 文件系统 & 权限
- `cat -n /etc/passwd | head -3` — 查看文件前 N 行并显示行号
- `/etc/shadow` 普通用户不可读，只有 root 和 shadow 组成员能访问
- `mkdir -p` + `touch {a,b,c}.txt` 花括号批量创建
- `chmod 644` 设置文件权限

**新理解：`&&` vs `|`**
- `&&` — 前一条命令成功(exit 0)才执行后一条，连接两个独立命令
- `|` — 把前一条的输出喂给后一条的输入，数据管道

### Day 2 - 文本处理
- `grep -c` 统计匹配行数
- `awk -F: '{print $1,$7}'` 提取 passwd 指定列
- `find /etc -name "*.conf" -mtime -7` 查找最近修改的配置文件
- `dmesg > file.log` 输出重定向

### Day 3 - 进程管理 & 网络
- `ss -tlnp` 查看监听端口（比 netstat 更快）
- `python3 -m http.server 9999 &` 后台启动简易服务器
- `kill %1` 杀掉后台任务（`%1` 是 job ID）

### Day 4 - systemd / journalctl / UFW

**systemd 是什么？**
Linux 的大管家(PID=1)，负责启动所有系统服务、监督运行状态、收集日志。不是每个程序都有 systemd，只有它自己启动的服务才被它管。

**journalctl 怎么找到日志的？**
传统日志：程序写文本文件 -> 你用 tail 找路径
journalctl：systemd-journald 拦截服务的 stdout/stderr -> 写入二进制数据库 -> journalctl 查询数据库
所以 `journalctl -u ssh` 不需要路径参数，直接在库里按服务名查。

**UFW 防火墙核心概念：**
- `default deny incoming` — 入站全拒绝
- `default allow outgoing` — 出站全放行（你主动连外面不拦）
- `allow 22/tcp` — 但需要单独放行 SSH 让外面能连进来
- `enable` — 让规则生效，之前规则只是定义了但没加载到内核

**容易搞混：incoming vs outgoing**
- incoming = 别人连你（需要开端口）
- outgoing = 你连别人（默认就通）
- 所以 `allow outgoing` 和 `allow 22/tcp` 不矛盾，是两个方向

## 踩坑记录

### 坑 1：nano 里粘贴不生效
`Ctrl+Shift+V` 在 nano 编辑器里不管用，但终端命令行里可以。

### 坑 2：VM 和主机之间传文件
VM 用 NAT 模式(10.0.2.15)，Windows 主机无法直接连 VM。但 VirtualBox 给 VM 留了 `10.0.2.2` 这个网关地址来反连主机。
解决方案：Windows 开 `python -m http.server 8888`，VM 用 `curl http://10.0.2.2:8888/file.sh` 下载。

### 坑 3：VM 不支持中文
脚本里中文输出变成菱形乱码。改成英文标签即可。

## 第一个脚本：sysinfo.sh

```bash
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
```

**知识点：**
- `$(command)` — 命令替换，把命令输出嵌入字符串
- `xargs` — 去掉输出首尾空格
- `model.name` — grep 正则用 `.` 匹配空格，避免引号嵌套问题

## NAT 本质理解

NAT 和防火墙是两层不同的防护：
- NAT：地址翻译，外网不知道你内网 IP（门牌号不对外公布）
- 防火墙：端口控制，已知端口上决定谁可以进（门禁规则）

VM 在两层 NAT 后面(家庭路由器 NAT + VirtualBox NAT)，外网无法主动连接。UFW 全关掉也没用，因为 NAT 遮住了地址。

IPv6 就是终极方案——地址多到不需要 NAT，每台设备都有公网 IP，安全交给防火墙负责。

## 今日收获

理解 `&&` 和 `|` 的本质区别、systemd 的日志收集机制、NAT 和防火墙的配合关系。
