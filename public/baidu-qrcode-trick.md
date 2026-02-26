# 百度网盘登录技巧：只发送纯二维码

## 问题
百度网盘登录页面包含大量其他内容，直接截图会包含很多无关信息，不方便用户扫码。

## 解决方案
通过JavaScript提取二维码图片URL，然后用纯图片方式展示。

## 操作步骤

### 1. 打开百度网盘登录页面
```json
{
  "action": "open",
  "targetUrl": "https://pan.baidu.com"
}
```

### 2. 点击"去登录"按钮
```json
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "去登录按钮的ref"
  }
}
```

### 3. 提取二维码图片URL（关键步骤）
```json
{
  "action": "act",
  "request": {
    "kind": "evaluate",
    "fn": "document.body.innerHTML = '<img src=\"' + document.querySelector('img[src*=\"qrcode\"]').src + '\" />'"
  }
}
```

### 4. 截图发送
```json
{ "action": "screenshot" }
```

### 5. 发送到聊天窗口
使用message工具发送图片给用户扫描。

## 原理
- 二维码图片URL在 `img[src*="qrcode"]` 元素中
- 通过JavaScript将整个页面替换为只包含二维码图片的HTML
- 截图后发送，这样用户收到的就只是纯净的二维码

## 效果
用户可以直接扫描二维码，无需处理多余信息。

## 记录时间
2026-02-26 23:12
