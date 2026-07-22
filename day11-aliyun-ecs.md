# Day 11: 阿里云 ECS 搭建 + 全流程安全加固 (2026-07-22)

## 服务器配置

- 公网 IP: **8.149.243.227**
- OS: Ubuntu 22.04 LTS (5.15.0-181-generic)
- 实例: 阿里云 ECS, `iZbp1je0h7gjb4kfydp2muZ`
- 磁盘: 40GB | 内存: 1.6GB | CPU: 1 核

## 一、系统初始化

```bash
apt update && apt upgrade -y
```

## 二、创建普通用户 + SSH 密钥登录

### 1. 创建用户

```bash
useradd -m -s /bin/bash yangyi
passwd yangyi
usermod -aG sudo yangyi
```

### 2. 生成密钥对（Windows PowerShell）

```bash
ssh-keygen -t ed25519 -C "yangyi-aliyun"
```

- ED25519: 公钥和私钥都是 256 位
- `-C` 是注释标签，不是密钥内容
- 一路回车，不设 passphrase

### 3. 部署公钥到服务器

```bash
mkdir -p /home/yangyi/.ssh
echo "ssh-ed25519 AAAAC3N... yangyi-aliyun" > /home/yangyi/.ssh/authorized_keys
chmod 700 /home/yangyi/.ssh
chmod 600 /home/yangyi/.ssh/authorized_keys
chown -R yangyi:yangyi /home/yangyi/.ssh
```

### 4. 验证密钥登录

```bash
ssh yangyi@8.149.243.227
# 不需要密码，私钥自动匹配 → 直接进
```

## 三、SSH 安全加固

修改 `/etc/ssh/sshd_config`，两项核心改动：

```bash
PasswordAuthentication no   # 关闭密码登录，只用密钥
PermitRootLogin no          # 禁止 root 远程登录
```

用 sed 一键改：

```bash
sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
```

> sed -i = 直接修改文件（in-place）
> 每条做两次：注释版(`^#`) + 非注释版，保证无论原来什么状态都改成 no
> `systemctl restart sshd` 不会断开已连接的 SSH 会话

## 四、两层防火墙

### 第一层：阿里云安全组（云控制台）

```
互联网 → 安全组 → 服务器
```

- 删掉 RDP 3389 规则（Linux 不用远程桌面）
- 添加 80 (HTTP)、443 (HTTPS) 入方向规则
- 授权对象: 0.0.0.0/0（全网）
- 优先级: 数字越小越优先

### 第二层：UFW（服务器内）

```bash
sudo ufw default deny incoming    # 入站全拒绝
sudo ufw default allow outgoing   # 出站全放行
sudo ufw allow 22/tcp             # SSH
sudo ufw allow 80/tcp             # HTTP
sudo ufw allow 443/tcp            # HTTPS
sudo ufw enable
```

概念对照：

| 层级 | 控制台 | 所在位置 | 配置方式 |
|------|--------|----------|----------|
| 第 1 层 | 安全组 | 阿里云控制台网页 | 图形界面 |
| 第 2 层 | UFW | 服务器本机 | 命令行 |

两层都得放行端口，流量才能到达服务。

## 五、fail2ban 防暴力破解

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban --now
```

- 监控 `/var/log/auth.log`
- 连续多次 SSH 登录失败 → 自动封 IP
- 和改 SSH 端口、禁密码登录形成三层防护

## 六、Nginx + MySQL (LEMP)

### Nginx

```bash
sudo apt install nginx -y
sudo systemctl enable nginx --now
```

- 访问 `http://8.149.243.227` 能看到欢迎页即成功
- systemctl = 服务遥控器，管启动/停止/开机自启/重新加载

### MySQL

```bash
sudo apt install mysql-server -y
sudo mysql_secure_installation
```

安全硬化四步（全选 Y）：

1. 删匿名用户 — 防止未认证连接
2. 禁 root 远程登录 — root 只能本地连
3. 删测试库 — 去掉自带的 test 数据库
4. 刷新权限表 — 改动立即生效

> MySQL root 不是系统 root，是两个独立的用户体系
> MySQL 8.0 默认 `auth_socket` 插件：系统 root 本地进 MySQL 免密，比密码更安全

## 七、部署自定义着陆页

替换 Nginx 默认页：

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>杨羿的云服务器</title>
...（含服务状态展示 + GitHub 跳转按钮）
```

- 纯静态 HTML，无需后端、无需数据库
- 任何人访问看到的都一样（无登录/账户概念）
- GitHub 按钮是真实超链接，非缓存/复制

## 八、最终状态

| 项 | 状态 |
|------|------|
| sudo apt update + upgrade | ✅ |
| 用户 yangyi (sudo 组) | ✅ |
| SSH 密钥登录 (ED25519) | ✅ |
| 禁 root 远程登录 | ✅ |
| 禁密码登录 | ✅ |
| fail2ban | ✅ |
| 安全组 22/80/443 | ✅ |
| UFW 22/80/443 | ✅ |
| Nginx | ✅ |
| MySQL 安全硬化 | ✅ |
| 自定义着陆页 | ✅ |
| 手机浏览器可访问 | ✅ |

## 核心概念速记

- **安全组 vs UFW**: 安全组在云控制台（第一道），UFW 在服务器里（第二道），两层都得通
- **ssh 客户端 vs sshd 服务端**: ssh 是你连别人，sshd 是别人连你，d = daemon
- **systemctl**: Linux 服务遥控器，`enable`=开机自启, `start`=立刻启动, `enable --now`=两步一起
- **mysql_secure_installation**: MySQL 出厂安全漏洞修复脚本，不是"安装 MySQL"
- **ED25519**: 256 位现代加密算法，公钥私钥位数相同，比 RSA 更快更短
