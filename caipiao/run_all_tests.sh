#!/bin/bash
# 完整测试脚本

echo "=========================================="
echo "七乐彩预测平台 - 全阶段自我验证"
echo "=========================================="

tests=(
    "v5_platform/data_layer/data_collector.py:数据采集器"
    "v5_platform/data_layer/data_cleaner.py:数据清洗器"
    "v5_platform/feature_layer/frequency_features.py:频率特征"
    "v5_platform/feature_layer/missing_features.py:遗漏特征"
    "v5_platform/prediction/constraint_checker.py:约束检查"
)

all_passed=true

for test in "${tests[@]}"; do
    IFS=: read -r file desc <<< "$test"
    echo ""
    echo "测试: $desc"
    echo "文件: $file"
    echo "----------------------------------------"
    
    if python3 "$file"; then
        echo "✅ $desc 通过"
    else
        echo "❌ $desc 失败"
        all_passed=false
    fi
done

echo ""
echo "=========================================="
if $all_passed; then
    echo "🎉 所有测试通过！"
    exit 0
else
    echo "⚠️ 部分测试失败"
    exit 1
fi
