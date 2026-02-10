# Feishu 权限管理

## 何时调用
当用户提及以下内容时激活：
- "权限"、"分享"、"协作者"、"成员"
- "设置权限"、"添加成员"、"移除成员"、"查看权限"

## 工具名称
`feishu_perm`

## ⚠️ 敏感操作
此工具默认**禁用**，因为权限管理涉及敏感操作。需要时需手动启用。

## 支持的操作

### 1. 列出协作者
```
{
  "action": "list",
  "token": "ABC123",
  "type": "docx"
}
```
返回：成员类型、ID、权限级别、名称

### 2. 添加协作者
```
{
  "action": "add",
  "token": "ABC123",
  "type": "docx",
  "member_type": "email",
  "member_id": "user@example.com",
  "perm": "edit"
}
```

### 3. 移除协作者
```
{
  "action": "remove",
  "token": "ABC123",
  "type": "docx",
  "member_type": "email",
  "member_id": "user@example.com"
}
```

## 资源类型 (type)
| 类型 | 说明 |
|-----|------|
| `doc` | 旧版文档 |
| `docx` | 新版文档 |
| `sheet` | 电子表格 |
| `bitable` | 多维表格 |
| `folder` | 文件夹 |
| `file` | 上传的文件 |
| `wiki` | Wiki 节点 |
| `mindnote` | 思维导图 |

## 成员类型 (member_type)
| 类型 | 说明 |
|-----|------|
| `email` | 邮箱地址 |
| `openid` | 用户 open_id |
| `userid` | 用户 user_id |
| `unionid` | 用户 union_id |
| `openchat` | 群聊 open_id |
| `opendepartmentid` | 部门 open_id |

## 权限级别 (perm)
| 级别 | 说明 |
|-----|------|
| `view` | 仅查看 |
| `edit` | 可以编辑 |
| `full_access` | 完全访问（可管理权限） |

## 使用示例

**用户说**："查看文档 ABC123def 的协作者列表"

**调用**：
```
{
  "action": "list",
  "token": "ABC123def",
  "type": "docx"
}
```

**用户说**："把文档 ABC123def 的编辑权限给 alice@company.com"

**调用**：
```
{
  "action": "add",
  "token": "ABC123def",
  "type": "docx",
  "member_type": "email",
  "member_id": "alice@company.com",
  "perm": "edit"
}
```

**用户说**："从文件夹 ABC123 移除 bob@company.com"

**调用**：
```
{
  "action": "remove",
  "token": "ABC123",
  "type": "folder",
  "member_type": "email",
  "member_id": "bob@company.com"
}
```

## 配置要求
```yaml
channels:
  feishu:
    tools:
      perm: true  # 默认关闭，需要时手动启用
```

## 所需权限
- `drive:permission`

