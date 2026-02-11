#!/bin/bash

# GitHub 自动备份脚本
# 功能：自动提交并推送工作目录到GitHub
# 频率：每天自动执行

set -e

# 配置
WORKSPACE_DIR="/home/lang/.openclaw/workspace"
BACKUP_TOKEN_FILE="${WORKSPACE_DIR}/config/github-token.md"
LOG_FILE="${WORKSPACE_DIR}/logs/backup.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
    echo -e "$1"
}

# 检查Token
check_token() {
    if [ ! -f "$BACKUP_TOKEN_FILE" ]; then
        log "${RED}❌ Token文件不存在: $BACKUP_TOKEN_FILE${NC}"
        return 1
    fi
    
    # 从文件提取Token
    TOKEN=$(grep "Token" "$BACKUP_TOKEN_FILE" | head -1 | awk '{print $2}')
    
    if [ -z "$TOKEN" ]; then
        log "${RED}❌ 无法从文件提取Token${NC}"
        return 1
    fi
    
    # 验证Token是否有效
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $TOKEN" https://api.github.com/user)
    
    if [ "$RESPONSE" != "200" ]; then
        log "${RED}❌ Token无效或已过期 (HTTP $RESPONSE)${NC}"
        log "${YELLOW}📝 请更新Token，参考文件: $BACKUP_TOKEN_FILE${NC}"
        return 1
    fi
    
    echo "$TOKEN"
}

# 主备份函数
main() {
    log "========================================"
    log "${GREEN}🚀 开始自动备份...${NC}"
    
    cd "$WORKSPACE_DIR"
    
    # 检查Token
    TOKEN=$(check_token) || exit 1
    log "${GREEN}✅ Token验证成功${NC}"
    
    # 配置git使用Token
    git config --global credential.helper store
    echo "https://hklang:$TOKEN@github.com" > ~/.git-credentials
    
    # 配置代理（通过v2rayA）
    git config --global http.proxy "socks5://127.0.0.1:20170"
    git config --global https.proxy "socks5://127.0.0.1:20170"
    
    # 检查是否有变更
    git add -A
    
    # 获取变更状态
    CHANGES=$(git status --porcelain)
    
    if [ -z "$CHANGES" ]; then
        log "${YELLOW}📝 没有新变更，跳过备份${NC}"
        exit 0
    fi
    
    # 提交变更
    COMMIT_MSG="Auto backup $(date +'%Y-%m-%d %H:%M:%S')"
    git commit -m "$COMMIT_MSG"
    
    log "${GREEN}✅ 提交成功: $COMMIT_MSG${NC}"
    
    # 推送到GitHub
    log "${GREEN}☁️ 推送到GitHub...${NC}"
    
    if git push origin master; then
        log "${GREEN}✅ 推送成功！${NC}"
        log "📂 仓库: https://github.com/hklang/Openclaw"
    else
        log "${RED}❌ 推送失败${NC}"
        log "${YELLOW}📝 可能是网络问题，稍后重试${NC}"
        exit 1
    fi
    
    log "${GREEN}🎉 备份完成！${NC}"
}

# 执行
main
