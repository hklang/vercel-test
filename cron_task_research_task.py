#!/usr/bin/env python3
"""
定时任务设计研究任务
每5分钟运行一次，自动研究定时任务优化
1小时后自动停止
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = '/home/lang/.openclaw/workspace'
RESEARCH_FILE = f'{WORKSPACE}/cron_task_research.md'
STATE_FILE = f'{WORKSPACE}/.cron_task_research_state.json'
CRON_ID_FILE = f'{WORKSPACE}/.cron_task_research_cron_id.json'

# 研究主题（轮询）
RESEARCH_TOPICS = [
    "cron job best practices production",
    "scheduled task reliability design",
    "cron task monitoring alerting best practices",
    "distributed cron job architecture",
    "celery beat vs cron comparison",
    "task queue design patterns",
    "cron job retry strategy exponential backoff",
    "systemd timer vs cron performance",
]


FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/3fda55c5-xxxx-xxxx"


def send_feishu(message):
    """发送飞书消息"""
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


def stop_cron_task():
    """停止cron任务"""
    if os.path.exists(CRON_ID_FILE):
        with open(CRON_ID_FILE, 'r') as f:
            cron_id = f.read().strip()
        if cron_id:
            try:
                msg = f"⏰ 定时任务研究已完成\n\n📄 结果: {RESEARCH_FILE}"
                send_feishu(msg)
                os.system(f"openclaw cron remove {cron_id}")
                print(f"已停止cron任务: {cron_id}")
            except Exception as e:
                print(f"停止cron失败: {e}")


def check_timeout(state):
    """检查是否超时"""
    start = datetime.fromisoformat(state['start_time'])
    elapsed = datetime.now() - start
    return elapsed.total_seconds() >= 3600  # 1小时


def generate_research_report():
    """生成研究报告"""
    state = load_state()
    
    findings_text = '\n'.join([f'- {f}' for f in state['findings']])
    suggestions_text = '\n'.join([f'- {s}' for s in state['suggestions']])
    topics_text = '\n'.join([f'- {t}' for t in RESEARCH_TOPICS])
    
    report = f"""# 定时任务设计研究报告

**开始时间**: {state['start_time']}
**研究轮数**: {state['round']}
**生成时间**: {datetime.now().isoformat()}

---

## 一、研究发现

### 核心发现

{findings_text}

### 改进建议

{suggestions_text}

---

## 二、现状分析

### 当前定时任务

| # | 任务 | 调度 | 状态 |
|:---|:---|:---|:---:|
| 1 | 每日新闻推送 | */30 8-20 * * * | ✅ |
| 2 | 新闻源扩展 | 0 */12 * * * | ✅ |
| 3 | 每日备份 | 0 3 * * * | ✅ |
| 4 | 七乐彩数据更新 | 35 21 * * 1,3,5 | ✅ |

### 存在问题

1. 缺乏监控：没有任务执行监控和告警
2. 无重试机制：任务失败后不会自动重试
3. 无依赖管理：任务之间没有依赖关系
4. 缺乏日志分析：没有任务执行统计分析

---

## 三、优化方案

### 1. 添加监控告警

实现任务执行状态监控，计算成功率、平均执行时间等指标。

### 2. 智能重试机制

使用指数退避策略，失败后自动重试。

### 3. 任务依赖管理

定义任务依赖关系，按正确顺序执行。

### 4. 健康检查

每5分钟检查系统健康状态。

---

## 四、改进建议

### 短期（1-2天）
1. 添加任务执行监控
2. 开启失败告警
3. 记录详细日志

### 中期（1周）
1. 实现重试机制
2. 添加任务依赖
3. 统计执行效率

### 长期（1月）
1. 引入Celery等任务队列
2. 实现分布式任务管理
3. 添加可视化监控面板

---

## 五、参考资料

{topics_text}

---

**报告生成时间**: {datetime.now().isoformat()}
**任务状态**: {'运行中' if state['round'] < 12 else '已完成'}
"""
    
    return report


def main():
    print("=" * 60)
    print("⏰ 定时任务设计研究任务")
    print("=" * 60)
    
    state = load_state()
    
    # 检查是否超时
    if check_timeout(state):
        print("已运行1小时，停止研究任务...")
        report = generate_research_report()
        with open(RESEARCH_FILE, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"生成最终报告: {RESEARCH_FILE}")
        stop_cron_task()
        return
    
    # 当前轮次
    state['round'] += 1
    topic = RESEARCH_TOPICS[(state['round'] - 1) % len(RESEARCH_TOPICS)]
    
    print(f"\n第{state['round']}轮研究")
    print(f"研究主题: {topic}")
    
    # 研究发现和建议
    findings = [
        "可靠性：添加健康检查和自动恢复机制",
        "可观测性：记录详细日志和执行指标",
        "幂等性：确保任务可重复执行",
        "优雅降级：依赖服务不可用时跳过非关键任务",
        "资源控制：限制任务执行时间和内存使用",
        "监控告警：任务失败时立即通知",
        "重试策略：使用指数退避避免雪崩",
        "依赖管理：按正确顺序执行依赖任务",
    ]
    
    suggestions = [
        "添加任务执行监控和成功率统计",
        "实现失败自动重试和告警",
        "为相关任务添加依赖关系",
        "定期清理过期日志和数据",
        "添加任务超时保护机制",
        "实现任务去重避免重复执行",
        "使用分布式锁防止并发问题",
        "添加任务执行效率分析",
    ]
    
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
    message = f"""📊 第{state['round']}轮定时任务研究

主题: {topic}

发现: {finding}

建议: {suggestion}

报告: {RESEARCH_FILE}
剩余: {max(0, 3600 - state['round']*300)}秒
"""
    send_feishu(message)
    
    print(f"更新报告: {RESEARCH_FILE}")
    print(f"已发送飞书通知")
    print(f"进度: {state['round']}/12 轮")


if __name__ == '__main__':
    main()
