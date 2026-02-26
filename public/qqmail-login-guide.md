# QQ邮箱自动化登录流程

## 概述
本文档记录通过OpenClaw浏览器自动化登录QQ邮箱的全过程。

## 环境准备

### 启动浏览器
```bash
xvfb-run --auto-servernum chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile \
  --no-sandbox \
  --window-size=1280,800
```

## 登录流程

### 步骤1：打开QQ邮箱首页
```json
{
  "action": "open",
  "targetUrl": "https://mail.qq.com/",
  "profile": "mychrome"
}
```

### 步骤2：等待页面加载
```bash
sleep 3-4秒
```

### 步骤3：获取登录二维码
直接截取完整页面发送到聊天窗口，用户扫码登录。

### 步骤4：验证登录成功
登录成功后，页面会显示：
- 用户头像和邮箱地址
- 收件箱邮件数量

## 登录成功的特征

登录成功后，页面结构包含：
- 用户信息：`蒋国春` + `xxx@qq.com`
- 左侧菜单：收件箱、已发送、草稿箱等
- 顶部菜单：写信、设置等

## 常用操作

### 查看收件箱
```json
{
  "action": "snapshot"
}
```

### 读取邮件
点击邮件标题即可查看邮件详细内容。

## 保存登录状态

浏览器user-data-dir保存了登录cookies，下次启动无需重新登录。

## 注意事项

1. **二维码时效**：QQ邮箱二维码时效较短，扫码要快
2. **多iframe**：QQ邮箱页面使用多个iframe，二维码在iframe中
3. **点击QQ登录**：如果显示微信登录，需要点击切换到QQ登录

## 相关文件
- `public/baidu-login-guide.md` - 百度网盘登录指南

## 更新时间
2026-02-27 00:20
