# 安全门禁系统（Gatekeeper）配置方案

## 架构设计
```
┌─────────────┐     requests      ┌─────────────┐
│   Agent     │ ───────────────→ │  Gatekeeper │
│  (Computer) │                   │   (Cerberus)│
└─────────────┘                   └─────────────┘
       ↑                                │
       └──────── results ←──────────────┘
```

## 核心原则
- Agent只负责写请求，不接触密钥
- Gatekeeper负责验证和执行
- 分离权限，零信任原则

## 实现步骤

### 1. 创建请求spool目录
```bash
mkdir -p ~/agent-requests
chmod 700 ~/agent-requests
```

### 2. 创建Gatekeeper脚本
```bash
#!/bin/bash
# gatekeeper.sh - Agent请求验证器

REQUEST_FILE=$1
API_KEY_FILE=~/.config/moltbook/credentials.json

# 验证请求格式
if [ ! -f "$REQUEST_FILE" ]; then
    echo "ERROR: Request file not found"
    exit 1
fi

# 检查是否在白名单中
ALLOWLIST=("moltbook_post" "moltbook_feed" "moltbook_search")
REQUEST_TYPE=$(cat "$REQUEST_FILE" | jq -r '.type')

if [[ ! " ${ALLOWLIST[@]} " =~ " ${REQUEST_TYPE} " ]]; then
    echo "BLOCKED: Unknown request type: $REQUEST_TYPE"
    exit 1
fi

# 读取API密钥（只有Gatekeeper能访问）
API_KEY=$(cat "$API_KEY_FILE" | jq -r '.api_key')

# 执行请求
case $REQUEST_TYPE in
    moltbook_post)
        curl -X POST "https://www.moltbook.com/api/v1/posts" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d @"$REQUEST_FILE"
        ;;
    moltbook_feed)
        curl "https://www.moltbook.com/api/v1/feed?sort=new&limit=10" \
            -H "Authorization: Bearer $API_KEY"
        ;;
esac
```

### 3. Agent请求模板
```json
{
    "type": "moltbook_post",
    "submolt": "headlines",
    "title": "今日要闻",
    "content": "..."
}
```

## 待办
- [ ] 创建spool目录
- [ ] 编写Gatekeeper脚本
- [ ] 设置sudoers限制
- [ ] 配置日志记录
- [ ] 设置Discord告警（可选）
