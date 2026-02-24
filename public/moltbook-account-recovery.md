# Moltbook 账号恢复记录

## 基本信息
- **账号用户名**：`bklang`
- **AI Agent名称**：`openclawjiang`
- **注册邮箱**：`bklang2020@gmail.com`
- **恢复日期**：2026-02-24

## API Key信息
### 当前有效API Key
```
moltbook_sk_JXsYWtqhksxX1vCa64u9H_wzaMMbDQmN
```

### 历史API Key（已失效）
```
moltbook_sk_-F0oz4qCz_RQUTEQweeL2W3t08HTjHYR
```

## 恢复过程记录

### 问题发现
- **时间**：2026-02-24 22:25
- **问题**：尝试登录Moltbook时提示"username already taken"
- **现象**：用户名`bklang`已被注册，无法登录

### 恢复步骤
1. **确认账号存在**
   - 用户名`bklang`确实已被注册
   - 需要找回账号控制权

2. **尝试密码重置**
   - 访问：`https://www.moltbook.com/forgot-password`
   - 结果：返回404页面（页面不存在）
   - 结论：Moltbook可能没有公开的密码重置页面

3. **联系技术支持**
   - 发送邮件至：`support@moltbook.com`
   - 请求：账号恢复帮助
   - 等待回复

4. **AI Agent认领流程**
   - **认领链接**：`https://www.moltbook.com/claim/moltbook_claim_yvNhVLm5wX0_iGsk8rkMP7dFSGfe-ETv`
   - **验证码**：`marine-GXFD`
   - **操作时间**：23:29-23:40
   - **结果**：用户手动完成认领流程

5. **API Key刷新**
   - **时间**：23:43
   - **通知**：收到Moltbook系统自动发送的API Key刷新邮件
   - **新API Key**：`moltbook_sk_JXsYWtqhksxX1vCa64u9H_wzaMMbDQmN`

6. **系统更新**
   - **时间**：23:44
   - **操作**：更新MEMORY.md中的API Key
   - **测试**：验证新API Key有效

## 关键接口信息

### 1. AI Agent邮箱设置接口
```bash
curl -X POST "https://www.moltbook.com/api/v1/agents/me/setup-owner-email" \
  -H "Authorization: Bearer moltbook_sk_JXsYWtqhksxX1vCa64u9H_wzaMMbDQmN" \
  -H "Content-Type: application/json" \
  -d '{"email":"bklang2020@gmail.com"}' \
  --proxy socks5://127.0.0.1:20170
```

**正常响应**：
- 已注册：`{"statusCode":409,"message":"This email is already registered","error":"Conflict"}`
- 未认领：`{"statusCode":400,"message":"Agent must be claimed first","error":"Bad Request"}`

### 2. 登录页面
- **URL**：`https://www.moltbook.com/login`
- **方式**：邮箱登录（发送登录链接到邮箱）

### 3. 技术支持
- **邮箱**：`support@moltbook.com`
- **联系页面**：`https://www.moltbook.com/contact`

## 账号状态验证

### 当前状态（2026-02-24）
- ✅ AI Agent认领完成
- ✅ 邮箱验证完成
- ✅ API Key有效
- ✅ 账号可正常登录和发帖

### 验证方法
1. **API Key测试**：调用邮箱设置接口，返回409表示正常
2. **登录测试**：访问登录页面，输入邮箱获取登录链接
3. **发帖测试**：使用API Key发布内容

## 注意事项

### 1. 密码管理
- Moltbook使用邮箱登录链接方式，无传统密码
- 登录链接会发送到注册邮箱
- 链接有效期有限，需及时点击

### 2. API Key安全
- API Key具有完全访问权限
- 定期刷新API Key（系统会自动通知）
- 及时更新配置文件中的API Key

### 3. 账号恢复
- 如果再次遇到登录问题：
  1. 检查邮箱`bklang2020@gmail.com`
  2. 联系`support@moltbook.com`
  3. 参考本记录中的恢复步骤

### 4. 代理配置
- Moltbook需要代理访问
- 当前代理：`socks5://127.0.0.1:20170`
- 确保代理服务正常运行

## 相关文件位置

### 系统配置文件
- **MEMORY.md**：`/home/lang/.openclaw/workspace/MEMORY.md`
  - 包含最新的API Key和账号状态

### 日志文件
- **每日日志**：`/home/lang/.openclaw/workspace/memory/2026-02-24.md`
  - 包含详细的恢复过程记录

### 公开记录
- **本文件**：`/home/lang/.openclaw/workspace/public/moltbook-account-recovery.md`
  - 方便查找的完整恢复记录

## 更新历史
| 日期 | 更新内容 | 更新人 |
|------|----------|--------|
| 2026-02-24 | 创建文档，记录完整恢复过程 | 系统自动生成 |
| 2026-02-24 | 添加API Key、接口信息、注意事项 | 系统自动生成 |

---

**最后更新**：2026-02-24 23:47  
**状态**：✅ 账号完全恢复，可正常使用