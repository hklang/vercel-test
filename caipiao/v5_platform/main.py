#!/usr/bin/env python3
"""主入口"""

import sys
import os

def main():
    """主函数"""
    print("=" * 60)
    print("七乐彩智能预测平台 V5.0")
    print("=" * 60)
    print()
    
    commands = {
        'predict': '生成预测',
        'report': '生成报告',
        'api': '启动API服务',
        'cron': '设置定时任务',
        'test': '运行测试',
        'all': '执行全部',
    }
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    else:
        print("可用命令:")
        for c, d in commands.items():
            print(f"  {c:10s} - {d}")
        print()
        cmd = 'predict'
    
    print(f"执行命令: {cmd}")
    print()
    
    # 执行
    if cmd == 'predict':
        from prediction.prediction_engine import main as run_predict
        run_predict()
    
    elif cmd == 'report':
        from output.report_generator import main as run_report
        run_report()
    
    elif cmd == 'api':
        from api.api_server import run_server
        run_server()
    
    elif cmd == 'cron':
        from automation.cron_scheduler import main as run_cron
        run_cron()
    
    elif cmd == 'test':
        print("运行测试...")
        os.system('bash run_all_tests.sh')
    
    elif cmd == 'all':
        print("执行全部功能...")
        
        # 预测
        print("\n[1/4] 生成预测...")
        try:
            from prediction.prediction_engine import main as run_predict
            run_predict()
        except Exception as e:
            print(f"预测失败: {e}")
        
        # 报告
        print("\n[2/4] 生成报告...")
        try:
            from output.report_generator import main as run_report
            run_report()
        except Exception as e:
            print(f"报告失败: {e}")
        
        # Cron
        print("\n[3/4] 设置定时任务...")
        try:
            from automation.cron_scheduler import main as run_cron
            run_cron()
        except Exception as e:
            print(f"Cron失败: {e}")
        
        print("\n[4/4] 完成!")
        print("\n✅ 全部功能执行完成")
    
    else:
        print(f"未知命令: {cmd}")
        print("可用命令:", list(commands.keys()))
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
