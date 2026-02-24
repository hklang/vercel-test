# 浏览器操作方法记录

## 概述
本文档记录通过OpenClaw的`browser`工具操作Chromium浏览器的方法和技巧，包括启动、导航、截图、元素操作等。

## 环境配置

### 1. 浏览器安装
```bash
# Debian/Ubuntu系统安装Chromium
apt-get install chromium-browser

# 或使用snap安装
snap install chromium
```

### 2. 手动启动浏览器（当OpenClaw浏览器服务不可用时）
```bash
# 启动Chromium并启用CDP远程调试
chromium-browser --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile \
  --no-sandbox \
  --disable-gpu \
  --window-size=1280,800 \
  --disable-blink-features=AutomationControlled
```

**关键参数说明：**
- `--remote-debugging-port=9222`：启用CDP协议，端口9222
- `--user-data-dir=/tmp/chrome-profile`：指定用户数据目录
- `--no-sandbox`：禁用沙盒（某些环境需要）
- `--disable-gpu`：禁用GPU加速（无头模式需要）
- `--window-size=1280,800`：设置窗口大小
- `--disable-blink-features=AutomationControlled`：隐藏自动化控制特征

## 基本操作流程

### 1. 检查浏览器状态
```javascript
// 使用browser工具
{
  "action": "status"
}
```

### 2. 打开网页
```javascript
// 打开指定URL
{
  "action": "open",
  "targetUrl": "https://example.com",
  "profile": "mychrome"
}
```

### 3. 获取页面快照（分析页面结构）
```javascript
// 获取页面元素引用
{
  "action": "snapshot",
  "targetId": "页面ID",
  "refs": "aria"  // 或 "role"
}
```

### 4. 操作页面元素
```javascript
// 点击元素
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e123"  // 元素引用
  }
}

// 输入文本
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "e123",
    "text": "要输入的内容"
  }
}

// 按键操作
{
  "action": "act",
  "request": {
    "kind": "press",
    "key": "Enter"
  }
}
```

### 5. 截图
```javascript
// 截取当前页面
{
  "action": "screenshot",
  "targetId": "页面ID",
  "fullPage": true  // 是否截取完整页面
}
```

## 实战案例

### 案例1：处理Cloudflare人机验证

#### 目标网址
```
https://cf.2hg.com/?action=mc
```

#### 验证特征
- HTTP状态码：403 Forbidden
- 响应头：`cf-mitigated: challenge`
- 页面内容："Just a moment..." 或 "执行安全验证"

#### 解决方案
1. **使用非无头浏览器模式**
   ```bash
   # 不要使用--headless参数
   chromium-browser --remote-debugging-port=9222 \
     --user-data-dir=/tmp/chrome-profile \
     --no-sandbox \
     --window-size=1280,800
   ```

2. **验证通过标志**
   - 页面显示："it works"
   - HTTP状态码：200 OK
   - 页面正常加载目标内容

#### 完整操作流程
```javascript
// 1. 打开验证页面
{
  "action": "open",
  "targetUrl": "https://cf.2hg.com/?action=mc",
  "profile": "mychrome"
}

// 2. 等待验证完成（手动或自动）
// 3. 截图验证结果
{
  "action": "screenshot",
  "targetId": "页面ID",
  "fullPage": true
}
```

### 案例2：访问本地文件系统

#### 目标
访问本地`public/skills/`目录

#### 操作流程
```javascript
// 1. 打开本地目录
{
  "action": "open",
  "targetUrl": "file:///home/lang/.openclaw/workspace/public/skills/",
  "profile": "mychrome"
}

// 2. 截图目录内容
{
  "action": "screenshot",
  "targetId": "页面ID",
  "fullPage": true
}
```

#### 注意事项
- 本地文件访问可能需要浏览器权限配置
- 某些浏览器安全策略会限制本地文件访问

## 高级技巧

### 1. 处理页面加载等待
```javascript
// 等待特定元素出现
{
  "action": "act",
  "request": {
    "kind": "wait",
    "timeMs": 5000  // 等待5秒
  }
}
```

### 2. 处理iframe和弹窗
```javascript
// 切换到iframe
{
  "action": "act",
  "request": {
    "kind": "evaluate",
    "fn": "document.querySelector('iframe').contentWindow"
  }
}
```

### 3. 模拟用户行为（减少被检测风险）
```javascript
// 添加随机延迟
await page.waitForTimeout(1000 + Math.random() * 2000);

// 模拟鼠标移动
await page.mouse.move(Math.random() * 100, Math.random() * 100);
```

## 故障排除

### 常见问题及解决方案

#### 1. 浏览器控制服务不可用
**症状**：`Can't reach the OpenClaw browser control service`
**解决方案**：
```bash
# 重启OpenClaw网关
openclaw gateway restart

# 或手动启动浏览器
chromium-browser --remote-debugging-port=9222 ...
```

#### 2. 无法通过人机验证
**症状**：页面显示验证挑战，无法访问目标内容
**解决方案**：
- 使用非无头浏览器模式
- 添加`--disable-blink-features=AutomationControlled`
- 设置合理的窗口大小
- 考虑使用验证码解决服务（如2Captcha）

#### 3. 本地文件访问被拒绝
**症状**：`net::ERR_ACCESS_DENIED`
**解决方案**：
- 检查文件路径权限
- 使用HTTP服务器提供本地文件
- 修改浏览器安全策略

#### 4. 元素操作失败
**症状**：点击或输入操作无效
**解决方案**：
- 使用`snapshot`确认元素引用正确
- 检查元素是否在iframe中
- 添加等待时间确保元素加载完成

## 最佳实践

### 1. 配置管理
- 将常用浏览器配置保存为profile
- 使用环境变量管理敏感信息
- 定期更新浏览器版本

### 2. 错误处理
- 添加超时机制
- 实现重试逻辑
- 记录详细的操作日志

### 3. 性能优化
- 复用浏览器实例
- 合理设置等待时间
- 避免不必要的截图操作

### 4. 安全考虑
- 遵守网站服务条款
- 控制请求频率
- 标识自动化工具身份

## 工具集成

### 与OpenClaw其他工具配合使用

#### 1. 结合`exec`工具
```javascript
// 先检查系统状态
{
  "action": "exec",
  "command": "ps aux | grep chromium"
}

// 再操作浏览器
{
  "action": "browser",
  "action": "status"
}
```

#### 2. 结合`message`工具
```javascript
// 截图后发送到聊天
{
  "action": "browser",
  "action": "screenshot"
}

{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "截图已生成",
  "media": "MEDIA:截图路径"
}
```

## 学习资源

### 1. 官方文档
- OpenClaw浏览器工具文档：`public/skills/browser.md`
- Chrome DevTools Protocol官方文档

### 2. 参考案例
- `public/moltbook-browser-operations.md` - Moltbook论坛操作
- `public/skills/browser_学习笔记.md` - 实战操作笔记

### 3. 社区资源
- OpenClaw Discord社区
- GitHub Issues和讨论区

## 更新记录

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-02-25 | 1.0 | 初始版本，记录基本操作方法 |
| 2026-02-25 | 1.1 | 添加Cloudflare验证处理案例 |
| 2026-02-25 | 1.2 | 添加故障排除和最佳实践 |

---

**创建者**：OpenClaw AI Assistant  
**最后更新**：2026-02-25  
**适用场景**：浏览器自动化、网页操作、数据采集、测试验证