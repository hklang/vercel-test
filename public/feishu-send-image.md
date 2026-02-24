# 飞书发送图片方法

## 方法总结

通过今天的实践，找到了在飞书中发送图片的正确方法：

### 1. 使用 `message` 工具的 `media` 参数

```javascript
message({
  action: "send",
  channel: "feishu",
  target: "群ID或用户ID",
  message: "图片描述文字",
  media: "/path/to/image.png"  // 本地图片路径
})
```

### 2. 关键要点

1. **必须指定 `target` 参数** - 飞书需要明确的目标（群ID或用户ID）
2. **使用本地绝对路径** - 如 `/home/lang/.openclaw/workspace/caipiao/analyze.png`
3. **图片格式支持** - PNG、JPG、JPEG等常见格式
4. **消息内容可选** - 可以只发送图片，也可以附带文字描述

### 3. 错误示例

❌ **错误1：缺少target参数**
```javascript
// 会报错：Action send requires a target.
message({
  action: "send",
  channel: "feishu",
  message: "图片",
  media: "/path/to/image.png"
})
```

❌ **错误2：使用markdown语法**
```javascript
// 飞书不支持markdown图片语法
message({
  action: "send",
  channel: "feishu",
  target: "群ID",
  message: "![图片](MEDIA:/path/to/image.png)"  // 不会显示图片
})
```

### 4. 成功示例

✅ **正确方法**
```javascript
// 成功发送图片到飞书群
message({
  action: "send",
  channel: "feishu",
  target: "oc_7873da17e98fa210dff4161ca6defd46",
  message: "发送一张七乐彩分析系统的图片：",
  media: "/home/lang/.openclaw/workspace/caipiao/analyze.png"
})
```

### 5. 获取图片路径的方法

1. **查找现有图片**
```bash
find /home/lang/.openclaw/workspace -name "*.png" -o -name "*.jpg" -o -name "*.jpeg"
```

2. **浏览器截图**
```javascript
browser({
  action: "screenshot",
  targetId: "浏览器标签ID",
  type: "png",
  fullPage: false
})
// 返回：MEDIA:/home/lang/.openclaw/media/browser/xxx.png
```

### 6. 实际测试结果

- **测试时间**: 2026-02-25
- **测试群**: `oc_7873da17e98fa210dff4161ca6defd46`
- **成功发送**: 七乐彩分析系统图片 (`/home/lang/.openclaw/workspace/caipiao/analyze.png`)
- **消息ID**: `om_x100b56e918ef80a0b292069d82379ef`

### 7. 注意事项

1. 飞书图片发送是同步的，会立即显示在聊天中
2. 图片大小有限制，建议不要超过5MB
3. 可以一次发送多张图片（使用`mediaUrls`数组）
4. 图片发送后会有mediaUrl返回，可用于后续引用

---

## 学习过程记录

### 遇到的问题

1. **第一次尝试**: 使用浏览器截图，但发送时缺少`target`参数导致失败
2. **第二次尝试**: 使用markdown语法，飞书不支持这种格式
3. **第三次尝试**: 使用本地图片路径并指定`target`，成功发送

### 关键发现

- 飞书的`message`工具需要明确指定`target`参数
- 不支持markdown图片语法，必须使用`media`参数
- 本地绝对路径可以直接使用

### 适用场景

1. 发送工作文档截图
2. 分享系统分析结果图表
3. 发送浏览器操作截图
4. 分享项目进度截图

---

*文档创建时间: 2026-02-25*
*创建者: OpenClaw 助手*