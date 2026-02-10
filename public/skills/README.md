# 📚 公共技能区

> 所有群聊都可以调用这里的技能

## 🎯 使用方法

在群聊中直接描述你的需求，我就会自动调用相关技能：

- "帮我读取飞书文档" → 调用 `feishu-doc`
- "查看云盘里的文件" → 调用 `feishu-drive`
- "整理知识库" → 调用 `feishu-wiki`
- "设置文档权限" → 调用 `feishu-perm`
- "查看天气" → 调用 `weather`

---

## 🔧 技能列表

### 1️⃣ Feishu 文档操作
- **调用方式**: 提及"飞书文档"、"docx"、"文档链接"
- **功能**: 读取、创建、编辑、追加文档内容
- **位置**: `skills/feishu-doc/README.md`

### 2️⃣ Feishu 云盘管理
- **调用方式**: 提及"云盘"、"文件夹"、"drive"
- **功能**: 浏览文件、创建文件夹、移动、删除
- **位置**: `skills/feishu-drive/README.md`

### 3️⃣ Feishu 知识库
- **调用方式**: 提及"wiki"、"知识库"、"知识空间"
- **功能**: 浏览wiki、创建页面、移动、重命名
- **位置**: `skills/feishu-wiki/README.md`

### 4️⃣ Feishu 权限管理
- **调用方式**: 提及"权限"、"分享"、"协作者"
- **功能**: 查看/添加/移除文档协作者
- **位置**: `skills/feishu-perm/README.md`

### 5️⃣ 天气查询
- **调用方式**: 提及"天气"、"今天天气"
- **功能**: 查询当前天气和预报
- **位置**: `skills/weather/README.md`

### 6️⃣ 浏览器操作
- **调用方式**: 提及"浏览器"、"打开网页"、"访问网址"、"浏览器截图"
- **功能**: 启动浏览器、导航网页、截图、点击输入等
- **位置**: `skills/browser.md`

### 7️⃣ 百度网盘操作
- **调用方式**: 提及"百度网盘"、"百度云"、"pan.baidu.com"、"网盘下载"
- **功能**: 通过浏览器访问百度网盘、下载文件、分享等
- **位置**: `skills/baidupan.md`

### 8️⃣ Moltbook (AI Agents社区)
- **调用方式**: 提及"moltbook"、"Moltbook.com"、"AI agents社区"
- **功能**: 注册、发布帖子、评论、投票、语义搜索、关注其他Agents
- **位置**: `skills/moltbook.md`
- **官网**: https://www.moltbook.com

### 9️⃣ 发送文件到聊天
- **调用方式**: 提及"发送文件"、"传文件"、"发文件到聊天"
- **功能**: 发送本地文件到飞书聊天记录
- **工具**: message工具 + filePath参数
- **位置**: `skills/飞书传文件.md`

---

## 📝 如何添加新技能

1. 在对应技能的 SKILL.md 中添加 description
2. 放在 `public/skills/` 目录下
3. 重启 Gateway 后自动生效

## ❓ 遇到问题

**不会用？**
→ 去 [Moltbook 论坛](https://www.moltbook.com) 学习交流

