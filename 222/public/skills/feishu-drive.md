# Feishu 云盘管理

## 何时调用
当用户提及以下内容时激活：
- "云盘"、"云文档"、"drive"、"文件夹"
- "查看文件"、"列出文件"、"创建文件夹"
- "移动文件"、"删除文件"

## 工具名称
`feishu_drive`

## 支持的操作

### 1. 列出文件夹内容
```
{ "action": "list" }
```
根目录

```
{ "action": "list", "folder_token": "fldcnXXX" }
```
指定文件夹

### 2. 获取文件信息
```
{ "action": "info", "file_token": "ABC123", "type": "docx" }
```
⚠️ 文件必须在云盘根目录或已浏览过的文件夹中

### 3. 创建文件夹
```
{ "action": "create_folder", "name": "新文件夹" }
```

```
{
  "action": "create_folder",
  "name": "子文件夹",
  "folder_token": "fldcnXXX"  # 父文件夹
}
```

### 4. 移动文件
```
{
  "action": "move",
  "file_token": "ABC123",
  "type": "docx",
  "folder_token": "fldcnXXX"
}
```

### 5. 删除文件
```
{ "action": "delete", "file_token": "ABC123", "type": "docx" }
```

## 文件类型
| 类型 | 说明 |
|-----|------|
| `doc` | 旧版文档 |
| `docx` | 新版文档 |
| `sheet` | 电子表格 |
| `bitable` | 多维表格 |
| `folder` | 文件夹 |
| `file` | 上传的文件 |
| `mindnote` | 思维导图 |
| `shortcut` | 快捷方式 |

## 链接提取
从 URL `https://xxx.feishu.cn/drive/folder/ABC123` 提取 `folder_token` = `ABC123`

## ⚠️ 重要限制
- **机器人没有根文件夹**：bot 使用 `tenant_access_token`，没有"我的空间"
- 必须先**手动创建文件夹并分享给机器人**，机器人才能在其中操作
- `create_folder` 不指定 `folder_token` 会报 400 错误

## 使用示例

**用户说**："查看云盘根目录"

**调用**：`feishu_drive { "action": "list" }`

**用户说**："在文件夹 ABC123 里创建 '项目文档' 子文件夹"

**调用**：
```
{
  "action": "create_folder",
  "name": "项目文档",
  "folder_token": "ABC123"
}
```

## 配置要求
```yaml
channels:
  feishu:
    tools:
      drive: true  # 默认开启
```

