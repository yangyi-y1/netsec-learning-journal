# Day 7 补充：Kali 安装 + CTFtime 注册 + 简历升级

> 2026-07-20 | Kali Linux 2026.2 + CTFtime

## Kali Linux 安装与配置

### 下载与导入
- 下载 Kali 2026.2 VirtualBox 预建镜像（3.7GB，`.7z` 格式）
- 解压得到 `.vbox`（VM 配置）+ `.vdi`（虚拟磁盘 15.1GB）
- VBoxManage registervm 注册到 VirtualBox
- 配置：8GB 内存、4 CPU
- 默认登录：`kali / kali`，带 Xfce 桌面 GUI

### 安装后配置
| 操作 | 命令 |
|------|------|
| 更新软件包列表 | `sudo apt update` |
| 升级所有工具 | `sudo apt upgrade -y` |
| 清理旧依赖 | `sudo apt autoremove -y` |
| 安装 SSH 服务 | `sudo apt install -y openssh-server` |
| 启动并开机自启 | `sudo systemctl enable ssh --now` |
| 查看运行状态 | `systemctl status ssh` → `active (running)` |

### VirtualBox 剪贴板共享
```bash
VBoxManage controlvm "kali-linux-2026.2-virtualbox-amd64" clipboard mode bidirectional
```
- 终端内：`Ctrl+Shift+C/V`
- 桌面其他地方：`Ctrl+C/V`

### Kali 自带安全工具速览
| 类别 | 工具 |
|------|------|
| 信息收集 | Nmap |
| 漏洞扫描 | Nikto |
| Web 应用分析 | Burp Suite, sqlmap |
| 密码攻击 | John the Ripper, Hydra |
| 无线攻击 | Aircrack-ng |
| 抓包分析 | Wireshark, tcpdump |

---

## CTFtime 注册 + jailCTF 2026 报名

### 注册步骤
1. ctftime.org 注册账号
2. Teams → Create new team
   - Name: `wwqy`
   - Country: China
   - 非 Academic 队伍（不勾选）
   - Description: `Individual player, learning cybersecurity.`
3. 找 jailCTF 2026 → Register → 选 wwqy → 确认
4. 成功后会跳转到比赛平台（黑色界面）

### jailCTF 2026 信息
| 项目 | 内容 |
|------|------|
| 类型 | Jeopardy（解题模式） |
| 形式 | On-line（线上） |
| 开始 | **7月25日（周五）凌晨 4:00**（北京时间） |
| 结束 | 7月28日（周一）凌晨 4:00 |
| 时长 | 72 小时 |
| 权重 | 37（新手友好） |
| 当前报名 | 46 队 |

### 比赛平台界面
- **Challenges**：比赛题目（开赛后出现）
- **Scoreboard**：实时排名
- **Profile**：队伍信息 + 邀请链接
- **Home**：公告

---

## 简历升级

### 本次更新
- 期望城市扩到 6 个（长沙/深圳/武汉/杭州/上海/广州）
- 专业技能拆成 6 大板块（Linux/Shell/网络/Web安全/安全工具/数据库）
- 项目经历改为「Linux全栈安全运维实战」，四层结构
- 新增个人总结板块
- 证书栏追加 CTFtime 队伍注册 + jailCTF 2026 参与

### 待完成的简历加分项
1. 云上 ECS 项目（公网可访问）
2. jailCTF 打出至少一题
3. Nmap 扫描报告推 GitHub
4. TryHackMe OWASP 房间完成记录

---

## 面试要点复习

### Q: Kali 预装了哪些类型的安全工具？
信息收集(Nmap)、漏洞扫描、Web分析(Burp/Sqlmap)、密码攻击(John/Hydra)、无线攻击(Aircrack-ng)、抓包分析(Wireshark/Tcpdump)

### Q: SSH 怎么装的？
`sudo apt install openssh-server` → `sudo systemctl enable ssh --now` → `systemctl status ssh` 确认 active

### Q: CTF 比赛 Jeopardy 模式是什么意思？
解题模式——没有红蓝对抗，所有队伍面对相同的题目(Misc/Crypto/Web/Reverse/Pwn 等)，解一题得一面旗，按得分排名。
