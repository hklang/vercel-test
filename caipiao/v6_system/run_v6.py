#!/usr/bin/env python3
"""
七乐彩智能预测系统 V6.0 - Cron配置和自动启动脚本
===================================================

功能：
- 系统启动时自动运行
- 定时更新预测
- 7x24小时无人值守

使用方法：
    python3 run_v6.py              # 前台运行
    python3 run_v6.py --daemon    # 后台运行
    python3 run_v6.py --start     # 启动服务
    python3 run_v6.py --stop      # 停止服务
    python3 run_v6.py --status    # 查看状态
    python3 run_v6.py --log       # 查看日志
"""

import os
import sys
import time
import signal
import argparse
import subprocess
from pathlib import Path

# 配置
WORKSPACE = '/home/lang/.openclaw/workspace/caipiao/v6_system'
PYTHON = sys.executable
PID_FILE = '/home/lang/.openclaw/workspace/caipiao/v6_system/v6.pid'
LOG_FILE = '/home/lang/.openclaw/workspace/caipiao/v6_logs/system.log'


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


def start_daemon(interval: int = 7200):
    """启动守护进程"""
    pid = check_running()
    if pid:
        print(f"❌ 已在运行 (PID: {pid})")
        return
    
    print("🚀 启动 V6.0 预测系统...")
    
    # 启动
    cmd = [
        PYTHON, f'{WORKSPACE}/main.py',
        '--auto', str(interval)
    ]
    
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    # 保存PID
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    time.sleep(2)
    
    if check_running():
        print(f"✅ 已启动 (PID: {proc.pid})")
        print(f"   日志: {LOG_FILE}")
        print(f"   预测: {WORKSPACE}/v6_output/predictions_latest.csv")
    else:
        print("❌ 启动失败")


def stop_daemon():
    """停止守护进程"""
    pid = check_running()
    if not pid:
        print("❌ 未运行")
        return
    
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        
        if not check_running():
            os.remove(PID_FILE)
            print("✅ 已停止")
        else:
            os.kill(pid, signal.SIGKILL)
            os.remove(PID_FILE)
            print("✅ 已强制停止")
    except Exception as e:
        print(f"❌ 停止失败: {e}")


def restart_daemon(interval: int = 7200):
    """重启"""
    stop_daemon()
    time.sleep(2)
    start_daemon(interval)


def show_status():
    """查看状态"""
    pid = check_running()
    if pid:
        print(f"✅ 运行中 (PID: {pid})")
        print(f"   预测目录: {WORKSPACE}/v6_output/")
        print(f"   日志文件: {LOG_FILE}")
        
        # 检查最后更新时间
        pred_file = f'{WORKSPACE}/v6_output/predictions_latest.csv'
        if os.path.exists(pred_file):
            mtime = os.path.getmtime(pred_file)
            elapsed = time.time() - mtime
            if elapsed < 3600:
                print(f"   最后预测: {elapsed/60:.0f} 分钟前")
            else:
                print(f"   最后预测: {elapsed/3600:.1f} 小时前")
    else:
        print("❌ 未运行")
        print("   使用 --start 启动")


def show_log(lines: int = 50):
    """查看日志"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            content = f.read().split('\n')
            for line in content[-lines:]:
                print(line)
    else:
        print("日志文件不存在")


def run_once():
    """运行一次"""
    cmd = [PYTHON, f'{WORKSPACE}/main.py']
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description='七乐彩V6系统管理')
    parser.add_argument('--start', action='store_true', help='启动服务')
    parser.add_argument('--stop', action='store_true', help='停止服务')
    parser.add_argument('--restart', action='store_true', help='重启服务')
    parser.add_argument('--status', action='store_true', help='查看状态')
    parser.add_argument('--log', action='store_true', help='查看日志')
    parser.add_argument('--daemon', action='store_true', help='后台运行')
    parser.add_argument('--interval', type=int, default=7200, help='更新间隔（秒）')
    
    args = parser.parse_args()
    
    if args.start:
        start_daemon(args.interval)
    elif args.stop:
        stop_daemon()
    elif args.restart:
        restart_daemon(args.interval)
    elif args.status:
        show_status()
    elif args.log:
        show_log()
    elif args.daemon:
        start_daemon(args.interval)
    else:
        run_once()


if __name__ == '__main__':
    main()
