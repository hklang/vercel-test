# Feishu 知识库（Wiki）

## 何时调用
当用户提及以下内容时激活：
- "wiki"、"知识库"、"知识空间"
- "页面"、"node"、"wikicn"
- 发送了 wiki 链接（包含 `wiki/xxx`）

## 工具名称
`feishu_wiki`

## 支持的操作

### 1. 列出所有知识空间
```
{ "action": "spaces" }
```

### 2. 列出节点（页面）
```
{ "action": "nodes", "space_id": "7xxx" }
```
指定父节点：
```
{
  "action": "nodes",
  "space_id": "7xxx",
  "parent_node_token": "wikcnXXX"
}
```

### 3. 获取节点详情
```
{ "action": "get", "token": "ABC123def" }
```
返回：`node_token`、`obj_token`、`obj_type` 等

### 4. 创建节点（页面）
```
{ "action": "create", "space_id": "7xxx", "title": "新页面" }
```

指定类型和父节点：
```
{
  "action": "create",
  "space_id": "7xxx",
  "title": "数据表",
  "obj_type": "sheet",
  "parent_node_token": "wikcnXXX"
}
```

类型可选值：`docx`(默认)、`sheet`、`bitable`、`mindnote`、`file`、`doc`、`slides`

### 5. 移动节点
```
{ "action": "move", "space_id": "7xxx", "node_token": "wikcnXXX" }
```

移动到其他位置：
```
{
  "action": "move",
  "space_id": "7xxx",
  "node_token": "wikcnXXX",
  "target_space_id": "7yyy",
  "target_parent_token": "wikcnYYY"
}
```

### 6. 重命名节点
```
{
  "action": "rename",
  "space_id": "7xxx",
  "node_token": "wikcnXXX",
  "title": "新标题"
}
```

## 链接提取
从 URL `https://xxx.feishu.cn/wiki/ABC123def` 提取 `token` = `ABC123def`

## Wiki ↔ Doc 工作流

Wiki 页面本质上是文档，编辑需要两步：

1. **获取文档 token**：
   ```
   feishu_wiki { "action": "get", "token": "wiki_token" }
   → 返回 obj_token
   ```

2. **读取/写入文档**：
   ```
   feishu_doc { "action": "read", "doc_token": "obj_token" }
   feishu_doc { "action": "write", "doc_token": "obj_token", "content": "..." }
   ```

## 使用示例

**用户说**："查看我的知识库"

**调用**：`feishu_wiki { "action": "spaces" }`

**用户说**："创建一个新页面叫 '会议记录'"

**调用**：
```
{
  "action": "create",
  "space_id": "7xxx",  # 先用 spaces 获取
  "title": "会议记录"
}
```

**用户说**："编辑 wiki 页面 ABC123def 的内容"

**调用**：
```
# 第一步：获取 obj_token
feishu_wiki { "action": "get", "token": "ABC123def" }
→ 返回 obj_token: "doxcnYYY"

# 第二步：读取当前内容
feishu_doc { "action": "read", "doc_token": "doxcnYYY" }

# 第三步：写入新内容
feishu_doc { "action": "write", "doc_token": "doxcnYYY", "content": "新内容..." }
```

## 配置要求
```yaml
channels:
  feishu:
    tools:
      wiki: true   # 默认开启
      doc: true    # 必须开启（wiki 内容通过 doc 操作）
```

