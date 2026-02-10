# GitHub 私有仓库备份指南

## 场景
将工作目录备份到 GitHub 私有仓库，防止数据丢失。

## 前置条件
- GitHub 账号
- Personal Access Token (PAT)

## 步骤

### 1️⃣ 生成 Personal Access Token

1. 打开：https://github.com/settings/tokens
2. 点击 **「Generate new token (classic)」**
3. 填写信息：
   - **Note**: `workspace-backup`
   - **Expiration**: `No expiration`（永不过期）
   - 勾选 **`repo`** 权限（完整勾选）
4. 点击 **「Generate token」**
5. **复制Token**（形如 `ghp_xxxxxxxxxxxx`）

### 2️⃣ 创建仓库（网页操作）

1. 打开：https://github.com/new
2. **Repository name**: `workspace-backup`
3. **Description**: `工作目录备份`
4. **Private**: ✅ 勾选（私有）
5. **不勾选** README、.gitignore 等
6. 点击 **「Create repository」**

### 3️⃣ 本地初始化并推送

```bash
cd /home/lang/.openclaw/workspace

# 初始化Git仓库（如果还未初始化）
git init
git add .
git commit -m "Initial backup $(date +'%Y-%m-%d')"

# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/workspace-backup.git

# 首次推送（使用Token作为密码）
git push -u origin main
```

### 4️⃣ 后续更新

```bash
# 查看状态
git status

# 提交更新
git add -A
git commit -m "Backup $(date +'%Y-%m-%d %H:%M')"

# 推送到GitHub
git push
```

## 常见问题

### Q: 推送时提示认证失败？

**A**: 使用 Personal Access Token 作为密码，而不是GitHub登录密码。

### Q: GitHub强制要求2FA？

**A**: Token就是认证方式，无需2FA。

### Q: 想用命令行创建仓库？

**A**: 需要安装 GitHub CLI (`gh`)，或使用API：

```bash
# 安装 gh
curl -fsSL https://cli.github.com/packages/linuxbrew_footer.sh | sudo bash
sudo apt install gh

# 登录
gh auth login

# 创建仓库
gh repo create workspace-backup --private --source=. --push
```

## 自动备份（可选）

创建定时任务：

```bash
# 编辑 crontab
crontab -e

# 添加（每天凌晨2点自动备份）
0 2 * * * cd /home/lang/.openclaw/workspace && git add -A && git commit -m "Auto backup $(date +'\%Y-\%m-\%d \%H:\%M')" && git push
```

## 文件排除（.gitignore）

```gitignore
# Git忽略规则
.venv/
venv/
__pycache__/
*.pyc
.env
node_modules/
.DS_Store
```

## 相关文件

- **公共文档**: `public/skills/v2rayA.md`
- **工作目录**: `/home/lang/.openclaw/workspace/`

---

**最后更新**: 2026-02-10
