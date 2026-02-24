# 发送图片到飞书聊天指南

## 概述
本文档详细记录如何通过OpenClaw将图片发送到飞书聊天对话框，包括截图、浏览器截图、本地图片文件等多种方式。

## 方法1：使用`message`工具发送图片（最常用）

### 基本语法
```javascript
{
  "action": "send",
  "channel": "feishu",
  "message": "图片说明文字",
  "media": "MEDIA:图片路径"
}
```

### 实际案例

#### 案例1：发送浏览器截图
```javascript
// 1. 先使用browser工具截图
{
  "action": "browser",
  "action": "screenshot",
  "targetId": "页面ID",
  "fullPage": true
}
// 返回：MEDIA:/home/lang/.openclaw/media/browser/e5a81687-f293-4855-8d8d-b7f7bb29142a.png

// 2. 发送截图到聊天
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "浏览器截图",
  "media": "MEDIA:/home/lang/.openclaw/media/browser/e5a81687-f293-4855-8d8d-b7f7bb29142a.png"
}
```

#### 案例2：发送本地图片文件
```javascript
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "本地图片",
  "media": "/home/lang/.openclaw/workspace/public/images/example.png"
}
```

#### 案例3：发送多张图片
```javascript
// 可以多次调用message工具发送多张图片
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "截图1",
  "media": "MEDIA:/path/to/image1.png"
}

{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "截图2",
  "media": "MEDIA:/path/to/image2.png"
}
```

## 方法2：使用`browser`工具截图并发送

### 完整流程示例

#### 步骤1：打开网页并截图
```javascript
// 1. 打开网页
{
  "action": "browser",
  "action": "open",
  "targetUrl": "https://www.baidu.com",
  "profile": "mychrome"
}
// 返回：{"targetId": "A8453ABF2654BBEDE03A0358BF04D883", ...}

// 2. 截图
{
  "action": "browser",
  "action": "screenshot",
  "targetId": "A8453ABF2654BBEDE03A0358BF04D883",
  "fullPage": true
}
// 返回：MEDIA:/home/lang/.openclaw/media/browser/f2034ca0-8898-4dcf-a23e-d79a3e259a0b.png
```

#### 步骤2：发送截图
```javascript
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "百度首页截图",
  "media": "MEDIA:/home/lang/.openclaw/media/browser/f2034ca0-8898-4dcf-a23e-d79a3e259a0b.png"
}
```

## 方法3：使用`canvas`工具截图并发送

### 适用于节点屏幕截图
```javascript
// 1. 获取节点屏幕截图
{
  "action": "canvas",
  "action": "snapshot",
  "node": "节点名称",
  "outputFormat": "png"
}
// 返回：MEDIA:路径

// 2. 发送截图
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "节点屏幕截图",
  "media": "MEDIA:返回的路径"
}
```

## 方法4：使用`nodes`工具摄像头截图

### 适用于设备摄像头拍照
```javascript
// 1. 摄像头拍照
{
  "action": "nodes",
  "action": "camera_snap",
  "node": "设备名称",
  "facing": "front"  // 或 "back"
}
// 返回：MEDIA:路径

// 2. 发送照片
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "摄像头照片",
  "media": "MEDIA:返回的路径"
}
```

## 图片路径说明

### OpenClaw媒体目录结构
```
/home/lang/.openclaw/media/
├── browser/          # 浏览器截图
│   ├── e5a81687-f293-4855-8d8d-b7f7bb29142a.png
│   └── f2034ca0-8898-4dcf-a23e-d79a3e259a0b.png
├── canvas/           # 画布截图
├── nodes/            # 节点截图和摄像头照片
└── tts/              # 语音文件
```

### MEDIA:前缀的重要性
- **必须使用**：`MEDIA:/path/to/image.png`
- **不能省略**：MEDIA:前缀告诉系统这是媒体文件
- **自动处理**：系统会自动上传到飞书并生成可访问的URL

## 实际应用场景

### 场景1：验证Cloudflare人机验证结果
```javascript
// 用户要求：验证cf.2hg.com并返回截图

// 1. 打开验证页面
{
  "action": "browser",
  "action": "open",
  "targetUrl": "https://cf.2hg.com/?action=mc",
  "profile": "mychrome"
}

// 2. 等待验证通过并截图
{
  "action": "browser",
  "action": "screenshot",
  "targetId": "页面ID",
  "fullPage": true
}

// 3. 发送验证结果截图
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "Cloudflare验证已通过，页面显示'it works'",
  "media": "MEDIA:/home/lang/.openclaw/media/browser/xxx.png"
}
```

### 场景2：发送学习文档目录截图
```javascript
// 用户要求：学习public文件并发送截图

// 1. 打开本地目录
{
  "action": "browser",
  "action": "open",
  "targetUrl": "file:///home/lang/.openclaw/workspace/public/skills/",
  "profile": "mychrome"
}

// 2. 截图目录内容
{
  "action": "browser",
  "action": "screenshot",
  "targetId": "页面ID",
  "fullPage": true
}

// 3. 发送目录截图
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "public/skills目录内容",
  "media": "MEDIA:/home/lang/.openclaw/media/browser/xxx.png"
}
```

### 场景3：发送多步骤操作截图
```javascript
// 用户要求：演示浏览器操作并发送多个截图

// 步骤1：打开百度
{
  "action": "browser",
  "action": "open",
  "targetUrl": "https://www.baidu.com"
}
{
  "action": "browser",
  "action": "screenshot"
}
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "步骤1：打开百度首页",
  "media": "MEDIA:截图1路径"
}

// 步骤2：搜索内容
{
  "action": "browser",
  "action": "act",
  "request": {"kind": "type", "ref": "搜索框引用", "text": "OpenClaw"}
}
{
  "action": "browser",
  "action": "screenshot"
}
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "步骤2：输入搜索关键词",
  "media": "MEDIA:截图2路径"
}

// 步骤3：点击搜索
{
  "action": "browser",
  "action": "act",
  "request": {"kind": "click", "ref": "搜索按钮引用"}
}
{
  "action": "browser",
  "action": "screenshot"
}
{
  "action": "message",
  "action": "send",
  "channel": "feishu",
  "message": "步骤3：搜索结果页面",
  "media": "MEDIA:截图3路径"
}
```

## 故障排除

### 常见问题及解决方案

#### 问题1：MEDIA:路径无效
**症状**：`media`参数无效，图片未发送
**解决方案**：
- 确认路径以`MEDIA:`开头
- 确认文件确实存在
- 检查文件权限：`ls -la /path/to/image.png`

#### 问题2：图片过大
**症状**：发送失败或超时
**解决方案**：
- 压缩图片：使用`convert`工具减小尺寸
- 截图时设置合适的分辨率
- 分批发送多张小图

#### 问题3：浏览器截图失败
**症状**：`screenshot`返回错误
**解决方案**：
- 确认浏览器页面已加载完成
- 添加等待时间：`{ "action": "act", "request": { "kind": "wait", "timeMs": 3000 } }`
- 检查浏览器状态：`{ "action": "status" }`

#### 问题4：飞书发送失败
**症状**：`message`工具返回错误
**解决方案**：
- 确认channel参数正确：`"channel": "feishu"`
- 确认有发送权限
- 检查网络连接

## 最佳实践

### 1. 图片命名规范
```javascript
// 使用有意义的文件名
const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const filename = `screenshot-${timestamp}.png`;
```

### 2. 图片压缩优化
```bash
# 使用ImageMagick压缩图片
convert input.png -resize 50% -quality 80 output.png
```

### 3. 批量发送管理
```javascript
// 批量发送多张图片
const images = [
  { path: 'MEDIA:/path/to/image1.png', desc: '截图1' },
  { path: 'MEDIA:/path/to/image2.png', desc: '截图2' },
  { path: 'MEDIA:/path/to/image3.png', desc: '截图3' }
];

for (const img of images) {
  await message.send({
    action: 'send',
    channel: 'feishu',
    message: img.desc,
    media: img.path
  });
  await sleep(1000); // 避免发送过快
}
```

### 4. 错误处理
```javascript
try {
  // 截图
  const screenshot = await browser.screenshot({ targetId: pageId });
  
  // 发送
  await message.send({
    action: 'send',
    channel: 'feishu',
    message: '操作截图',
    media: screenshot.mediaPath
  });
  
  console.log('✅ 图片发送成功');
} catch (error) {
  console.error('❌ 图片发送失败:', error.message);
  
  // 发送错误信息
  await message.send({
    action: 'send',
    channel: 'feishu',
    message: `图片发送失败: ${error.message}`
  });
}
```

## 高级技巧

### 1. 自动清理旧图片
```bash
# 清理7天前的浏览器截图
find /home/lang/.openclaw/media/browser/ -name "*.png" -mtime +7 -delete
```

### 2. 图片水印添加
```bash
# 使用ImageMagick添加水印
convert input.png -pointsize 20 -fill white \
  -annotate +10+20 "OpenClaw截图 $(date '+%Y-%m-%d %H:%M')" \
  output.png
```

### 3. 图片格式转换
```bash
# PNG转JPG（减小文件大小）
convert input.png -quality 85 output.jpg
```

### 4. 截图区域选择
```javascript
// 截取特定区域（如果浏览器工具支持）
{
  "action": "browser",
  "action": "screenshot",
  "targetId": "页面ID",
  "clip": { "x": 0, "y": 0, "width": 800, "height": 600 }
}
```

## 学习资源

### 1. 相关文档
- `public/skills/飞书传文件.md` - 文件发送基础
- `public/skills/browser.md` - 浏览器操作指南
- `public/browser-operation-methods.md` - 浏览器操作方法

### 2. 工具参考
- **message工具**：发送消息和媒体文件
- **browser工具**：网页截图和操作
- **canvas工具**：节点屏幕截图
- **nodes工具**：设备摄像头拍照

### 3. 实践案例
- Cloudflare验证截图发送
- 学习文档目录截图发送
- 多步骤操作演示截图

## 总结

### 核心要点
1. **使用`message`工具**：发送图片的主要方式
2. **MEDIA:前缀**：必须包含，标识媒体文件
3. **路径正确性**：确保图片文件存在且可访问
4. **分批发送**：多张图片时避免发送过快

### 工作流程
```
生成图片 → 获取MEDIA路径 → message.send → 飞书聊天
    ↑           ↑              ↑
 browser    screenshot      channel: feishu
 canvas     camera_snap     media: MEDIA:路径
```

### 适用场景
- 验证结果展示
- 学习过程记录
- 操作步骤演示
- 问题排查截图
- 数据可视化展示

---

**创建者**：OpenClaw AI Assistant  
**最后更新**：2026-02-25  
**适用场景**：飞书聊天图片发送、截图分享、操作演示