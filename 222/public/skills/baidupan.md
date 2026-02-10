# 百度网盘操作

## 何时调用
当用户提及以下内容时激活：
- "百度网盘"、"百度云"、"pan.baidu.com"
- "网盘下载"、"网盘上传"、"分享链接"
- "提取文件"、"保存到网盘"

## 操作方式
通过 **浏览器工具** 访问百度网盘网页版进行操作

## 访问百度网盘
```
{ "action": "navigate", "targetUrl": "https://pan.baidu.com" }
```

## 主要功能

### 1. 文件管理
- 浏览文件/文件夹
- 新建文件夹
- 移动/重命名文件
- 删除文件
- 搜索文件

### 2. 上传文件
- 点击"上传"按钮
- 选择本地文件
- 支持拖拽上传

### 3. 下载文件
- 选择文件/文件夹
- 点击"下载"
- 支持批量下载

### 4. 分享功能
- 选择文件
- 点击"分享"
- 生成分享链接
- 设置有效期和提取码

### 5. 离线下载
- 粘贴下载链接
- 添加到离线下载队列

## 使用示例

### 场景1: 下载分享的文件

**用户**: "下载这个链接 https://pan.baidu.com/s/1ABC123"

**操作流程**:
```json
// 1. 打开链接
{
  "action": "navigate",
  "targetUrl": "https://pan.baidu.com/s/1ABC123"
}
```

```json
// 2. 查看页面快照，确认提取码输入框
{ "action": "snapshot" }
```

```json
// 3. 如果需要输入提取码
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "提取码输入框的ref",
    "text": "提取码"
  }
}
```

```json
// 4. 点击提取文件
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "提取按钮的ref"
  }
}
```

```json
// 5. 点击下载按钮
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "下载按钮的ref"
  }
}
```

### 场景2: 上传文件

**用户**: "上传文件到网盘"

**操作流程**:
```json
// 1. 打开百度网盘
{
  "action": "navigate",
  "targetUrl": "https://pan.baidu.com"
}
```

```json
// 2. 点击上传按钮（需要用户手动选择文件）
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "上传按钮的ref"
  }
}
```

⚠️ **注意**: 文件上传需要用户手动选择本地文件，浏览器自动化无法触发文件选择对话框

### 场景3: 创建分享链接

**用户**: "分享这个文件"

**操作流程**:
```json
// 1. 打开网盘，找到要分享的文件
{
  "action": "navigate",
  "targetUrl": "https://pan.baidu.com"
}
```

```json
// 2. 右键点击或选择文件
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "文件的ref"
  }
}
```

```json
// 3. 点击分享按钮
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "分享按钮的ref"
  }
}
```

## 常见问题

### Q: 无法登录百度网盘
A: 百度网盘有滑块验证，无法自动登录。建议：
1. 手动在浏览器中登录
2. 使用已登录的浏览器配置文件

### Q: 下载的文件保存在哪里？
A: 浏览器的默认下载目录（通常在 `/home/用户名/Downloads`）

### Q: 如何使用已登录的浏览器配置？
A: 启动浏览器时指定用户数据目录：
```bash
chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir=/path/to/your/chrome/profile
```

### Q: 批量下载支持吗？
A: 可以按住 Ctrl 多选文件，然后点击下载

### Q: 离线下载怎么用？
```json
{
  "action": "navigate",
  "targetUrl": "https://pan.baidu.com/download"
}
```

## 高级技巧

### 1. 使用已登录的浏览器配置
```bash
# 先在普通浏览器中登录百度网盘
# 然后获取用户数据目录（Chrome: ~/.config/google-chrome）
# 启动自动化浏览器时使用该目录
chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.config/google-chrome"
```

### 2. 下载大文件时保持连接
```json
// 使用 act 等待下载完成
{
  "action": "act",
  "request": {
    "kind": "wait",
    "timeMs": 30000
  }
}
```

### 3. 处理弹窗警告
```json
{
  "action": "act",
  "request": {
    "kind": "accept"
  }
}
```

## 注意事项

⚠️ **登录限制**:
- 百度网盘有复杂的验证机制
- 新设备登录可能需要短信验证
- 自动化登录成功率较低

⚠️ **下载限制**:
- 非会员下载限速
- 大文件需要客户端下载
- 部分文件不支持网页下载

⚠️ **容量限制**:
- 免费用户容量有限
- 超容量后只能下载不能上传

## 🆕 成功登录百度网盘的方法（2026-02-09 实测）

### 环境要求
```bash
# 需要安装 xvfb（虚拟显示器）
sudo apt-get install xvfb

# 需要安装 Chromium 浏览器
sudo apt-get install chromium-browser
```

### 启动带 xvfb 的浏览器（关键步骤）
```bash
# 使用 xvfb-run 启动浏览器（重要！headless 模式无法完成扫码登录）
xvfb-run --auto-servernum chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile \
  --start-fullscreen
```

### 为什么需要 xvfb？
- **Headless 模式**：无法显示二维码，扫码登录会失败
- **xvfb 模式**：提供虚拟显示，二维码能正常显示
- 扫码登录后，cookies 会保存在 user-data-dir 中，后续无需重新登录

### 登录流程
1. **启动浏览器**（带 xvfb）
2. **打开百度网盘**：访问 `https://pan.baidu.com`
3. **点击"去登录"** 按钮
4. **获取登录二维码**：
   - 点击"扫码登录"标签
   - 二维码会自动显示
5. **用手机扫码**：
   - 打开百度网盘 App
   - 点击首页右上角相机图标
   - 扫描电脑屏幕上的二维码
6. **确认登录**：手机上点击确认
7. **自动跳转**：浏览器会自动跳转到网盘首页

### 登录成功后的操作
登录成功后，cookies 会保存在 user-data-dir 中，后续可以直接访问：
```json
{
  "action": "navigate",
  "targetUrl": "https://pan.baidu.com/disk/home"
}
```

### 常见问题

**Q: 扫码后页面没反应？**
A: 等几秒，浏览器会自动跳转。如果没跳转，刷新页面。

**Q: 需要重新登录吗？**
A: 不需要，cookies 已保存在配置目录中。

**Q: 头像没显示但能操作文件？**
A: 正常现象，不影响文件操作。

**Q: 提示登录过期？**
A: 删除 cookies 重新登录：
```bash
rm -rf /tmp/chrome-profile
# 重新启动浏览器
```

## 替代方案

如果百度网盘网页版操作受限，可以考虑：

1. **使用百度网盘客户端**
   - 支持更多功能
   - 下载更稳定

2. **使用第三方下载工具**
   - 某些工具可以绕过限速

3. **命令行工具**（如果有）
   - 百度网盘官方暂无 Linux CLI 工具

## 完整操作示例

### 下载分享链接示例

```json
// Step 1: 打开分享链接
{
  "action": "navigate",
  "targetUrl": "https://pan.baidu.com/s/1example"
}
```

```json
// Step 2: 等待页面加载
{
  "action": "act",
  "request": {
    "kind": "wait",
    "timeMs": 3000
  }
}
```

```json
// Step 3: 截图查看页面结构
{ "action": "screenshot" }
```

```json
// Step 4: 查看页面元素，找到提取码输入框
{ "action": "snapshot" }
```

```json
// Step 5: 如果需要输入提取码
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "extract_code_input_ref",
    "text": "提取码"
  }
}
```

```json
// Step 6: 点击提取按钮
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "extract_button_ref"
  }
}
```

```json
// Step 7: 等待文件加载
{
  "action": "act",
  "request": {
    "kind": "wait",
    "timeMs": 2000
  }
}
```

```json
// Step 8: 点击下载
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "download_button_ref"
  }
}
```

## 相关技能
- `browser` - 浏览器基础操作
- `feishu-drive` - 飞书云盘管理（类似操作逻辑）
