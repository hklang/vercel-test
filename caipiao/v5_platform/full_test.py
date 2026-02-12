#!/usr/bin/env python3
"""完整自我验证测试 - V5.0"""

import sys
import json

class SelfTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name, func):
        self.tests.append((name, func))
    
    def run(self):
        print("=" * 70)
        print("七乐彩预测平台 V5.0 - 完整自我验证")
        print("=" * 70)
        print()
        
        for i, (name, func) in enumerate(self.tests, 1):
            status = "⏳"
            try:
                result = func()
                if result:
                    self.passed += 1
                    status = "✅"
                else:
                    self.failed += 1
                    status = "❌"
            except Exception as e:
                self.failed += 1
                status = f"❌ ({e})"
            
            print(f"{status} [{i:2d}/{len(self.tests)}] {name}")
        
        print()
        print("=" * 70)
        print(f"结果: {self.passed} 通过, {self.failed} 失败")
        print("=" * 70)
        
        if self.failed == 0:
            print("🎉 所有测试通过!")
            return True
        else:
            print("⚠️ 部分测试失败")
            return False

# 测试函数
def test_imports():
    try:
        import json
        from collections import Counter
        return True
    except:
        return False

def test_load_history():
    from prediction.engine_v5 import PredictionEngineV5
    engine = PredictionEngineV5()
    return len(engine.history) > 0

def test_analyze():
    from prediction.engine_v5 import PredictionEngineV5
    engine = PredictionEngineV5()
    engine.analyze()
    return len(engine.hot_numbers) > 0 and len(engine.missing_values) > 0

def test_constraints():
    from prediction.engine_v5 import PredictionEngineV5
    engine = PredictionEngineV5()
    # 有效预测
    valid = [1, 5, 10, 15, 18, 22, 25]  # 3奇4偶
    # 无效预测（6奇1偶）
    invalid = [1, 3, 5, 7, 9, 11, 13]
    return engine.check_constraints(valid) and not engine.check_constraints(invalid)

def test_generate_predictions():
    from prediction.engine_v5 import PredictionEngineV5
    engine = PredictionEngineV5()
    predictions = engine.generate_predictions(10)
    return len(predictions) == 10

def test_save_predictions():
    from prediction.engine_v5 import PredictionEngineV5
    engine = PredictionEngineV5()
    predictions = [[1, 5, 10, 15, 18, 22, 25]]
    return engine.save_predictions(predictions, '/tmp/test_predictions.csv')

def test_generate_report():
    from prediction.engine_v5 import PredictionEngineV5
    engine = PredictionEngineV5()
    report = engine.generate_report()
    return len(report) > 100 and "热号" in report

def test_constraint_checker():
    from prediction.constraint_checker import ConstraintChecker
    c = ConstraintChecker()
    return c.check([1, 5, 10, 15, 18, 22, 25])

def test_frequency_features():
    from feature_layer.frequency_features import FrequencyFeatures
    history = [{'basic_numbers': ['01', '05', '09', '12', '15', '18', '22']}]
    f = FrequencyFeatures(history)
    result = f.extract()
    return len(result) > 0

def test_missing_features():
    from feature_layer.missing_features import MissingFeatures
    history = [{'basic_numbers': ['01', '05', '09', '12', '15', '18', '22']}]
    m = MissingFeatures(history)
    result = m.extract()
    return 'missing_1' in result

def test_pure_rf():
    from models.pure_rf import PurePythonRandomForest
    history = [
        [1, 5, 9, 12, 15, 18, 22],
        [2, 6, 10, 13, 16, 19, 23],
    ]
    model = PurePythonRandomForest(n_trees=3, max_depth=2)
    model.fit(history[:-1], history[1:])
    pred = model.predict(history)
    return len(pred) == 7

def test_cron_scheduler():
    from automation.cron_scheduler import CronScheduler
    s = CronScheduler()
    s.add_task("测试", "0 0 * * *", "echo test")
    return len(s.tasks) == 1

def test_api_server():
    from api.api_server import PredictionAPI
    api = PredictionAPI()
    status = api.get_status()
    return 'status' in status

def test_report_generator():
    from output.report_generator import ReportGenerator
    g = ReportGenerator()
    if not g.load_history():
        print(" (跳过，无历史数据)")
        return True
    report = g.generate_daily_report()
    return len(report) > 100

def main():
    tester = SelfTester()
    
    # 添加测试
    tester.add_test("基础导入", test_imports)
    tester.add_test("加载历史数据", test_load_history)
    tester.add_test("数据分析", test_analyze)
    tester.add_test("约束检查器", test_constraints)
    tester.add_test("生成预测", test_generate_predictions)
    tester.add_test("保存预测", test_save_predictions)
    tester.add_test("生成报告", test_generate_report)
    tester.add_test("频率特征", test_frequency_features)
    tester.add_test("遗漏特征", test_missing_features)
    tester.add_test("纯Python随机森林", test_pure_rf)
    tester.add_test("Cron调度器", test_cron_scheduler)
    tester.add_test("API服务", test_api_server)
    tester.add_test("报告生成器", test_report_generator)
    
    return tester.run()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
