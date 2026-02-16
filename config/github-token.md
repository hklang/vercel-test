# GitHub Token 配置

## Token 信息

- **用户名**: hklang
- **Token**: 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
- **权限**: repo (完整仓库访问)
- **创建时间**: 2026-02-10
- **过期时间**: 无 (No expiration)

## 用途

用于推送代码到 GitHub 私有/公开仓库。

## 使用方法

```bash
# 方法1: 在URL中包含Token
git remote set-url origin "https://hklang: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@github.com/hklang/Openclaw.git"
git push -u origin master

# 方法2: 使用 git credential
git config --global credential.helper store
# 第一次push时会提示输入用户名和Token，后续会自动保存
```

## 关联仓库

- `hklang/Openclaw` - 工作目录备份 (公共仓库)

## 安全提醒

⚠️ **不要泄露此Token！**
- Token 相当于密码，具有完整仓库访问权限
- 不要分享给他人
- 不要提交到代码仓库

## 备份状态

- **本地提交**: ✅ 完成
- **GitHub推送**: ✅ 已修复token
- **最后推送**: 2026-02-16 23:31:44
- **提交记录**: `Backup 2026-02-16 23:31:44`

## 后续操作

网络恢复后执行：
```bash
cd /home/lang/.openclaw/workspace
git push -u origin master
```

---

**最后更新**: 2026-02-16
