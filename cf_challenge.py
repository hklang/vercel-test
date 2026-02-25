#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# 创建driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # 访问页面
    print("访问页面: https://cf.2hg.com/?action=mc")
    driver.get("https://cf.2hg.com/?action=mc")
    
    # 等待页面加载
    time.sleep(5)
    
    # 检查当前URL和标题
    print(f"当前URL: {driver.current_url}")
    print(f"页面标题: {driver.title}")
    
    # 获取所有cookies
    cookies = driver.get_cookies()
    print(f"\n获取到的Cookies ({len(cookies)}个):")
    for cookie in cookies:
        print(f"  {cookie['name']}: {cookie['value']}")
    
    # 将cookies保存到文件
    with open('selenium_cookies.txt', 'w') as f:
        for cookie in cookies:
            f.write(f"{cookie['name']}={cookie['value']}\n")
    
    # 截图
    print("\n正在截图...")
    driver.save_screenshot('cf_challenge_screenshot.png')
    print("截图已保存: cf_challenge_screenshot.png")
    
    # 获取页面源代码
    page_source = driver.page_source
    with open('cf_page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("页面源代码已保存: cf_page_source.html")
    
except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # 关闭浏览器
    driver.quit()
    print("\n浏览器已关闭")