#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据自动更新脚本
功能：每天下载最新的开奖数据，更新本地数据库

使用方法：
    python update_qlc.py

Cron配置：
    0 21 * * 1,3,5 /usr/bin/python3 /home/lang/.openclaw/workspace/caipiao/update_qlc.py >> /home/lang/.openclaw/workspace/caipiao/logs/update.log 2>&1

说明：七乐彩每周一、三、五21:15开奖，所以cron设置在21:00执行
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 配置
DATA_DIR = Path("/home/lang/.openclaw/workspace/caipiao")
LOG_DIR = DATA_DIR / "logs"
HISTORY_FILE = DATA_DIR / "qlc_history_full.json"
BACKUP_DIR = DATA_DIR / "backups"
LOG_FILE = LOG_DIR / "update.log"

def log(message):
    """日志记录"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + "\n")

def load_history():
    """加载历史数据"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(data):
    """保存历史数据"""
    # 先备份
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True)
    
    backup_file = BACKUP_DIR / f"qlc_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 保存最新
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    log(f"数据已保存，共 {len(data)} 条")

def download_latest():
    """下载最新数据"""
    import requests
    
    url = "http://data.17500.cn/7lc_desc.txt"
    
    log(f"下载最新数据: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/plain,*/*',
        'Referer': 'https://www.17500.cn/',
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=60)
        r.raise_for_status()
        
        # 保存临时文件
        temp_file = DATA_DIR / "7lc_desc_new.txt"
        with open(temp_file, 'wb') as f:
            f.write(r.content)
        
        log(f"下载成功，文件大小: {len(r.content)} 字节")
        return temp_file
        
    except Exception as e:
        log(f"下载失败: {e}")
        return None

def parse_data(file_path):
    """解析数据文件"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 10:
                data.append({
                    "period": parts[0],
                    "date": parts[1],
                    "basic_numbers": parts[2:9],
                    "special_number": parts[9],
                    "total_bet": parts[10] if len(parts) > 10 else None,
                })
    return data

def merge_data(old_data, new_data):
    """合并数据，保留最新的"""
    # 创建期号集合
    existing_periods = {item['period'] for item in old_data}
    
    # 添加新数据
    merged = old_data.copy()
    for item in new_data:
        if item['period'] not in existing_periods:
            merged.insert(0, item)  # 新数据放在最前面
            existing_periods.add(item['period'])
    
    return merged

def main():
    """主函数"""
    log("=" * 50)
    log("七乐彩数据更新任务开始")
    
    # 确保日志目录存在
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. 加载历史数据
    log(f"加载历史数据: {HISTORY_FILE}")
    old_data = load_history()
    log(f"历史数据: {len(old_data)} 条")
    
    # 2. 下载最新数据
    temp_file = download_latest()
    if not temp_file:
        log("更新失败：无法下载数据")
        return 1
    
    # 3. 解析新数据
    log("解析新数据...")
    new_data = parse_data(temp_file)
    log(f"新数据: {len(new_data)} 条")
    
    # 4. 合并数据
    log("合并数据...")
    merged_data = merge_data(old_data, new_data)
    new_count = len(merged_data) - len(old_data)
    log(f"新增: {new_count} 条，总数: {len(merged_data)} 条")
    
    if new_count > 0:
        # 5. 保存数据
        log("保存更新后的数据...")
        save_history(merged_data)
        log(f"✅ 更新完成！新增 {new_count} 条数据")
    else:
        log("✅ 没有新数据，无需更新")
    
    # 6. 清理临时文件
    temp_file.unlink(missing_ok=True)
    
    # 7. 更新预测目标期号和日期
    update_prediction_target(merged_data)
    
    log("任务结束")
    log("=" * 50)
    return 0

def update_prediction_target(data):
    """更新预测目标期号和日期"""
    TEMPLATE_FILE = Path("/home/lang/.openclaw/workspace/caipiao/预测帮助模板.md")
    
    if not TEMPLATE_FILE.exists():
        return
    
    # 排序数据（按期号降序，最新在前）
    data.sort(key=lambda x: x['period'], reverse=True)
    
    latest = data[0]
    latest_period = latest['period']
    latest_date = datetime.strptime(latest['date'], '%Y-%m-%d')
    next_period = str(int(latest_period) + 1)
    
    # 七乐彩开奖日：周一(0)、周三(2)、周五(4)
    # 计算下一个开奖日
    weekday = latest_date.weekday()  # 0=周一, 1=周二, ..., 6=周日
    
    # 根据当前开奖日推算下一个开奖日
    if weekday == 0:  # 周一 -> 周三(2天后)
        next_date = latest_date + timedelta(days=2)
    elif weekday == 2:  # 周三 -> 周五(2天后)
        next_date = latest_date + timedelta(days=2)
    elif weekday == 4:  # 周五 -> 下周一(3天后)
        next_date = latest_date + timedelta(days=3)
    else:
        # 如果不是开奖日（如数据有误），默认找下一个周一/三/五
        next_date = latest_date + timedelta(days=2)
    
    next_date_str = next_date.strftime('%Y-%m-%d')
    
    # 读取模板
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换预测目标
    old_target = f"📌 预测目标: 第{next_period}期 (预计{next_date_str}开奖)"
    import re
    content = re.sub(r'📌 预测目标: 第\d+期 \(预计\d+-\d+-\d+开奖\)', old_target, content)
    
    with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"预测目标已更新: 第{next_period}期 (预计{next_date_str}开奖)")

if __name__ == "__main__":
    sys.exit(main())
