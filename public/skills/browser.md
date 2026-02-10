# 浏览器操作

## 何时调用
当用户提及以下内容时激活：
- "浏览器"、"打开网页"、"访问网址"、"导航"
- "浏览器截图"、"浏览器状态"、"启动浏览器"
- "点击元素"、"输入文本"、"滚动页面"

## 工具名称
`browser`

## 环境要求
- **Linux**: 需要安装 Chromium 浏览器
  ```bash
  # Debian/Ubuntu
  apt-get install chromium-browser
  
  # 或使用 snap
  snap install chromium
  ```
- **macOS**: 系统自带 Safari 或安装 Chrome
- **Windows**: 安装 Chrome 或 Edge

## 启动浏览器

### 自动检测（推荐）
```
{ "action": "status" }
```
返回浏览器状态和配置信息

### 手动启动
```bash
# Linux (headless模式)
chromium-browser --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile \
  --headless --no-sandbox --disable-gpu

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile
```

## 支持的操作

### 1. 查看浏览器状态
```
{ "action": "status" }
```
返回：
- 是否运行
- CDP 端口
- 检测到的浏览器
- 配置信息

### 2. 启动浏览器实例
```
{ "action": "start" }
```
自动启动已配置的浏览器实例

### 3. 停止浏览器
```
{ "action": "stop" }
```

### 4. 打开网页
```
{
  "action": "navigate",
  "targetUrl": "https://www.baidu.com"
}
```

### 5. 截图
```
{ "action": "screenshot" }
```
保存截图到 `~/.openclaw/media/browser/`

### 6. 获取页面快照（DOM结构）
```
{ "action": "snapshot" }
```
返回页面元素的层级结构（ARIA 可访问性树）

### 7. 点击元素
```
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e123"  // 元素引用ID
  }
}
```

### 8. 输入文本
```
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "e123",
    "text": "要输入的内容"
  }
}
```

### 9. 滚动页面
```
{
  "action": "act",
  "request": {
    "kind": "scroll",
    "x": 0,
    "y": 500
  }
}
```

### 10. 执行 JavaScript
```
{
  "action": "act",
  "request": {
    "kind": "evaluate",
    "script": "document.title"
  }
}
```

### 11. 等待元素
```
{
  "action": "act",
  "request": {
    "kind": "wait",
    "ref": "e123"
  }
}
```

## 元素引用（ref）

使用 `snapshot` 获取页面后，每个元素都有 `ref` 属性：
```
- generic [ref=e3]:
  - link "登录" [ref=e21] [cursor=pointer]:
    - /url: https://passport.baidu.com/v2/login
```

点击登录按钮：
```
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e21"
  }
}
```

## 实用技巧

### 等待页面加载
```javascript
// 在 evaluate 中执行
await new Promise(r => setTimeout(r, 2000));
```

### 处理 iframe
```json
{
  "action": "snapshot",
  "frame": "iframe_ref"
}
```

### 处理弹窗
```json
{
  "action": "act",
  "request": {
    "kind": "accept"
  }
}
```

## 常见问题

### Q: 浏览器无法启动
A: 检查 Chrome/Chromium 是否安装：
```bash
which chromium-browser
chromium-browser --version
```

### Q: CDP 连接超时
A: 浏览器进程可能崩溃，重启浏览器：
```bash
pkill -f "chromium.*remote-debugging"
# 然后重新启动
```

### Q: 元素找不到
A: 重新执行 `snapshot` 获取最新 DOM 树

### Q: 滑块验证无法通过
A: 目前无法自动化完成滑块验证，建议：
1. 手动完成验证
2. 使用第三方打码服务

## 完整使用示例

**场景**: 自动登录百度

```json
// 1. 打开登录页面
{
  "action": "navigate",
  "targetUrl": "https://passport.baidu.com/v2/login"
}

// 2. 点击用户名登录
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e27"
  }
}

// 3. 输入账号
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "e50",
    "text": "13596016143"
  }
}

// 4. 输入密码
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "e52",
    "text": "your_password"
  }
}

// 5. 点击登录
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e54"
  }
}

// 6. 截图确认结果
{ "action": "screenshot" }
```

## 配置要求
```yaml
# ~/.openclaw/openclaw.json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "mychrome",
    "profiles": {
      "mychrome": {
        "cdpUrl": "http://127.0.0.1:9222",
        "color": "#FF4500"
      }
    }
  }
}
```

## 高级配置

### 指定浏览器路径
```json
{
  "browser": {
    "executablePath": "/usr/bin/chromium-browser"
  }
}
```

### 无头模式
```json
{
  "browser": {
    "headless": true
  }
}
```

### 多标签页管理
```json
{
  "action": "tabs"
}
```

### 切换标签页
```json
{
  "action": "focus",
  "targetId": "target_id_from_tabs"
}
```

## 性能优化

1. **减少截图频率**：截图会消耗较多资源
2. **复用浏览器实例**：避免频繁启动/停止
3. **使用等待条件**：避免硬编码 sleep
4. **批量操作**：减少 CDP 调用次数

## 注意事项

⚠️ **安全警告**:
- 不要在浏览器中输入敏感密码后截图保存
- 定期清理浏览器缓存和 cookies
- 使用独立的用户数据目录

⚠️ **限制**:
- 无法通过滑块验证码
- 某些网站会检测自动化并阻止
- 文件下载需要额外配置
