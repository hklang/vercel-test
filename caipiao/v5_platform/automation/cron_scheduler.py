#!/usr/bin/env python3
"""Cron调度器"""

import subprocess
import json
from datetime import datetime
from typing import Dict, List, Callable

class CronScheduler:
    """Cron调度器"""
    
    def __init__(self):
        self.tasks = []
    
    def add_task(self, name: str, schedule: str, command: str):
        """添加任务"""
        self.tasks.append({
            'name': name,
            'schedule': schedule,
            'command': command,
        })
        print(f"✅ 添加任务: {name} ({schedule})")
    
    def remove_task(self, name: str):
        """删除任务"""
        self.tasks = [t for t in self.tasks if t['name'] != name]
        print(f"✅ 删除任务: {name}")
    
    def list_tasks(self) -> List[Dict]:
        """列出任务"""
        return self.tasks
    
    def run_task(self, name: str) -> bool:
        """运行任务"""
        for task in self.tasks:
            if task['name'] == name:
                try:
                    result = subprocess.run(task['command'], shell=True, capture_output=True)
                    print(f"✅ 运行完成: {name}")
                    return result.returncode == 0
                except Exception as e:
                    print(f"❌ 运行失败: {e}")
                    return False
        return False
    
    def generate_crontab(self) -> str:
        """生成crontab配置"""
        lines = ["# 七乐彩预测平台定时任务", ""]
        
        for task in self.tasks:
            lines.append(f"{task['schedule']} {task['command']} # {task['name']}")
        
        return '\n'.join(lines)
    
    def apply_crontab(self):
        """应用crontab"""
        crontab = self.generate_crontab()
        
        # 保存到文件
        with open('/home/lang/.openclaw/workspace/caipiao/v5_platform/crontab.txt', 'w') as f:
            f.write(crontab)
        
        # 应用
        try:
            subprocess.run('crontab /home/lang/.openclaw/workspace/caipiao/v5_platform/crontab.txt', shell=True)
            print("✅ Crontab已应用")
            return True
        except Exception as e:
            print(f"❌ 应用失败: {e}")
            return False

def setup_weekly_tasks(scheduler: CronScheduler):
    """设置每周任务"""
    # 七乐彩开奖日: 周一、三、五 21:35
    scheduler.add_task(
        "七乐彩-数据更新",
        "35 21 * * 1,3,5",
        "cd /home/lang/.openclaw/workspace/caipiao && python3 v5_platform/prediction/update_data.py"
    )
    
    scheduler.add_task(
        "七乐彩-预测生成",
        "40 21 * * 1,3,5",
        "cd /home/lang/.openclaw/workspace/caipiao && python3 v5_platform/prediction/prediction_engine.py"
    )
    
    scheduler.add_task(
        "七乐彩-分析报告",
        "0 22 * * 1,3,5",
        "cd /home/lang/.openclaw/workspace/caipiao && python3 v5_platform/output/report_generator.py"
    )
    
    # 每日任务
    scheduler.add_task(
        "每日数据备份",
        "0 3 * * *",
        "cd /home/lang/.openclaw/workspace/caipiao && python3 v5_platform/automation/backup.py"
    )

def main():
    """主函数"""
    print("=" * 60)
    print("Cron调度器设置")
    print("=" * 60)
    
    scheduler = CronScheduler()
    setup_weekly_tasks(scheduler)
    
    # 生成crontab
    crontab = scheduler.generate_crontab()
    print("\n生成的Crontab配置:")
    print(crontab)
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
