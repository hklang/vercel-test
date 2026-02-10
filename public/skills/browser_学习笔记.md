# 浏览器操作技能笔记

## 核心概念

### 1. CDP (Chrome DevTools Protocol)
- OpenClaw通过CDP协议控制Chrome浏览器
- 端口：默认9222
- URL: http://127.0.0.1:9222

### 2. 元素引用 (ref)
- snapshot返回DOM树，每个元素有唯一ref
- ref格式：e123（数字递增）
- 操作元素必须用ref，不能用XPath或CSS

### 3. 操作流程
```
打开网页 → snapshot获取DOM → act操作元素 → screenshot确认
```

---

## 常用操作模板

### 场景1: 打开网页并截图
```json
{
  "action": "navigate",
  "targetUrl": "https://www.baidu.com"
}
```
```json
{ "action": "screenshot" }
```

### 场景2: 点击按钮
```json
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e21"
  }
}
```

### 场景3: 输入文本
```json
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "e50",
    "text": "要输入的内容"
  }
}
```

### 场景4: 滚动页面
```json
{
  "action": "act",
  "request": {
    "kind": "scroll",
    "x": 0,
    "y": 500
  }
}
```

### 场景5: 执行JavaScript
```json
{
  "action": "act",
  "request": {
    "kind": "evaluate",
    "script": "document.title"
  }
}
```

---

## 实战示例

### 登录GitHub
```json
// 1. 打开登录页
{
  "action": "navigate",
  "targetUrl": "https://github.com/login"
}

// 2. 获取页面快照
{ "action": "snapshot" }

// 3. 输入用户名
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "e23",
    "text": "bklang@qq.com"
  }
}

// 4. 输入密码
{
  "action": "act",
  "request": {
    "kind": "type",
    "ref": "e45",
    "text": "your_password"
  }
}

// 5. 点击登录
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e67"
  }
}

// 6. 截图确认
{ "action": "screenshot" }
```

### 搜索并打开链接
```json
// 1. 导航到搜索页
{
  "action": "navigate",
  "targetUrl": "https://github.com/search?q=七乐彩+数据"
}

// 2. 获取页面结构
{ "action": "snapshot" }

// 3. 点击搜索结果
{
  "action": "act",
  "request": {
    "kind": "click",
    "ref": "e123"
  }
}
```

---

## 常见问题与解决

### Q1: 元素找不到
**原因**: 页面未完全加载
**解决**: 
```json
{
  "action": "act",
  "request": {
    "kind": "wait",
    "ref": "e123"
  }
}
```

### Q2: 点击无效
**原因**: 元素被遮挡或不可见
**解决**: 先滚动到元素可见
```json
{
  "action": "act",
  "request": {
    "kind": "scroll",
    "x": 0,
    "y": 500
  }
}
```

### Q3: CDP连接超时
**原因**: 浏览器进程崩溃
**解决**: 
```bash
pkill -f "chromium.*remote-debugging"
```
然后重新启动

### Q4: 验证码无法通过
**原因**: 滑块验证需要人类操作
**解决**: 手动完成验证，或使用打码服务

---

## 最佳实践

1. **先snapshot再操作** - 必须先获取DOM结构
2. **使用ref引用元素** - 不要用XPath或CSS选择器
3. **操作后截图确认** - 验证操作是否成功
4. **设置等待时间** - 页面加载需要时间
5. **复用浏览器实例** - 避免频繁启动/停止

---

## 相关资源

- OpenClaw文档: https://docs.openclaw.ai/
- Discord社区: https://discord.com/invite/clawd
- browser.md技能: /home/lang/.openclaw/workspace/public/skills/browser.md

---

## 我的总结

### 学到的关键点：
1. **必须先snapshot** - 所有操作基于DOM树
2. **ref是核心** - 操作元素的唯一标识
3. **act是万能操作** - click/type/scroll/evaluate/wait都通过act
4. **browser工具≠Python playwright** - 要用内置的browser工具

### 改进方向：
1. 优先使用browser工具
2. 每次操作前先snapshot
3. 用ref引用元素
4. 重要操作后截图确认

---

最后更新: 2026-02-09
