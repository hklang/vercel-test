#!/usr/bin/env python3
"""
七乐彩优化任务 - 飞书反馈模板 V2.0
生成简洁友好的飞书消息
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 配置
OUTPUT_DIR = '/home/lang/.openclaw/workspace/caipiao/v5_platform/output'
LOG_DIR = '/home/lang/.openclaw/workspace/caipiao/v5_platform/logs'
DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'

# 飞书Webhook
FEISHU_WEBHOOK_URL = os.environ.get('FEISHU_WEBHOOK_URL', '')


def load_history():
    """加载历史数据"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


def load_predictions():
    """加载最新预测"""
    pred_file = f'{OUTPUT_DIR}/predictions_latest.csv'
    if not os.path.exists(pred_file):
        return None, None
    
    predictions = []
    with open(pred_file, 'r') as f:
        lines = f.readlines()
        for line in lines[1:11]:  # 前10组
            parts = line.strip().split(',')
            if len(parts) >= 8:
                numbers = [int(x) for x in parts[1:8]]
                predictions.append(numbers)
    
    # 获取最新期号
    history = load_history()
    latest_issue = history[-1]['period'] if history else '????'
    
    return predictions, latest_issue


def analyze_predictions(predictions):
    """分析预测数据"""
    if not predictions:
        return None
    
    # 和值
    sums = [sum(p) for p in predictions]
    avg_sum = sum(sums) / len(sums)
    min_sum = min(sums)
    max_sum = max(sums)
    
    # 奇偶
    odd_counts = [sum(1 for n in p if n % 2 == 1) for p in predictions]
    avg_odd = sum(odd_counts) / len(odd_counts)
    
    # 大小区
    small_counts = [sum(1 for n in p if n <= 10) for p in predictions]
    large_counts = [sum(1 for n in p if n >= 21) for p in predictions]
    
    return {
        'avg_sum': avg_sum,
        'min_sum': min_sum,
        'max_sum': max_sum,
        'avg_odd': avg_odd,
        'avg_small': sum(small_counts) / len(small_counts),
        'avg_large': sum(large_counts) / len(large_counts),
    }


def generate_feishu_message():
    """生成飞书消息（富文本格式）"""
    predictions, latest_issue = load_predictions()
    stats = analyze_predictions(predictions)
    
    if not predictions:
        return None
    
    # 格式化预测号码（前5组）
    pred_lines = []
    for i, p in enumerate(predictions[:5]):
        nums = ' '.join(f"{n:02d}" for n in p)
        pred_lines.append(f"  {i+1}. {nums}")
    pred_text = '\n'.join(pred_lines)
    
    # 分析结果
    analysis = ""
    if stats:
        analysis = f"""📈 分析:
   • 和值: {stats['avg_sum']:.0f} ({stats['min_sum']}-{stats['max_sum']})
   • 奇偶: {stats['avg_odd']:.1f}个奇数
   • 区间: 小区{stats['avg_small']:.1f}个 / 大区{stats['avg_large']:.1f}个"""
    
    message = f"""**【七乐彩智能预测】** 第{latest_issue}期

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')} · 100组预测

📊 数据: {len(load_history())}期

🎯 **精选5组:**
{pred_text}

{analysis}

📌 策略权重:
   热号20% | 遗漏30% | 周期15% | 特征20% | 随机15%

---
🔄 自动生成 | V7.1"""
    
    return message


def send_feishu(message):
    """发送到飞书"""
    if not FEISHU_WEBHOOK_URL or FEISHU_WEBHOOK_URL == 'YOUR_WEBHOOK_URL_HERE':
        print("⚠️ 未配置FEISHU_WEBHOOK_URL")
        print("\n" + "="*60)
        print("消息预览:")
        print("="*60)
        print(message)
        print("="*60)
        return False
    
    import requests
    try:
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            json={
                'msg_type': 'text',
                'content': {'text': message}
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ 飞书消息已发送")
            return True
        else:
            print(f"❌ 发送失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 发送出错: {e}")
        return False


def main():
    print("="*60)
    print("七乐彩 - 飞书通知")
    print("="*60)
    
    message = generate_feishu_message()
    
    if not message:
        print("❌ 无法生成消息（无预测数据）")
        return
    
    # 发送到飞书
    send_feishu(message)


if __name__ == '__main__':
    main()
