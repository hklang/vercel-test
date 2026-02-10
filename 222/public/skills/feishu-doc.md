# Feishu 文档操作

## 何时调用
当用户提及以下内容时激活：
- "飞书文档"、"feishu doc"、"docx"
- 发送了飞书文档链接（包含 `docx/xxx`）
- "读取文档"、"创建文档"、"编辑文档"

## 工具名称
`feishu_doc`

## 支持的操作

### 1. 读取文档
```
{ "action": "read", "doc_token": "ABC123def" }
```
返回：文档标题、纯文本内容、块统计信息

### 2. 写入文档（替换全部）
```
{
  "action": "write",
  "doc_token": "ABC123def",
  "content": "# 新标题\n\nMarkdown 内容..."
}
```
⚠️ 不支持 Markdown 表格

### 3. 追加内容
```
{
  "action": "append",
  "doc_token": "ABC123def",
  "content": "追加的文本"
}
```

### 4. 创建文档
```
{ "action": "create", "title": "新文档标题" }
```

### 5. 列出所有块（表格、图片等）
```
{ "action": "list_blocks", "doc_token": "ABC123def" }
```

### 6. 更新特定块
```
{
  "action": "update_block",
  "doc_token": "ABC123def",
  "block_id": "doxcnXXX",
  "content": "新文本"
}
```

### 7. 删除块
```
{ "action": "delete_block", "doc_token": "ABC123def", "block_id": "doxcnXXX" }
```

## 链接提取
从 URL `https://xxx.feishu.cn/docx/ABC123def` 提取 `doc_token` = `ABC123def`

## 使用示例

**用户说**："读取这个文档 https://xxx.feishu.cn/docx/ABC123def"

**调用流程**：
1. 提取 doc_token: `ABC123def`
2. `feishu_doc { "action": "read", "doc_token": "ABC123def" }`
3. 返回内容给用户

**用户说**："在文档 ABC123def 后面追加 '测试完成'"

**调用流程**：
1. `feishu_doc { "action": "append", "doc_token": "ABC123def", "content": "测试完成" }`
2. 返回执行结果

## 配置要求
```yaml
channels:
  feishu:
    tools:
      doc: true  # 默认开启
```

