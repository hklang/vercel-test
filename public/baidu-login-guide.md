# 百度网盘自动化登录完整流程

## 概述
本文档记录通过OpenClaw浏览器自动化登录百度网盘的全过程。

## 环境准备

### 1. 安装必要工具
```bash
# 安装xvfb（虚拟显示器）
sudo apt-get install xvfb

# 安装Chromium浏览器
sudo apt-get install chromium-browser
```

### 2. 启动带虚拟显示的浏览器
```bash
xvfb-run --auto-servernum chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/baidu-profile \
  --no-sandbox \
  --window-size=1280,800
```

**关键说明：**
- **为什么需要xvfb？** 百度网盘登录需要显示二维码，headless模式无法显示
- **user-data-dir** 保存登录cookies，后续无需重新登录

## 完整登录流程

### 步骤1：启动浏览器并打开百度网盘
```json
{
  "action": "open",
  "targetUrl": "https://pan.baidu.com"
}
```

### 步骤2：点击"去登录"按钮
```json
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "去登录按钮的ref"
  }
}
```

### 步骤3：提取纯二维码（关键技巧）
```json
{
  "action": "act",
  "request": {
    "kind": "evaluate",
    "fn": "document.body.innerHTML = '<img src=\"' + document.querySelector('img[src*=\"qrcode\"]').src + '\" />'"
  }
}
```

### 步骤4：截图发送二维码给用户
```json
{ "action": "screenshot" }
```

### 步骤5：发送图片到聊天窗口
```python
# 使用message工具发送图片
message(action="send", filePath="/path/to/qrcode.png")
```

### 步骤6：用户扫码登录
- 用户使用百度网盘App扫描二维码
- 在手机上确认登录
- 浏览器自动跳转到网盘首页

### 步骤7：验证登录成功
```json
{ "action": "snapshot" }
```

## 登录成功后的操作

登录后可以直接操作百度网盘：
- 浏览文件
- 上传/下载文件
- 创建文件夹
- 分享文件等

## 保存登录状态

浏览器user-data-dir保存了登录cookies，下次启动无需重新登录：
```bash
# 下次启动使用相同的user-data-dir
chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/baidu-profile \
  ...
```

## 常见问题

### Q: 二维码刷新了怎么办？
A: 重新执行步骤3-5

### Q: 需要重新登录吗？
A: 不需要，cookies保存在user-data-dir中

### Q: 提示登录过期？
A: 删除cookies重新登录：
```bash
rm -rf /tmp/baidu-profile
```

## 相关文件
- `public/baidu-qrcode-trick.md` - 纯二维码提取技巧

## 更新时间
2026-02-26 23:16
