#!/usr/bin/env python3
"""
尝试使用Selenium和ChromeDriver访问目标网站
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_chrome_options():
    """设置Chrome选项"""
    chrome_options = Options()
    
    # 添加常用参数
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 模拟真实浏览器
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # 禁用自动化特征
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    return chrome_options

def test_cloudflare_site():
    """测试访问Cloudflare保护的网站"""
    url = "https://cf.2hg.com/?action=mc"
    
    print(f"尝试访问: {url}")
    print("正在启动Chrome浏览器...")
    
    try:
        # 设置Chrome选项
        chrome_options = setup_chrome_options()
        
        # 尝试使用chromium-browser
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        
        # 创建driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # 访问网站
        driver.get(url)
        
        print("页面已加载")
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 等待一段时间，看是否有验证页面
        time.sleep(5)
        
        # 检查页面内容
        page_source = driver.page_source
        if "cloudflare" in page_source.lower() or "challenge" in page_source.lower():
            print("检测到Cloudflare验证页面")
            
            # 尝试截图
            screenshot_path = "/tmp/cloudflare_challenge.png"
            driver.save_screenshot(screenshot_path)
            print(f"已保存截图: {screenshot_path}")
            
            # 保存页面HTML用于分析
            html_path = "/tmp/cloudflare_page.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page_source)
            print(f"已保存页面HTML: {html_path}")
            
        # 获取cookies
        cookies = driver.get_cookies()
        print(f"\n获取到的Cookies ({len(cookies)}个):")
        for cookie in cookies:
            print(f"  {cookie['name']}: {cookie['value'][:50]}...")
        
        # 保存cookies到文件
        cookies_path = "/tmp/cookies.json"
        with open(cookies_path, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"\nCookies已保存到: {cookies_path}")
        
        # 保持浏览器打开，让用户查看
        print("\n浏览器保持打开状态...")
        print("请手动检查页面并完成人机验证（如果需要）")
        print("按Ctrl+C停止脚本")
        
        # 等待用户操作
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"访问网站时出错: {e}")
        print(f"错误类型: {type(e).__name__}")
        
        # 检查是否缺少ChromeDriver
        if "chromedriver" in str(e).lower():
            print("\n可能需要安装ChromeDriver:")
            print("1. sudo apt-get install chromium-chromedriver")
            print("2. 或从 https://chromedriver.chromium.org/ 下载")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("\n浏览器已关闭")

if __name__ == "__main__":
    test_cloudflare_site()