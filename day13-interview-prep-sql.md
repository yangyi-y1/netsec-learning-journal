# Day 13 — 面试突击 + MySQL 实操 + jailCTF 备战

**日期：** 2026-07-24

---

## 1. 面试知识扫盲

### TCP 三次握手
```
客户端 SYN → 服务器 SYN+ACK → 客户端 ACK
```
为什么三次：确认双方收发都正常；防历史重复 SYN 造成半开连接浪费。

### TCP 四次挥手
```
客户端 FIN → 服务器 ACK → 服务器 FIN → 客户端 ACK → 等 2MSL
```
为什么四次：TCP 全双工——你发完了不代表我也发完了，各关各的。
- FIN = 礼貌告别，RST = 摔门走人
- 2MSL 等待防最后的 ACK 丢包

### TLS 加密握手（TLS 1.3）
完成三件事：身份认证（CA 证书）→ 密钥协商（DH/ECDHE）→ 开始对称加密
- TLS 1.3：1-RTT，一次往返搞定
- 证书验证：CA 私钥加密签名 → 浏览器用 CA 公钥解密比对哈希
- 非对称加密互为逆运算：公钥加密私钥解（保密），私钥加密公钥解（签名）

### 数字签名原理
CA 对证书内容 SHA256 取哈希 → 用 CA 私钥加密 → 附在证书里
浏览器用 CA 公钥解密得 H2 → 自己重算 H1 → 比对 H1==H2

### SQL 注入
原理：用户输入被当 SQL 代码执行
防御：参数化查询（把 SQL 结构和数据分开提交，`?` 占位符不会被当代码）
输入白名单（下拉框限定查询类型）也是辅助手段

### XSS 三种类型
- 反射型：URL 参数含恶意脚本，点链接的人受害
- 存储型：恶意代码存在服务器数据库，所有访问者受害
- DOM 型：纯前端问题，不经过服务器

### CSRF（跨站请求伪造）
原理：浏览器自动带 Cookie 发请求，服务器分不清是你自愿还是被诱导
关键：黑客拿不到 Cookie，但他能骗你的浏览器替他发请求
防御：CSRF Token（表单嵌随机码，黑客跨站读不到）+ SameSite Cookie + Referer 检查

### 同源策略
浏览器铁律：A 网站的代码不能读 B 网站的页面内容
协议+域名+端口三者相同才算同源
CSRF Token 安全性靠这条保证——evil.com 读不到 bank.com 页面里的 Token

### IDOR（越权漏洞）
- 水平越权：User A 看到 User B 数据
- 垂直越权：普通用户执行管理员操作
修复：服务端校验当前用户是否有权访问，别信客户端传的 id

### Nmap 参数
| 参数 | 用途 |
|------|------|
| `-sS` | TCP SYN 半连接扫描（技术隐蔽但 IDS 能检测） |
| `-sT` | TCP 全连接扫描（走完三次握手，日志留痕） |
| `-sU` | UDP 扫描 |
| `-sV` | 服务版本探测 |
| `-O` | OS 指纹识别 |

规避：`-f` 分片、`-T0/T1` 慢速、`-D` 诱饵、`--source-port 53` 伪装 DNS

### 端口状态
- open：收到 SYN+ACK，端口开着
- closed：收到 RST，端口关了且无防火墙拦截
- filtered：啥也没收到或有防火墙截胡

### 纵深防御（Defense in Depth）
```
阿里云安全组 → UFW → SSH密钥 → fail2ban → 日志审计
```
不赌单层，多层兜底。

### 最小权限原则
UFW default deny → 只放行需要端口的 → MySQL 专用只读账号不给 root

### 3-2-1 备份原则
3 份拷贝、2 种介质、1 份异地

### 堡垒机 / SIEM / SOC
- 堡垒机：运维跳板机 + 操作录像机，所有人统一入口
- SIEM：全设备日志汇聚，统一关联分析（攻击链）
- SOC：人+工具+流程，7×24 安全运营
- IDS：只告警不动手；IPS：检测+阻断；SIEM：全局日志关联 vs IDS/IPS 实时单点

### 零信任
不再默认信任内网，每次访问都要验证

### 索引（B+树）
- B+树深度 3-4 层，3-4 次 IO 叶子节点定位数据
- 叶子节点用双向链表串起来，范围查询快
- 只在常用 WHERE、JOIN、ORDER BY 列上加
- 代价：占空间、写入变慢
- B 树 vs B+树：B+树叶子链表范围查询快，树更矮 IO 更少

### EXPLAIN 执行计划
```sql
EXPLAIN SELECT ...;
```
- `type=ALL` → 全表扫描，百万行一行行翻 → 需要加索引
- `type=ref/eq_ref` → 走索引，快
- `rows` → 预计扫描行数
- `Extra: Using filesort` → ORDER BY 没用索引，手动排序

### MySQL 增删改查
```sql
INSERT INTO t (col) VALUES ('val');
DELETE FROM t WHERE id = 1;
UPDATE t SET col = 'val' WHERE id = 1;
SELECT col FROM t WHERE condition;
ALTER TABLE t ADD COLUMN col VARCHAR(50);  -- 加列
```

### Linux 排障四件套
```bash
systemctl status nginx      # 服务在不在
journalctl -u nginx --since '10min ago'  # 日志有无报错
ss -tlnp | grep 80          # 端口监听否
top / df -h                 # 资源打满没
ps aux --sort=-%cpu | head -5  # CPU 前5
du -sh /* 2>/dev/null | sort -rh | head -10  # 磁盘谁在吃
kill -9 PID                 # 强制杀进程（-15 优雅退出）
```

---

## 2. MySQL 实操

### Navicat 远程连接
- SSH 进服务器改 MySQL 密码：`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '密码';`
- 改绑定地址：`bind-address = 0.0.0.0`
- UFW 开 3306
- 阿里云安全组仅放行自己公网 IP（42.48.102.63/32）
- 需要额外授权：`CREATE USER 'root'@'IP'` + `GRANT ALL`
- 3306 必须 /32 不能 0/0——MySQL 只有密码防线，不像 SSH 有密钥+fail2ban 兜底

### 建库建表
- 数据库 `server_monitor`，字符集 `utf8mb4`，排序 `utf8mb4_general_ci`
- `servers` 表：id, hostname, ip, os, created_at
- `inspection_logs` 表：id, server_id(FK), cpu_usage, mem_usage, disk_usage, status(ENUM), check_time
- 插入了服务器和巡检数据

### 查询示例
```sql
SELECT s.hostname, s.ip, l.cpu_usage, l.mem_usage, l.status, l.check_time
FROM inspection_logs l
JOIN servers s ON l.server_id = s.id
WHERE l.cpu_usage > 80
ORDER BY l.check_time DESC;
```

### MySQL 自带三库
- `information_schema`：元数据
- `mysql`：账号权限
- `performance_schema`：性能数据

### 字符集与排序规则
- 字符集 = 字节到字符的编码规则，选 utf8mb4
- 排序规则：`_general_ci` 不区分大小写，`_bin` 区分

---

## 3. 面试技巧

### 常见报错速查
- nginx `bind() failed (98: Address already in use)` → 端口被占
- `Can't connect to local MySQL server` → MySQL 挂了
- `Failed password for root from IP` → SSH 爆破
- `Out of memory: Killed process` → OOM
- Nginx `502 Bad Gateway` → 后端没响应

### /var 目录
- `/var/log`：所有日志（auth.log、nginx/、mysql/、syslog）
- `/var/lib`：服务持续变化的数据（mysql/存表、docker/镜像容器）

### 面试微操
- 别主动提 CTF，除非对方问
- 别说"我不会" → 换成"我理解原理但还没实操过"
- 别贬低自己
- 别背答案像念课文

### 自我介绍话术（30秒）
三句：我是谁 + 做了啥 + 为什么来

### 反问面试官
1. 团队目前几个人，有没有老同事带实习生？
2. 这个岗位日常具体做哪些工作？

---

## 4. CTF 备战

### 已报名比赛
| 比赛 | 时间 | 时长 | 官网 |
|------|------|:--:|------|
| jailCTF 2026 | 7/25 04:00 - 7/28 04:00 | 72h | https://ctf.pyjail.club/ |
| D^3CTF 2026 | 7/25 20:00 - 7/26 20:00 | 24h | https://d3c.tf/ |

- CTFtime 队伍：Hijacking（已替换原 wwqy）
- jailCTF 重点：pyjail、esolang 沙盒逃逸
- Discord：https://discord.gg/JxtuFxMaE8

---

## 5. 面试安排

- 公司：赢时胜 长沙分公司（已上市，1000-9999人，长沙 450 人研发）
- 岗位：软件运维实习生
- 地点：长沙开福区华创国际广场 A 座 29 层
- 时间：周六（7/25）下午 5:00
- 薪资：3000-4000，150-200/天

---

## 6. 简历投递记录（今日）

| 公司 | 城市 | 薪资 | 状态 |
|------|------|------|------|
| 凯捷 | 沈阳 | 110-120/天 | 已发简历 |
| UCloud | 成都 | 150-170/天 | 已沟通 |
| 南威软件 | 承德 | 150-200/天 | 已沟通 |
| 南京某司 | 南京 | 100-150/天 | 已发简历 |
| 三亚都广科技 | 三亚 | 70-100/天 | 被拒 |

---

## 7. 备忘

- 简历 CTF 队伍名已全部替换为 Hijacking
- MySQL root 密码注意更换，老密码已在聊天记录泄露
- 服务器 3306 端口当前仅对 42.48.102.63/32 开放
- 下一个学习节点：Day 14（面试后补）
