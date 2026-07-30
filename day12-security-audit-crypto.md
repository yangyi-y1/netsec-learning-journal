# Day 12 — 安全审计 + 加密基础 + Docker + 简历投递

**日期：** 2026-07-23

---

## 1. 服务器安全审计

### 发现的问题 & 修复
| 问题 | 严重度 | 修复 |
|------|:------:|------|
| PasswordAuthentication yes | 🔴 高危 | `sudo sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config` |
| UFW 未启用 | 🔴 高危 | `sudo ufw allow 22,80,443/tcp && sudo ufw --force enable` |
| fail2ban 未配 | 🟡 中危 | `/etc/fail2ban/jail.local` maxretry=3, bantime=3600 |
| yangyi 不在 adm 组 | 🟢 低危 | `sudo usermod -aG adm yangyi` |

### 日志分析三板斧（面试必考）
```bash
# 统计暴力破解 IP
grep 'Failed password' /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

# 查异常请求 IP 排行榜
grep '404\|400\|405' /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn

# 查正常访问 IP
grep ' 200 ' /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn
```

### 审计发现
- 扫描器 TOP1：`213.209.159.154`（德国，101次请求）
- 家庭公网 IP：`42.48.102.63`（长沙联通）
- 手机流量 IP vs 服务器看到的 IP 不同（CGNAT 运营商级 NAT）
- 无挖矿/无入侵/无成功暴力破解

### IP 定位精度结论
| 场景 | 精度 |
|------|------|
| 家庭宽带 | 城市级（长沙） |
| 手机流量 CGNAT | 城市+运营商级 |
| VPN/VPS | 完全不可信 |
| 免费查 IP：`curl ip-api.com/json/IP` |

---

## 2. Day 12 加密基础

### 产出文件
- `netsec-learning/day12-crypto/aes_demo.py` — AES-256-CBC 对称加解密
- `netsec-learning/day12-crypto/hash_demo.py` — MD5/SHA256 + 加盐哈希

### 面试核心概念
| 概念 | 一句话 |
|------|--------|
| 认证 vs 授权 | 认证=你是谁，授权=你能干嘛 |
| 对称加密 | 同一把钥匙加解密，快，适合大数据（AES） |
| 非对称加密 | 公钥加密私钥解密，安全但慢（RSA） |
| 哈希 | 单向不可逆，SHA256 是密码存储标准 |
| 加盐 | 密码+随机盐再哈希，防彩虹表 |

---

## 3. Docker 部署

```bash
sudo apt install docker.io -y
# Docker Hub 被墙 → 配国内镜像源 /etc/docker/daemon.json
sudo docker run -d -p 8080:80 nginx
sudo ufw deny 8080/tcp  # 验证后关端口
```

现在简历可写：**"了解 Docker 基础操作，有容器化部署经验"**

---

## 4. 网站更新

- 旧页面：写有真实姓名"杨羿"
- 新页面：终端风格 Security Lab，名字已去
- 文件：`/var/www/html/index.html`
- 本地备份：`C:\Users\jkhsj\Desktop\netsec-learning\index.html`

---

## 5. 域名

- `cssman.top` 已购买（阿里云万网，14元/年）
- 状态：clientHold 等待实名认证（身份证丢失，暂无法通过）
- 备选方案：借家人身份证或去 Cloudflare/Namecheap 免实名注册

---

## 6. 简历投递准备

### 简历改动
- 项目经历拆成两个：云服务器安全运维 + Web 安全实验
- 删掉 AI/百炼/PolarDB 鸡肋证书
- 求职意向锁定"安全运维实习生"
- 加 Docker 到技能列表
- 加 GitHub 链接和手机号

### 已投岗位
- 蓝凌软件 运维实习生（深圳，150-160/天）

---

## 7. SSH 防断配置

`C:\Users\jkhsj\.ssh\config`：
```
Host 8.149.243.227
    ServerAliveInterval 60
```

---

## 8. 服务器当前安全状态

| 层 | 状态 |
|----|:--:|
| 阿里云安全组 | 22/80/443 |
| UFW | deny incoming, allow 22/80/443 |
| SSH | 密钥登录（PasswordAuthentication no） |
| fail2ban | sshd jail, 3次失败封1h |
| Docker | nginx 容器运行中，8080 已关 |

---

## 9. CTF 备战

- jailCTF 2026 — 7/25 凌晨 4:00 开赛
- CTFtime 队伍：Hijacking（单人）

---

## 10. 备忘

- 身份证丢失 → 域名实名暂无法通过 → 不影响服务器使用
- 软考报名：8月底（http://gxt.hunan.gov.cn/rkb）
- 下一个学习节点：Day 13 Nmap 扫描 + 信息收集
- BOSS 直聘打招呼话术已备好（豆包版本 2 + 通用版）
