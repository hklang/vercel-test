#!/usr/bin/env python3
"""
自动任务管理脚本 - V7.1
每小时自动运行预测
"""

import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path

# 配置
PREDICT_SCRIPT = '/home/lang/.openclaw/workspace/caipiao/v5_platform/main.py'
LOG_DIR = '/home/lang/.openclaw/workspace/caipiao/v5_platform/logs'
PID_FILE = '/tmp/predictor_auto.pid'
INTERVAL = 3600  # 1小时


def check_running():
    """检查是否在运行"""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        try:
            os.kill(int(pid), 0)
            return int(pid)
        except (OSError, ProcessLookupError):
            os.remove(PID_FILE)
            return None
    return None


def start_daemon(interval=INTERVAL):
    """启动守护进程"""
    pid = check_running()
    if pid:
        print(f"❌ 已在运行 (PID: {pid})")
        return
    
    print("🚀 启动自动预测任务...")
    
    cmd = [sys.executable, PREDICT_SCRIPT]
    proc = os.popen(' '.join(cmd) + f' > {LOG_DIR}/auto.log 2>&1 & echo $!')
    pid = proc.read().strip()
    
    with open(PID_FILE, 'w') as f:
        f.write(pid)
    
    print(f"✅ 已启动 (PID: {pid})")
    print(f"   间隔: {interval}秒（1小时）")
    print(f"   日志: {LOG_DIR}/auto.log")


def stop_daemon():
    """停止守护进程"""
    pid = check_running()
    if not pid:
        print("❌ 未运行")
        return
    
    try:
        os.kill(pid, 9)
        os.remove(PID_FILE)
        print("✅ 已停止")
    except Exception as e:
        print(f"❌ 停止失败: {e}")


def run_once():
    """运行一次"""
    print("="*50)
    print("运行预测任务")
    print("="*50)
    os.system(f'{sys.executable} {PREDICT_SCRIPT}')
    
    # 发送飞书通知
    print("\n📤 发送飞书通知...")
    os.system(f'{sys.executable} /home/lang/.openclaw/workspace/caipiao/v5_platform/notify_feishu.py')


def show_status():
    """查看状态"""
    pid = check_running()
    if pid:
        print(f"✅ 运行中 (PID: {pid})")
    else:
        print("❌ 未运行")
    
    # 显示最近运行时间
    log_file = f'{LOG_DIR}/auto.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.read().split('\n')
            for line in reversed(lines):
                if line.strip():
                    print(f"\n最近运行: {line}")
                    break


def generate_cron():
    """生成Cron配置"""
    cron_line = f"0 * * * * /usr/bin/python3 {PREDICT_SCRIPT} >> {LOG_DIR}/cron.log 2>&1"
    
    print("=== Cron配置 ===")
    print(cron_line)
    print()
    print("添加到crontab:")
    print(f"  echo \"{cron_line}\" >> /var/spool/cron/crontabs/lang")
    print("  或编辑: crontab -e")


def main():
    parser = argparse.ArgumentParser(description='自动预测任务管理')
    parser.add_argument('--start', action='store_true', help='启动守护进程')
    parser.add_argument('--stop', action='store_true', help='停止守护进程')
    parser.add_argument('--status', action='store_true', help='查看状态')
    parser.add_argument('--cron', action='store_true', help='生成Cron配置')
    parser.add_argument('--run', action='store_true', help='运行一次')
    
    args = parser.parse_args()
    
    if args.start:
        start_daemon()
    elif args.stop:
        stop_daemon()
    elif args.status:
        show_status()
    elif args.cron:
        generate_cron()
    elif args.run:
        run_once()
    else:
        # 默认运行一次
        run_once()


if __name__ == '__main__':
    main()
