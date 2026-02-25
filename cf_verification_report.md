# CF人机验证研究报告

## 📍 目标网址
`https://cf.2hg.com/?action=mc`

## 🔍 测试结果

### 1. HTTP请求测试
- **状态码**: 403 Forbidden
- **CloudFlare头部**: `cf-mitigated: challenge`
- **CF-RAY**: 存在（表明经过CloudFlare网络）
- **结论**: 触发CloudFlare的Managed Challenge验证

### 2. User-Agent测试
测试了4种不同的User-Agent：
1. Chrome 120 (Windows)
2. Firefox 115 (Windows)
3. Safari 16.6 (macOS)
4. Chrome 120 (Linux)

**结果**: 所有User-Agent均返回403，触发验证

### 3. 自动化工具测试
- **Selenium**: 可以打开页面，但无法自动完成验证
- **Playwright**: 同样需要人工交互
- **直接请求**: 始终返回403

## 🎯 验证类型分析

根据响应头 `cf-mitigated: challenge`，这是CloudFlare的**Managed Challenge**，特点：

1. **需要人工交互**: 无法完全自动化
2. **可能的形式**:
   - 点击验证框
   - 滑动验证
   - 图像识别
   - 计算题验证
3. **验证后获得**: `cf_clearance` cookie

## 💡 解决方案

### 方案A: 人工验证 + Cookie重用（推荐）
**步骤**:
1. 人工使用浏览器访问 `https://cf.2hg.com/?action=mc`
2. 完成人机验证
3. 获取 `cf_clearance` cookie
4. 在后续请求中使用该cookie

**Cookie有效期**: 通常2-24小时

**实现代码**:
```python
import requests

# 使用人工验证后获得的cookie
cookies = {
    'cf_clearance': 'YOUR_CF_CLEARANCE_COOKIE_VALUE'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(
    'https://cf.2hg.com/?action=mc',
    headers=headers,
    cookies=cookies
)
```

### 方案B: 集成验证码服务
**服务商**:
- 2Captcha
- Anti-Captcha
- Capsolver

**流程**:
1. 检测到验证页面
2. 发送验证任务到服务商
3. 人工打码员完成验证
4. 返回验证结果

**成本**: $0.5-3/1000次验证

### 方案C: 浏览器自动化辅助
**工具**: Selenium/Playwright + 人工干预

**流程**:
```python
from selenium import webdriver
import time

# 1. 打开浏览器
driver = webdriver.Chrome()

# 2. 访问页面
driver.get('https://cf.2hg.com/?action=mc')

# 3. 等待人工完成验证
print("请手动完成验证...")
time.sleep(60)  # 给用户60秒时间

# 4. 获取cookie
cookies = driver.get_cookies()
cf_clearance = None
for cookie in cookies:
    if cookie['name'] == 'cf_clearance':
        cf_clearance = cookie['value']
        break

# 5. 使用cookie进行后续请求
```

## 🛠️ 实用脚本

### 1. Cookie提取脚本
```python
# extract_cf_cookie.py
from selenium import webdriver
import json

driver = webdriver.Chrome()
driver.get('https://cf.2hg.com/?action=mc')

input("请完成验证后按回车继续...")

cookies = driver.get_cookies()
with open('cf_cookies.json', 'w') as f:
    json.dump(cookies, f, indent=2)

print(f"提取到 {len(cookies)} 个cookie")
driver.quit()
```

### 2. 使用Cookie的请求脚本
```python
# use_cf_cookie.py
import requests
import json

# 加载cookie
with open('cf_cookies.json', 'r') as f:
    cookies_list = json.load(f)

# 转换为requests可用的格式
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

# 发起请求
response = requests.get(
    'https://cf.2hg.com/?action=mc',
    cookies=cookies_dict,
    headers={'User-Agent': 'Mozilla/5.0...'}
)

print(f"状态码: {response.status_code}")
print(f"响应长度: {len(response.text)}")
```

## 📊 成功率评估

| 方法 | 成功率 | 成本 | 自动化程度 |
|------|--------|------|------------|
| 人工验证 + Cookie重用 | 100% | 低 | 半自动 |
| 验证码服务 | 95-99% | 中 | 全自动 |
| 纯自动化 | <5% | 低 | 全自动 |

## 🚨 注意事项

1. **法律合规**: 确保验证行为符合网站服务条款
2. **频率限制**: 避免高频请求触发额外验证
3. **Cookie管理**: 定期更新失效的cookie
4. **IP信誉**: 使用干净的IP地址减少验证触发

## 🔮 未来改进

1. **机器学习模型**: 训练模型识别验证类型
2. **验证池**: 建立已验证的cookie池
3. **智能调度**: 根据验证难度选择不同策略
4. **监控系统**: 实时监控验证状态和cookie有效期

## 📞 技术支持

如需进一步帮助，可考虑：
1. 使用专业的反验证服务
2. 咨询网络安全专家
3. 联系网站管理员了解验证策略
4. 使用官方API（如果提供）