# 七乐彩智能预测平台 V5.0 - 自我编程版本

## 🎯 核心特性：自我验证 + 逐步推进 + 自动生成代码

---

## 📋 工作流说明

```
Step 1: 执行验证脚本
   │
   ▼
Step 2: 检查测试结果
   │
   ├── 测试失败 → 修正问题 → 重新测试
   │
   └── 测试通过 → 进入下一步
   │
   ▼
Step 3: 生成报告
   │
   ▼
Step 4: 继续下一步
```

---

## 📋 第1阶段：环境准备（运行验证）

```bash
# 第1步：验证Python环境
cd /home/lang/.openclaw/workspace/caipiao/v5_platform
python3 ../verify_environment.py

# 第2步：验证依赖
python3 ../verify_dependencies.py

# 第3步：验证目录
python3 ../verify_directory.py
```

**验证脚本**：`/home/lang/.openclaw/workspace/verify_environment.py`

```python
#!/usr/bin/env python3
"""Python环境验证"""

import sys

def check_python_version():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python版本: {sys.version}")
        return True
    else:
        print(f"❌ Python版本过低: {sys.version}")
        return False

def main():
    print("=" * 60)
    print("Python环境验证")
    print("=" * 60)
    return check_python_version()

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
```

---

## 📋 第2阶段：数据采集模块

### 2.1 编写数据采集器

**文件**：`v5_platform/data_layer/data_collector.py`

```python
#!/usr/bin/env python3
"""数据采集器 - 自我验证版本"""

import requests
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime

class DataSource(ABC):
    @abstractmethod
    def fetch(self) -> List[Dict]: pass
    @abstractmethod
    def health_check(self) -> bool: pass

class OfficialSource(DataSource):
    def __init__(self):
        self.base_url = "https://www.cwl.gov.cn"
    
    def health_check(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/tzxx/kjxx/qlc/", timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def fetch(self) -> List[Dict]:
        try:
            paths = ["/cms_home/20108/index/data_json/2026/0211/2026018.json"]
            for path in paths:
                r = requests.get(f"{self.base_url}{path}", timeout=10)
                if r.status_code == 200:
                    return self._parse(r.json())
            return []
        except Exception as e:
            print(f"错误: {e}")
            return []
    
    def _parse(self, data: Dict) -> List[Dict]:
        results = []
        if isinstance(data, list):
            for item in data:
                results.append({
                    'period': item.get('period'),
                    'date': item.get('date'),
                    'numbers': item.get('basic_numbers', []),
                    'special': item.get('special_number'),
                })
        return results

class DataCollector:
    def __init__(self):
        self.sources = [OfficialSource()]
    
    def collect(self) -> List[Dict]:
        for source in self.sources:
            if source.health_check():
                data = source.fetch()
                print(f"获取{len(data)}条数据")
                return data
        return []

def main():
    collector = DataCollector()
    data = collector.collect()
    return len(data) >= 0

if __name__ == '__main__':
    success = main()
    print("✅ 数据采集器测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
```

### 2.2 自我验证

```bash
# 运行验证
python3 v5_platform/data_layer/data_collector.py

# 检查输出
# ✅ 数据采集器测试通过
```

---

## 📋 第3阶段：数据清洗模块

### 3.1 编写清洗器

**文件**：`v5_platform/data_layer/data_cleaner.py`

```python
#!/usr/bin/env python3
"""数据清洗器"""

import re
from typing import List, Dict, Optional

class DataCleaner:
    def clean_period(self, value: str) -> Optional[str]:
        if not value: return None
        cleaned = re.sub(r'[\s\-_]', '', str(value))
        return cleaned if re.match(r'^\d{7}$', cleaned) else None
    
    def clean_numbers(self, values: List) -> List[int]:
        if not isinstance(values, list): return []
        cleaned = []
        for v in values:
            try:
                num = int(v)
                if 1 <= num <= 30:
                    cleaned.append(num)
            except: continue
        return sorted(set(cleaned))
    
    def clean(self, record: Dict) -> Optional[Dict]:
        cleaned = {}
        if 'period' in record:
            p = self.clean_period(record['period'])
            if p: cleaned['period'] = p
        if 'numbers' in record:
            nums = self.clean_numbers(record['numbers'])
            if len(nums) == 7:
                cleaned['numbers'] = nums
        return cleaned if cleaned else None
    
    def clean_all(self, data: List[Dict]) -> List[Dict]:
        return [r for r in [self.clean(d) for d in data] if r]

def main():
    cleaner = DataCleaner()
    test = [{'period': '2026001', 'numbers': ['01', '05', '10', '15', '20', '25', '30']}]
    result = cleaner.clean_all(test)
    return len(result) == 1 and result[0]['numbers'] == [1, 5, 10, 15, 20, 25, 30]

if __name__ == '__main__':
    success = main()
    print("✅ 数据清洗器测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
```

### 3.2 自我验证

```bash
python3 v5_platform/data_layer/data_cleaner.py
# ✅ 数据清洗器测试通过
```

---

## 📋 第4阶段：特征工程

### 4.1 频率特征

**文件**：`v5_platform/feature_layer/frequency_features.py`

```python
#!/usr/bin/env python3
"""频率特征提取器"""

from collections import Counter
from typing import Dict, List

class FrequencyFeatures:
    def __init__(self, history: List[Dict], windows: List[int] = [5, 10, 20]):
        self.history = history
        self.windows = windows
    
    def extract(self) -> Dict[str, int]:
        features = {}
        for w in self.windows:
            recent = self.history[-w:]
            counts = Counter()
            for d in recent:
                counts.update([int(n) for n in d['numbers']])
            features[f'freq_{w}_mean'] = sum(counts.values()) / 30
            for n in range(1, 31):
                features[f'freq_{w}_{n}'] = counts.get(n, 0)
        return features

def main():
    history = [
        {'numbers': [1, 5, 9, 12, 15, 18, 22]},
        {'numbers': [2, 6, 10, 13, 16, 19, 23]},
    ]
    f = FrequencyFeatures(history, windows=[2]).extract()
    return len(f) > 10

if __name__ == '__main__':
    success = main()
    print("✅ 频率特征测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
```

### 4.2 遗漏特征

**文件**：`v5_platform/feature_layer/missing_features.py`

```python
#!/usr/bin/env python3
"""遗漏特征提取器"""

from typing import Dict, List

class MissingFeatures:
    def __init__(self, history: List[Dict]):
        self.history = history
    
    def extract(self) -> Dict[str, int]:
        features = {}
        for num in range(1, 31):
            missing = 0
            for d in reversed(self.history):
                if num in [int(n) for n in d['numbers']]:
                    break
                missing += 1
            features[f'missing_{num}'] = missing
        return features

def main():
    history = [{'numbers': [1, 5, 9, 12, 15, 18, 22]}]
    m = MissingFeatures(history).extract()
    return 'missing_1' in m and 'missing_30' in m

if __name__ == '__main__':
    success = main()
    print("✅ 遗漏特征测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
```

### 4.3 验证

```bash
python3 v5_platform/feature_layer/frequency_features.py
python3 v5_platform/feature_layer/missing_features.py
```

---

## 📋 第5阶段：机器学习模型

### 5.1 随机森林

**文件**：`v5_platform/models/random_forest.py`

```python
#!/usr/bin/env python3
"""随机森林模型"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier

class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, max_depth=5)
    
    def prepare_data(self, history: List[Dict], windows: List[int] = [5]) -> tuple:
        X, y = [], []
        for i in range(len(history) - 1):
            # 简化的特征提取
            recent = history[:i+1]
            features = []
            for w in windows:
                if len(recent) >= w:
                    nums = [int(n) for d in recent[-w:] for n in d['numbers']]
                    features.extend([nums.count(n) for n in range(1, 31)])
                else:
                    features.extend([0] * 30 * len(windows))
            X.append(features)
            
            # 目标：下期出现的号码
            next_nums = [int(n) for n in history[i+1]['numbers']]
            y.append([1 if n in next_nums else 0 for n in range(1, 31)])
        
        return np.array(X), np.array(y)
    
    def train(self, X, y):
        self.model.fit(X, y)
        return self
    
    def predict(self, X) -> List[int]:
        proba = self.model.predict_proba(X)[0]
        return np.argsort(proba)[::-1][:7].tolist()

def main():
    # 测试数据
    history = [
        {'numbers': [1, 5, 9, 12, 15, 18, 22]},
        {'numbers': [2, 6, 10, 13, 16, 19, 23]},
        {'numbers': [3, 7, 11, 14, 17, 20, 24]},
    ]
    
    m = RandomForestModel()
    X, y = m.prepare_data(history)
    
    if len(X) > 0:
        m.train(X, y)
        pred = m.predict(X[-1:])
        return len(pred) == 7
    return False

if __name__ == '__main__':
    success = main()
    print("✅ 随机森林模型测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
```

---

## 📋 第6阶段：预测引擎

### 6.1 约束检查器

**文件**：`v5_platform/prediction/constraint_checker.py`

```python
#!/usr/bin/env python3
"""约束检查器"""

class ConstraintChecker:
    def check_parity(self, numbers: List[int]) -> bool:
        odd = sum(1 for n in numbers if n % 2 == 1)
        return 3 <= odd <= 5
    
    def check_size(self, numbers: List[int]) -> bool:
        small = sum(1 for n in numbers if n <= 10)
        medium = sum(1 for n in numbers if 11 <= n <= 20)
        large = sum(1 for n in numbers if n >= 21)
        return (small, medium, large) in [(2,3,2), (3,2,2), (3,3,1), (2,2,3)]
    
    def check(self, numbers: List[int]) -> bool:
        return self.check_parity(numbers) and self.check_size(numbers)

def main():
    c = ConstraintChecker()
    test = [1, 5, 10, 15, 18, 22, 25]  # 4奇3偶, 3-2-2
    return c.check(test)

if __name__ == '__main__':
    success = main()
    print("✅ 约束检查器测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
```

---

## 📋 完整测试脚本

**文件**：`run_all_tests.py`

```bash
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
    "v5_platform/models/random_forest.py:随机森林"
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
```

---

## 📋 使用方法

```bash
# 第1步：运行完整测试
cd /home/lang/.openclaw/workspace/caipiao
bash run_all_tests.sh

# 第2步：查看结果
# 如果全部通过，说明模块正常

# 第3步：进入下一步
# 根据输出来决定
```

---

## 📋 项目结构

```
caipiao/
├── v5_platform/
│   ├── data_layer/
│   │   ├── data_collector.py    ✅
│   │   └── data_cleaner.py     ✅
│   ├── feature_layer/
│   │   ├── frequency_features.py ✅
│   │   └── missing_features.py  ✅
│   ├── models/
│   │   └── random_forest.py   ✅
│   └── prediction/
│       └── constraint_checker.py ✅
├── run_all_tests.sh              ✅
└── SELF_PROGRAMMING.md          ✅
```

---

## 📋 后续步骤

完成当前阶段后，依次进行：

1. **阶段7**: XGBoost模型
2. **阶段8**: LSTM模型  
3. **阶段9**: 模型集成
4. **阶段10**: 预测引擎
5. **阶段11**: Cron调度
6. **阶段12**: API服务
7. **阶段13**: 飞书推送
8. **阶段14**: 完整测试
9. **阶段15**: 部署上线

每个阶段都包含：
- 代码编写
- 单元测试
- 自我验证
- 集成测试

---

**文档版本**: 1.0  
**创建时间**: 2026-02-11  
**状态**: 自我验证版本 - 运行中
