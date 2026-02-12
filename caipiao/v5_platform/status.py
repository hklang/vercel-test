#!/usr/bin/env python3
"""项目状态检查 - 修复版"""

import os
import json

def check_file(filepath: str) -> dict:
    """检查文件"""
    base = '/home/lang/.openclaw/workspace/caipiao'
    full_path = os.path.join(base, filepath)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        return {'exists': True, 'size': size}
    return {'exists': False, 'size': 0}

def main():
    print("=" * 70)
    print("七乐彩预测平台 V5.0 - 项目状态")
    print("=" * 70)
    print()
    
    base = '/home/lang/.openclaw/workspace/caipiao'
    
    dirs = [
        'v5_platform/data_layer',
        'v5_platform/feature_layer',
        'v5_platform/models',
        'v5_platform/prediction',
        'v5_platform/automation',
        'v5_platform/api',
        'v5_platform/output',
        'v5_platform/tests',
        'v5_platform/data/raw',
        'v5_platform/data/models',
        'v5_platform/logs',
    ]
    
    print("📁 目录结构:")
    for d in dirs:
        full_path = os.path.join(base, d)
        status = "✅" if os.path.exists(full_path) else "❌"
        print(f"  {status} {d}")
    
    print()
    print("📄 文件列表:")
    
    files = [
        ('v5_platform/data_layer/__init__.py', '数据层初始化'),
        ('v5_platform/data_layer/data_collector.py', '数据采集器'),
        ('v5_platform/data_layer/data_cleaner.py', '数据清洗器'),
        ('v5_platform/feature_layer/__init__.py', '特征层初始化'),
        ('v5_platform/feature_layer/frequency_features.py', '频率特征'),
        ('v5_platform/feature_layer/missing_features.py', '遗漏特征'),
        ('v5_platform/models/__init__.py', '模型层初始化'),
        ('v5_platform/models/random_forest.py', '随机森林'),
        ('v5_platform/models/xgboost.py', 'XGBoost'),
        ('v5_platform/models/lstm.py', 'LSTM'),
        ('v5_platform/models/model_ensemble.py', '模型集成'),
        ('v5_platform/prediction/__init__.py', '预测层初始化'),
        ('v5_platform/prediction/constraint_checker.py', '约束检查器'),
        ('v5_platform/prediction/prediction_engine.py', '预测引擎'),
        ('v5_platform/automation/__init__.py', '自动化层初始化'),
        ('v5_platform/automation/cron_scheduler.py', 'Cron调度器'),
        ('v5_platform/api/__init__.py', 'API层初始化'),
        ('v5_platform/api/api_server.py', 'API服务器'),
        ('v5_platform/output/__init__.py', '输出层初始化'),
        ('v5_platform/output/feishu_sender.py', '飞书推送'),
        ('v5_platform/output/report_generator.py', '报告生成器'),
        ('v5_platform/main.py', '主入口'),
        ('v5_platform/self_test.py', '自我测试'),
        ('run_all_tests.sh', '测试脚本'),
        ('v5_platform/predictions_v5.csv', '预测结果'),
    ]
    
    exists_count = 0
    for filepath, desc in files:
        info = check_file(filepath)
        status = f"✅ {info['size']:5d}B" if info['exists'] else "❌"
        if info['exists']:
            exists_count += 1
        print(f"  {status} {desc}")
    
    print()
    print("=" * 70)
    print(f"📊 状态: {exists_count}/{len(files)} 文件已创建")
    print()
    print("💡 运行完整测试: python3 v5_platform/self_test.py")
    print("💡 生成预测: cd v5_platform && python3 prediction/prediction_engine.py")
    print("💡 启动API: cd v5_platform && python3 api/api_server.py 8080")
    print("=" * 70)

if __name__ == '__main__':
    main()
