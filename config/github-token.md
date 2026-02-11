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
- **GitHub推送**: ⏳ 待网络恢复后重试
- **提交记录**: `Initial backup 2026-02-10 23:12:17`
- **文件数量**: 406 个文件

## 后续操作

网络恢复后执行：
```bash
cd /home/lang/.openclaw/workspace
git push -u origin master
```

---

**最后更新**: 2026-02-10
