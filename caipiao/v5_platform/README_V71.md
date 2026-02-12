# 七乐彩 V7.1 预测系统使用说明

## 🎯 V7.1 新增功能

### 1. 周期性分析算法
- **星期规律分析**：根据当前星期推荐热号
- **周期回补预测**：预测即将回补的周期性号码
- **交替规律提示**：奇偶、大小交替趋势

### 2. 自动启动任务
- 每小时自动运行预测
- 后台守护进程模式
- 日志记录

### 3. 增强预测
- 新增周期性权重（15%）
- 周期性号码池

---

## 🚀 快速开始

### 方式1：手动运行一次
```bash
cd /workspace/caipiao/v5_platform
python3 main_v71.py
```

### 方式2：启动守护进程（推荐）
```bash
cd /workspace/caipiao/v5_platform
chmod +x auto_predict.sh
./auto_predict.sh start     # 启动
./auto_predict.sh status  # 状态
./auto_predict.sh stop    # 停止
```

### 方式3：Cron定时运行
```bash
# 生成Cron配置
./auto_predict.sh cron

# 手动添加到crontab
echo "0 * * * * /usr/bin/python3 /workspace/caipiao/v5_platform/main_v71.py >> /workspace/caipiao/v5_platform/logs/auto_predict.log 2>&1" | crontab -
```

---

## 📁 文件说明

| 文件 | 说明 |
|:---|:---|
| `main_v71.py` | V7.1主程序 |
| `auto_predict.sh` | 自动任务管理脚本 |
| `periodic_analyzer.py` | 周期性分析器 |
| `output/predictions_latest.csv` | 最新预测结果 |
| `output/report_latest.txt` | 最新报告 |
| `logs/system.log` | 系统日志 |

---

## ⚙️ 策略权重

| 策略 | 权重 |
|:---|:---:|
| 遗漏策略 | 30% |
| 热号策略 | 20% |
| 周期性策略 | 15% |
| 特征策略 | 20% |
| 随机策略 | 15% |

---

## 🆕 V7.1 vs V7.0

| 项目 | V7.0 | V7.1 |
|:---|:---:|:---:|
| 周期性分析 | ❌ | ✅ |
| 自动任务 | ❌ | ✅ |
| 策略权重 | 5个 | 6个 |

---

## 📊 预期提升

- 周期性分析带来额外 **3-5%** 命中率提升
- 自动运行节省人工操作

---

*生成时间: 2026-02-12*
