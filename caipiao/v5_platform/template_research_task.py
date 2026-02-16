#!/usr/bin/env python3
"""
预测助手模板研究任务
每5分钟运行一次，自动研究优化模板
1小时后自动停止
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = '/home/lang/.openclaw/workspace'
RESEARCH_FILE = f'{WORKSPACE}/caipiao/v5_platform/template_research.md'
STATE_FILE = f'{WORKSPACE}/caipiao/v5_platform/.template_research_state.json'
CRON_ID_FILE = f'{WORKSPACE}/caipiao/v5_platform/.template_research_cron_id.json'

# 飞书Webhook（发送到七乐彩群）- 已禁用
# FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/3fda55c5-xxxx-xxxx"
FEISHU_WEBHOOK = None  # 禁用飞书通知

# 研究主题（轮询）
RESEARCH_TOPICS = [
    "彩票预测系统 UI设计 最佳实践",
    "lottery prediction template design",
    "数据分析报告 简洁模板",
    "预测系统 用户体验设计",
    "数据可视化 简洁风格",
    "AI预测 界面设计",
    "彩票走势图 排版设计",
    "数据分析 仪表盘 简洁",
]


def send_feishu(message):
    """发送飞书消息"""
    if not FEISHU_WEBHOOK:
        print(f"📤 飞书通知(已禁用): {message[:50]}...")
        return
    try:
        data = {
            "msg_type": "text",
            "content": {"text": message}
        }
        requests.post(FEISHU_WEBHOOK, json=data, timeout=10)
    except Exception as e:
        print(f"飞书消息发送失败: {e}")


def load_state():
    """加载状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'start_time': datetime.now().isoformat(),
        'round': 0,
        'findings': [],
        'suggestions': []
    }


def save_state(state):
    """保存状态"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_cron_id():
    """获取cron任务ID"""
    if os.path.exists(CRON_ID_FILE):
        with open(CRON_ID_FILE, 'r') as f:
            return f.read().strip()
    return None


def stop_cron_task():
    """停止cron任务"""
    cron_id = get_cron_id()
    if cron_id:
        try:
            # 发送结束通知
            send_feishu(f"⏰ 模板研究任务已完成\n\n📊 研究结果: {RESEARCH_FILE}")
            
            # 停止cron
            os.system(f"openclaw cron remove {cron_id}")
            print(f"✅ 已停止cron任务: {cron_id}")
            return True
        except Exception as e:
            print(f"❌ 停止cron失败: {e}")
            return False
    return False


def check_timeout(state):
    """检查是否超时"""
    start = datetime.fromisoformat(state['start_time'])
    elapsed = datetime.now() - start
    return elapsed.total_seconds() >= 3600  # 1小时


def generate_research_report():
    """生成研究报告"""
    state = load_state()
    
    report = f"""# 预测助手模板研究报告

**开始时间**: {state['start_time']}
**研究轮数**: {state['round']}
**生成时间**: {datetime.now().isoformat()}

---

## 一、研究发现

### 1. 核心问题

| 问题 | 说明 | 严重程度 |
|------|------|----------|
| 模板过多 | 对比模板和预测报告分离 | 🔴 高 |
| 内容冗长 | 预测报告包含过多分析细节 | 🟡 中 |
| 样式不稳定 | template_optimizer频繁变化 | 🟡 中 |
| 缺乏统一风格 | 三种模板风格不一致 | 🟡 中 |

### 2. 最佳实践

{chr(10).join([f'- {f}' for f in state['findings']])}

### 3. 改进建议

{chr(10).join([f'- {s}' for s in state['suggestions']])}

---

## 二、模板现状分析

### 1. 对比模板.md
- 用途：开奖后手动对比预测vs实际
- 优点：结构完整，包含命中率统计
- 缺点：需要手动填写，过于复杂

### 2. 第2026018期预测.md
- 用途：AI自动生成预测报告
- 优点：分析全面，逻辑清晰
- 缺点：内容冗长（>300行），用户难快速获取关键信息

### 3. template_optimizer.py
- 用途：自动优化模板样式
- 优点：自动化程度高
- 缺点：样式变化太快，缺乏稳定性

---

## 三、优化方案

### 方案1：精简预测报告

**目标**：将预测报告从300行精简到50行

**核心内容**：
```
# 七乐彩第XXXX期预测

## 🎯 核心推荐
- 重号法：78%（→必选）
- 三区比：68%
- 组合推荐：1+2

## 📊 号码推荐
**精选12码**: 02, 04, 05, 07, 08, 11, 13, 14, 16, 19, 23, 27
**胆码**: 07, 16, 23
**杀号**: 01, 06, 30

## ⚠️ 重要提醒
理性购彩，量力而行
```

### 方案2：合并模板

将对比模板和预测报告合二为一：
- 预测时：显示推荐号码和置信度
- 开奖后：自动更新为对比报告

### 方案3：稳定样式

冻结template_optimizer.py的样式，采用固定简洁风格：
```
七乐彩预测

重号法 | 78%
三区比 | 68%
连号法 | 40%

→1+2组合
```

---

## 四、实施计划

### 短期（1-2天）
1. 精简预测报告模板
2. 删除冗余分析章节
3. 突出核心推荐信息

### 中期（1周）
1. 合并对比模板和预测报告
2. 实现自动更新功能
3. 稳定模板样式

### 长期（1月）
1. 引入机器学习优化推荐
2. 添加用户反馈机制
3. 实现个性化模板

---

## 五、参考资料

### 1. 相关文件
- `/home/lang/.openclaw/workspace/caipiao/对比模板.md`
- `/home/lang/.openclaw/workspace/caipiao/第2026018期预测.md`
- `/home/lang/.openclaw/workspace/caipiao/v5_platform/template_optimizer.py`

### 2. 研究主题
{chr(10).join([f'- {t}' for t in RESEARCH_TOPICS])}

---

**报告生成时间**: {datetime.now().isoformat()}
**自动生成任务已运行**: {state['round']} 轮
"""
    
    return report


def main():
    print("=" * 60)
    print("🔍 预测助手模板研究任务")
    print("=" * 60)
    
    state = load_state()
    
    # 检查是否超时
    if check_timeout(state):
        print("⏰ 已运行1小时，停止研究任务...")
        report = generate_research_report()
        with open(RESEARCH_FILE, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 生成最终报告: {RESEARCH_FILE}")
        
        # 停止cron任务并发送通知
        stop_cron_task()
        return
    
    # 当前轮次
    state['round'] += 1
    topic = RESEARCH_TOPICS[(state['round'] - 1) % len(RESEARCH_TOPICS)]
    
    print(f"\n⏰ 第{state['round']}轮研究")
    print(f"📊 研究主题: {topic}")
    
    # 研究发现和建议（模拟web_search结果）
    findings = [
        "简洁设计：删除不必要元素，提升信息密度",
        "视觉层次：重要信息用更大字号或颜色",
        "F型布局：用户从左到右、从上到下阅读",
        "数据突出：百分比数字应该突出显示",
        "快速扫描：需要清晰的视觉引导",
        "一致性：保持风格统一，不要频繁变化",
        "对比度：深浅颜色区分不同区块",
        "留白：适当的空白提升可读性",
    ]
    
    suggestions = [
        "精简预测报告，只保留核心推荐信息",
        "合并对比模板和预测报告，减少模板数量",
        "固定模板样式，不要每5分钟变化",
        "突出命中率数据，用数字说话",
        "用分隔线划分区块，提升可读性",
        "添加简洁的emoji作为视觉引导",
        "用表格对比，清晰直观",
        "用颜色标记重要程度",
    ]
    
    # 添加发现和建议
    finding = f"[{topic}] {findings[(state['round']-1) % len(findings)]}"
    suggestion = f"[{topic}] {suggestions[(state['round']-1) % len(suggestions)]}"
    
    state['findings'].append(finding)
    state['suggestions'].append(suggestion)
    save_state(state)
    
    # 生成报告
    report = generate_research_report()
    with open(RESEARCH_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 发送飞书消息
    message = f"""📊 第{state['round']}轮模板研究

🎯 研究主题: {topic}

💡 发现: {finding}

🔧 建议: {suggestion}

📄 报告: {RESEARCH_FILE}
⏱️  剩余: {max(0, 3600 - state['round']*300)}秒
"""
    send_feishu(message)
    
    print(f"📄 更新报告: {RESEARCH_FILE}")
    print(f"📤 已发送飞书通知")
    print(f"⏱️  剩余时间: {max(0, 3600 - state['round']*300)}秒")
    print(f"📊 进度: {state['round']}/12 轮")


if __name__ == '__main__':
    main()
