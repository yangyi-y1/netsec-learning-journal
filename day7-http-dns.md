# Day 7：应用层协议 — HTTP/HTTPS/DNS

> 2026-07-20 | Windows + Wireshark

## DNS 解析

### nslookup baidu.com

```text
Server:  ChinaUnicom.bbrouter
Address:  192.168.1.1

Non-authoritative answer:
Name:    baidu.com
Addresses:  111.63.65.103
             124.237.177.164
             110.242.74.102
             111.63.65.247
```

关键点：
- `Server: 192.168.1.1` → 家庭路由器充当 DNS 转发器，不是权威 DNS
- `Non-authoritative answer` → 路由器从上游联通 DNS 拿到的缓存结果
- 返回 4 个 IP → DNS 负载均衡，不同用户可能分到不同 IP

### Wireshark DNS 抓包

| 帧 | 方向 | 内容 |
|----|------|------|
| 122 | 本机→路由器 | `Standard query AAAA httpbin.org`（查 IPv6） |
| 123 | 本机→路由器 | `Standard query A httpbin.org`（查 IPv4） |
| 124 | 路由器→本机 | `Standard query response AAAA` → SOA（表示无 IPv6） |
| 125 | 路由器→本机 | `Standard query response A` → 4 个 IPv4 地址 |

- A 记录 = 查 IPv4 地址
- AAAA 记录 = 查 IPv6 地址
- SOA = 权威应答表示"这条记录类型不存在"，即 httpbin.org 没有 IPv6
- DNS 使用 UDP 53 端口，查询和响应是成对出现的
- `0x51ba` / `0xeef8` 是事务 ID，请求和响应的 ID 相同才算配对

## HTTP 协议

### curl 请求 / 响应拆解

```text
# 请求（> 发出）
GET /get HTTP/1.1
Host: httpbin.org
User-Agent: curl/8.21.0
Accept: */*

# 响应（< 返回）
HTTP/1.1 200 OK
Date: Sun, 19 Jul 2026 23:33:23 GMT
Content-Type: application/json
Content-Length: 253
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
```

请求头解读：
| 头部 | 含义 |
|------|------|
| `GET /get HTTP/1.1` | 请求方法 + 路径 + 协议版本 |
| `Host: httpbin.org` | 目标主机（一台服务器可托管多个网站） |
| `User-Agent` | 客户端标识 |
| `Accept: */*` | 接受任意响应格式 |

响应头解读：
| 头部 | 含义 |
|------|------|
| `HTTP/1.1 200 OK` | 状态行，200 = 成功 |
| `Content-Type: application/json` | 响应体是 JSON 格式 |
| `Content-Length: 253` | 响应体大小 253 字节 |
| `Server: gunicorn/19.9.0` | 服务器用的 Web 框架 |

### 状态码速记

| 范围 | 含义 | 例子 |
|------|------|------|
| 2xx | 成功 | 200 OK |
| 3xx | 重定向 | 301 永久, 302 临时 |
| 4xx | 客户端错误 | 404 找不到, 403 禁止 |
| 5xx | 服务端错误 | 500 内部错误, 502 网关错误 |

### Wireshark HTTP 抓包

过滤 `http` 后看到最少 2 个包：

| 帧 | Info | 说明 |
|----|------|------|
| ?? | `GET /get HTTP/1.1` | 发出的请求，含 Host / User-Agent / Accept 头 |
| ?? | `HTTP/1.1 200 OK` | 返回的响应，含 Content-Type / Content-Length / Server 头 |

数据包五层结构（俄罗斯套娃）：

| 层 | 协议 | 看什么 |
|----|------|--------|
| 1-链路层 | Ethernet II | MAC 地址 |
| 2-网络层 | IP | 源 IP → 目标 IP |
| 3-传输层 | TCP | 端口 80、Seq/Ack 序号 |
| 4-应用层 | HTTP | GET、200 OK、响应头 |
| 5-数据 | JSON / Line-based text | 真正的响应内容 |

Wireshark 将 JSON 解析为可折叠树（`javascript object` → `member` → `key: value`），和原始文本是同一份数据的不同展示方式。

## HTTP vs HTTPS 抓包对比

| | HTTP | HTTPS |
|----|------|-------|
| 端口 | 80 | 443 |
| 抓包可见性 | 请求头、响应头、响应体全部明文 | 全是密文 |
| Wireshark 过滤器 | `http` | `tls` |
| TLS 握手后 | 无 | 加密数据带 `Application Data` |

HTTP 访问 httpbin.org 时，Wireshark 能直接看到 `GET /get` 和 JSON 响应。
HTTPS 访问 baidu.com 时，抓包只能看到 TLS 加密载荷，无法看到具体请求内容。

## 面试话术

> "我理解 DNS 的 A 记录和 AAAA 记录分别查 IPv4 和 IPv6 地址，用 nslookup 和 Wireshark 都实操过。HTTP 协议请求由请求行(GET/POST + 路径 + 版本)、请求头(Host/User-Agent)、请求体组成；响应由状态行(200/404/500)、响应头(Content-Type)、响应体组成。HTTP 是明文传输，HTTPS 通过 TLS 加密，Wireshark 抓 HTTP 能看到全部内容，HTTPS 只能看到加密后的 TLS 记录。我理解数据包的五层结构：以太网→IP→TCP→HTTP→数据，每层只关心自己的任务。"
