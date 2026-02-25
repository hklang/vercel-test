#!/usr/bin/env python3
"""
测试CF人机验证自动化方法
网址: https://cf.2hg.com/?action=mc
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_direct_request():
    """测试直接HTTP请求"""
    print("=== 测试直接HTTP请求 ===")
    url = "https://cf.2hg.com/?action=mc"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    proxies = {
        'http': 'socks5://127.0.0.1:20170',
        'https': 'socks5://127.0.0.1:20170'
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        print(f"状态码: {response.status_code}")
        print(f"响应头:")
        for key, value in response.headers.items():
            if 'cf-' in key.lower() or 'cloudflare' in key.lower():
                print(f"  {key}: {value}")
        
        # 检查是否有验证页面
        if response.status_code == 403:
            print("⚠️ 检测到CloudFlare验证 (403)")
            return False
        elif response.status_code == 200:
            print("✅ 可能绕过验证")
            return True
        else:
            print(f"❓ 未知状态: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_selenium_automation():
    """测试Selenium自动化"""
    print("\n=== 测试Selenium自动化 ===")
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280,800')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # 添加代理设置
    chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:20170')
    
    # 尝试绕过自动化检测
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # 执行CDP命令来隐藏自动化特征
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })
        
        print("🌐 访问CF验证页面...")
        driver.get("https://cf.2hg.com/?action=mc")
        
        # 等待页面加载
        time.sleep(5)
        
        print(f"当前URL: {driver.current_url}")
        print(f"页面标题: {driver.title}")
        
        # 检查页面内容
        page_source = driver.page_source
        if "challenge" in page_source.lower() or "cloudflare" in page_source.lower():
            print("⚠️ 检测到CloudFlare验证页面")
            
            # 截图保存
            driver.save_screenshot('cf_selenium_challenge.png')
            print("📸 截图已保存: cf_selenium_challenge.png")
            
            # 尝试查找验证元素
            try:
                # 查找可能的验证元素
                elements = driver.find_elements(By.TAG_NAME, 'div')
                for elem in elements[:10]:
                    text = elem.text.strip()
                    if text and len(text) > 0:
                        print(f"页面文本: {text[:100]}...")
                        
            except Exception as e:
                print(f"查找元素时出错: {e}")
            
            driver.quit()
            return False
        else:
            print("✅ 可能成功访问页面")
            driver.quit()
            return True
            
    except Exception as e:
        print(f"❌ Selenium测试失败: {e}")
        return False

def test_cf_clearance_cookie():
    """测试使用已有的cf_clearance cookie"""
    print("\n=== 测试使用已有Cookie ===")
    
    # 尝试读取之前保存的cookie
    try:
        with open('selenium_cookies.txt', 'r') as f:
            cookies = f.readlines()
        
        print(f"找到 {len(cookies)} 个cookie")
        
        # 解析cookie
        cookie_dict = {}
        for line in cookies:
            if '=' in line:
                name, value = line.strip().split('=', 1)
                cookie_dict[name] = value
                print(f"  {name}: {value[:50]}...")
        
        if 'cf_clearance' in cookie_dict:
            print("✅ 找到cf_clearance cookie")
            return True
        else:
            print("❌ 未找到cf_clearance cookie")
            return False
            
    except FileNotFoundError:
        print("❌ 未找到cookie文件")
        return False

def main():
    """主函数"""
    print("🔍 开始测试CF人机验证自动化方法")
    print(f"目标网址: https://cf.2hg.com/?action=mc")
    print("-" * 50)
    
    # 测试1: 直接HTTP请求
    method1_success = test_direct_request()
    
    # 测试2: 检查已有cookie
    method2_success = test_cf_clearance_cookie()
    
    # 测试3: Selenium自动化
    method3_success = test_selenium_automation()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"1. 直接HTTP请求: {'✅ 成功' if method1_success else '❌ 失败'}")
    print(f"2. 使用已有Cookie: {'✅ 可用' if method2_success else '❌ 不可用'}")
    print(f"3. Selenium自动化: {'✅ 成功' if method3_success else '❌ 失败'}")
    
    print("\n💡 建议:")
    if method2_success:
        print("  - 可以使用已有的cf_clearance cookie来绕过验证")
    else:
        print("  - 需要人工完成一次验证来获取cf_clearance cookie")
        print("  - 验证后，cookie通常有效2-24小时")
    
    print("  - CloudFlare的Managed Challenge需要真实人工交互")
    print("  - 自动化工具只能辅助，不能完全替代人工验证")

if __name__ == "__main__":
    main()