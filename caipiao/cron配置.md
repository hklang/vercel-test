# 七乐彩数据自动更新 - Cron配置

## 任务说明

**功能**: 每天自动下载最新的七乐彩开奖数据  
**脚本位置**: `/home/lang/.openclaw/workspace/caipiao/update_qlc.py`  
**日志位置**: `/home/lang/.openclaw/workspace/caipiao/logs/update.log`

---

## 七乐彩开奖时间

| 星期 | 开奖时间 |
|------|----------|
| 周一 | 21:15 |
| 周三 | 21:15 |
| 周五 | 21:15 |

因此，数据更新应设置在 **21:00** 或 **22:00**

---

## Cron配置

### 方案1：每次开奖后更新（推荐）

```bash
# 每周一、周三、周五 21:30 执行
0 21 * * 1,3,5
```

### 方案2：每天更新（简单）

```bash
# 每天 22:00 执行
0 22 * * *
```

### 方案3：OpenClaw Cron配置

```json
{
  "name": "qlc-data-update",
  "schedule": {
    "kind": "cron",
    "expr": "0 21 * * 1,3,5",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "执行七乐彩数据更新任务：运行 /home/lang/.openclaw/workspace/caipiao/update_qlc.py 脚本"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

---

## OpenClaw Cron命令

### 查看cron状态
```bash
openclaw cron status
```

### 添加任务
```bash
openclaw cron add --file cron.json
```

### 查看任务列表
```bash
openclaw cron list
```

### 手动执行任务
```bash
openclaw cron run <job_id>
```

---

## 手动执行

```bash
# 直接运行脚本
python3 /home/lang/.openclaw/workspace/caipiao/update_qlc.py

# 或添加执行权限后
chmod +x /home/lang/.openclaw/workspace/caipiao/update_qlc.py
/home/lang/.openclaw/workspace/caipiao/update_qlc.py
```

---

## 日志查看

```bash
# 实时查看日志
tail -f /home/lang/.openclaw/workspace/caipiao/logs/update.log

# 查看最近20行
tail -20 /home/lang/.openclaw/workspace/caipiao/logs/update.log

# 查看所有日志
cat /home/lang/.openclaw/workspace/caipiao/logs/update.log
```

---

## 数据备份

每次更新会自动备份到：
```
/home/lang/.openclaw/workspace/caipiao/backups/qlc_history_YYYYMMDD_HHMMSS.json
```

---

## 故障排除

### 问题1：权限不足
```bash
chmod +x /home/lang/.openclaw/workspace/caipiao/update_qlc.py
```

### 问题2：Python模块缺失
```bash
pip3 install requests
```

### 问题3：网络超时
- 检查网络连接
- 增加timeout值（当前60秒）

### 问题4：数据未更新
- 查看日志确认执行时间
- 确认七乐彩是否已开奖
- 手动执行脚本测试

---

## 监控建议

1. **定期检查日志**：确认任务正常运行
2. **监控新增数据**：确认数据确实在更新
3. **检查备份**：确认备份文件生成
4. **告警设置**：任务失败时通知

---

## 自动化流程图

```
时间触发 (21:00 or 22:00)
        ↓
执行 update_qlc.py
        ↓
下载最新数据 (data.17500.cn)
        ↓
解析数据
        ↓
合并到历史数据
        ↓
备份旧数据
        ↓
保存新数据
        ↓
记录日志
```

---

最后更新: 2026-02-09
