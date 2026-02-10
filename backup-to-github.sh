#!/bin/bash

# 工作目录 GitHub 备份脚本
# 用法: bash backup-to-github.sh <username> <token>

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 开始工作目录备份...${NC}"

# 检查参数
if [ -z "$1" ] || [ -z "$2" ]; then
    echo -e "${RED}❌ 用法: $0 <username> <token>${NC}"
    echo -e "${YELLOW}示例: $0 bklang ghp_xxxxxxxxxxxx${NC}"
    exit 1
fi

USERNAME=$1
TOKEN=$2
REPO_NAME="workspace-backup"

# 进入工作目录
cd /home/lang/.openclaw/workspace

echo -e "${GREEN}📁 当前目录: $(pwd)${NC}"

# 检查是否已初始化Git
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📦 初始化Git仓库...${NC}"
    git init
    git add .
    git commit -m "Initial backup $(date +'%Y-%m-%d %H:%M:%S')"
fi

# 设置远程仓库
echo -e "${GREEN}🔗 设置远程仓库...${NC}"
if git remote get-url origin &>/dev/null; then
    echo "远程仓库已存在"
else
    git remote add origin "https://${USERNAME}:${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"
fi

# 提交所有更改
echo -e "${GREEN}📝 提交更改...${NC}"
git add -A
git commit -m "Backup $(date +'%Y-%m-%d %H:%M:%S')" || echo "没有新更改"

# 推送
echo -e "${GREEN}☁️ 推送到GitHub...${NC}"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push -u origin ${BRANCH}

echo -e "${GREEN}✅ 备份完成！${NC}"
echo -e "${YELLOW}📂 仓库地址: https://github.com/${USERNAME}/${REPO_NAME}${NC}"
