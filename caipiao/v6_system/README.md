# 七乐彩智能预测系统 V6.0

## 📋 概述

七乐彩智能预测系统 V6.0 是一个**全自动、7x24小时运行**的预测系统，具备以下特性：

### ✨ 核心功能

| 功能 | 说明 | 状态 |
|:---|:---|:---:|
| 🤖 机器学习 | 纯Python随机森林 | ✅ |
| ⚖️ 动态权重 | 根据表现自动调整 | ✅ |
| 📍 分位置预测 | 首位/末位/中间分开 | ✅ |
| 🔄 自动更新 | 数据变化自动重新预测 | ✅ |
| 🧪 自我验证 | 自动验证预测准确性 | ✅ |
| 📊 完整日志 | 记录所有运行状态 | ✅ |

---

## 🚀 快速开始

### 方式1：运行一次
```bash
cd /home/lang/.openclaw/workspace/caipiao/v6_system
python3 main.py
```

### 方式2：后台运行（推荐）
```bash
cd /home/lang/.openclaw/workspace/caipiao/v6_system
python3 run_v6.py --start
```

### 方式3：Cron定时运行
```bash
# 每2小时运行一次
0 */2 * * * /usr/bin/python3 /home/lang/.openclaw/workspace/caipiao/v6_system/run_v6.py --cron
```

---

## 📁 文件结构

```
v6_system/
├── main.py           # 主程序（预测引擎）
├── run_v6.py         # 管理脚本（启动/停止/状态）
├── README.md         # 本文档
└── ...

v6_output/            # 输出目录
├── predictions_YYYYMMDD_HHMMSS.csv  # 预测结果
├── predictions_latest.csv           # 最新预测（软链接）
└── ...

v6_models/            # 模型目录
├── weights.json      # 当前权重配置
└── weights_history.json  # 权重变化历史

v6_logs/             # 日志目录
├── system.log        # 系统运行日志
├── report_YYYYMMDD_HHMMSS.txt  # 预测报告
└── report_latest.txt  # 最新报告（软链接）
```

---

## 🎯 预测方法

### 特征提取（172个特征）
1. **频率特征** - 5/10/20期窗口
2. **遗漏特征** - 各号码遗漏值
3. **和值特征** - 均值、趋势
4. **跨度特征** - 最大-最小差
5. **AC值特征** - 复杂度指标
6. **012路特征** - 除3余数分布
7. **奇偶特征** - 奇数个数
8. **大小特征** - 小/中/大分布
9. **位置特征** - 首位/末位
10. **连号特征** - 连续号码

### 预测策略
- **热号策略**: 30%
- **遗漏策略**: 35%
- **特征策略**: 15%
- **随机策略**: 15%
- **ML策略**: 10%

### 约束条件
- 奇偶分布：2-5个奇数
- 大小分布：1-4个小/中/大
- 和值范围：60-170
- 跨度范围：15-27
- AC值范围：8-15
- 连号限制：最多2组

---

## 📊 自动化运维

### 管理命令

```bash
# 启动
python3 run_v6.py --start

# 停止
python3 run_v6.py --stop

# 重启
python3 run_v6.py --restart

# 状态
python3 run_v6.py --status

# 日志
python3 run_v6.py --log

# 运行一次（不守护）
python3 run_v6.py
```

### Cron配置

```bash
# 每2小时自动更新预测
0 */2 * * * /usr/bin/python3 /home/lang/.openclaw/workspace/caipiao/v6_system/run_v6.py --cron >> /home/lang/.openclaw/workspace/caipiao/v6_logs/cron.log 2>&1

# 每天凌晨3点更新数据并预测
0 3 * * * /usr/bin/python3 /home/lang/.openclaw/workspace/caipiao/update_qlc.py >> /home/lang/.openclaw/workspace/caipiao/logs/update.log 2>&1
```

### Systemd服务（可选）

```ini
# /etc/systemd/system/v6-qlc.service
[Unit]
Description=QiLeCai Prediction System V6.0
After=network.target

[Service]
Type=simple
User=lang
WorkingDirectory=/home/lang/.openclaw/workspace/caipiao/v6_system
ExecStart=/usr/bin/python3 /home/lang/.openclaw/workspace/caipiao/v6_system/run_v6.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 安装服务
sudo cp v6-qlc.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable v6-qlc
sudo systemctl start v6-qlc
```

---

## 📈 验证与评估

### 自我验证机制

系统会自动：
1. 用前N期数据训练模型
2. 预测后M期的结果
3. 计算命中率
4. 根据结果调整权重

### 查看验证结果

```bash
# 运行验证
python3 main.py --verify

# 查看日志
tail -100 v6_logs/system.log
```

---

## 🔧 故障排除

### 问题1：预测失败
```bash
# 检查数据
python3 -c "import json; d=json.load(open('qlc_history_full.json')); print(len(d))"
# 确保数据文件存在且有效
```

### 问题2：无法启动
```bash
# 检查端口占用
lsof -i :8080

# 检查日志
cat v6_logs/system.log
```

### 问题3：内存不足
```bash
# 清理旧文件
rm -f v6_output/predictions_*.csv
rm -f v6_logs/report_*.txt

# 减少特征
# 修改 main.py 中的 FEATURE_WINDOWS
```

---

## 📝 更新日志

### V6.0 (2026-02-12)
- ✅ 机器学习预测
- ✅ 动态权重调整
- ✅ 分位置预测
- ✅ 7x24自动运行
- ✅ 完整日志系统

---

## ⚠️ 免责声明

- 本系统仅供学习研究使用
- 彩票具有随机性，预测结果不保证准确
- 请理性购彩，量力而行
- 作者不承担任何责任

---

## 📧 联系

如有问题，请查看日志或联系开发者。
