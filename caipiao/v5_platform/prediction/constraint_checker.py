#!/usr/bin/env python3
"""约束检查器"""

from typing import List

class ConstraintChecker:
    def check_parity(self, numbers: List[int]) -> bool:
        odd = sum(1 for n in numbers if n % 2 == 1)
        return 2 <= odd <= 5  # 放宽到2-5个奇数
    
    def check_size(self, numbers: List[int]) -> bool:
        small = sum(1 for n in numbers if n <= 10)
        medium = sum(1 for n in numbers if 11 <= n <= 20)
        large = sum(1 for n in numbers if n >= 21)
        # 放宽条件：只要不是极端分布
        return small <= 4 and medium <= 4 and large <= 4
    
    def check(self, numbers: List[int]) -> bool:
        return self.check_parity(numbers) and self.check_size(numbers)

def main():
    c = ConstraintChecker()
    test = [1, 5, 10, 15, 18, 22, 25]
    return c.check(test)

if __name__ == '__main__':
    success = main()
    print("✅ 约束检查器测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
