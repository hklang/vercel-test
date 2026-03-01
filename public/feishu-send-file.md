# 飞书发送文件（音频/视频/文档）方法

## 关键发现

飞书发送文件使用 `media` 参数，不是 `filePath`！

## 正确方法

```javascript
message({
  action: "send",
  channel: "feishu",
  target: "群ID或用户ID",
  message: "文字说明",
  media: "/path/to/file.mp3"  // 本地文件路径
})
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| channel | 固定为 feishu | feishu |
| target | 群ID或用户ID | oc_xxx 或 user:ou_xxx |
| message | 文字说明（可选） | "这是音频文件" |
| media | 本地文件绝对路径 | /home/lang/xxx.mp3 |

## 常见问题

### 1. target格式
- 群ID：以 `oc_` 开头，如 `oc_0ad3b06c089701c068e0091c0f6fc395`
- 用户ID：以 `user:` 开头，如 `user:ou_xxx`
- 群ID加前缀：`chat:` 如 `chat:oc_xxx`

### 2. 文件路径
- 必须用本地绝对路径
- 路径不能有空格（如果有空格需要转义）
- 文件必须存在且有内容

### 3. 目标ID获取
- 私聊：用 `user:用户open_id`
- 群聊：用 `oc_群ID`

## 错误示例

❌ **错误1：用filePath参数**
```javascript
// 错误！
message({
  action: "send",
  channel: "feishu",
  target: "oc_xxx",
  message: "文件",
  filePath: "/path/to/file.mp3"  // 这是错的！
})
```

❌ **错误2：target格式错误**
```javascript
// 错误！
message({
  action: "send",
  channel: "feishu",
  target: "g-oc_xxx",  // 不需要加前缀
  media: "/path/to/file.mp3"
})
```

## 成功案例

### 发送音频
```javascript
message({
  action: "send",
  channel: "feishu",
  target: "oc_0ad3b06c089701c068e0091c0f6fc395",
  message: "📢 滥竽充数旁白试听",
  media: "/home/lang/.openclaw/workspace/video/滥竽充数/旁白配音.mp3"
})
```

### 发送图片
```javascript
message({
  action: "send",
  channel: "feishu",
  target: "oc_7873da17e98fa210dff4161ca6defd46",
  message: "七乐彩分析",
  media: "/home/lang/.openclaw/workspace/caipiao/analyze.png"
})
```

## 常见文件格式支持

| 类型 | 支持格式 | 示例 |
|------|----------|------|
| 音频 | mp3, wav, m4a | .mp3 |
| 视频 | mp4, mov | .mp4 |
| 图片 | png, jpg, jpeg, gif | .png |
| 文档 | pdf, doc, docx | .pdf |

## 文件大小限制

- 图片：建议 < 5MB
- 音频：建议 < 10MB  
- 视频：建议 < 20MB
- 文档：建议 < 10MB

---

*创建时间：2026-03-01*
