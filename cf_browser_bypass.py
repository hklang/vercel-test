#!/usr/bin/env python3
"""
CF人机验证 - 使用浏览器自动化
使用Selenium WebDriver来自动完成CF验证

依赖安装:
    pip install selenium webdriver-manager

使用方法:
    python cf_browser_bypass.py
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CFBrowserBypass:
    def __init__(self):
        self.url = "https://cf.2hg.com/?action=mc"
        self.cookies_file = "cf_browser_cookies.json"
        self.screenshot_file = "cf_browser_screenshot.png"
        
    def setup_driver(self):
        """配置Chrome WebDriver"""
        print("🔧 配置Chrome WebDriver...")
        
        chrome_options = Options()
        
        # 基础设置
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280,800')
        
        # 代理设置（使用v2rayA）
        chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:20170')
        
        # 反检测设置
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        try:
            # 使用webdriver-manager自动下载和管理chromedriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 执行CDP命令隐藏webdriver
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['zh-CN', 'zh', 'en']
                    });
                '''
            })
            
            print("✅ Chrome WebDriver 配置成功")
            return driver
            
        except Exception as e:
            print(f"❌ 配置失败: {e}")
            return None
    
    def detect_challenge(self, driver):
        """检测页面是否有CF验证"""
        print("\n🔍 检测CF验证...")
        
        # 检查URL
        if "challenge" in driver.current_url.lower():
            print("⚠️ 检测到挑战页面")
            return True
        
        # 检查页面标题
        if "cloudflare" in driver.title.lower() or "challenge" in driver.title.lower():
            print("⚠️ 页面标题包含验证信息")
            return True
        
        # 检查页面内容
        page_source = driver.page_source.lower()
        challenge_indicators = [
            'cf-challenge',
            'cf-turnstile', 
            'challenges.cloudflare.com',
            'cloudflare challenge',
            'checking your browser',
            'please wait'
        ]
        
        for indicator in challenge_indicators:
            if indicator in page_source:
                print(f"⚠️ 检测到验证标识: {indicator}")
                return True
        
        print("✅ 未检测到CF验证")
        return False
    
    def wait_for_challenge(self, driver, timeout=30):
        """等待CF验证完成"""
        print(f"⏳ 等待验证完成（超时 {timeout}秒）...")
        
        start_time = time.time()
        check_count = 0
        
        while time.time() - start_time < timeout:
            check_count += 1
            print(f"  检查 #{check_count}...", end=" ")
            
            # 检查是否还有验证
            if not self.detect_challenge(driver):
                print("✅ 验证似乎已通过!")
                return True
            
            # 检查URL是否变化
            print(f"URL: {driver.current_url[:50]}...")
            
            time.sleep(2)
        
        print("⏰ 等待超时")
        return False
    
    def try_solve_challenge(self, driver):
        """尝试自动解决验证"""
        print("\n🛠️ 尝试自动解决验证...")
        
        # 尝试查找并点击验证iframe
        try:
            # 查找可能的验证元素
            iframes = driver.find_elements(By.TAG_NAME, 'iframe')
            print(f"  找到 {len(iframes)} 个iframe")
            
            for i, iframe in enumerate(iframes):
                try:
                    src = iframe.get_attribute('src')
                    if src and 'cloudflare' in src:
                        print(f"  iframe {i}: {src[:80]}...")
                except:
                    pass
            
        except Exception as e:
            print(f"  查找iframe时出错: {e}")
        
        # 尝试查找turnstile元素
        try:
            turnstile = driver.find_elements(By.CLASS_NAME, 'cf-turnstile')
            if turnstile:
                print("  找到Turnstile验证元素")
                # Turnstile通常自动处理
        except:
            pass
        
        # 尝试查找验证按钮
        try:
            # 常见的验证按钮
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button[type="button"], input[type="checkbox"]')
            for btn in buttons:
                try:
                    text = btn.text.lower()
                    if 'verify' in text or 'challenge' in text or '确认' in text:
                        print(f"  点击验证按钮: {btn.text}")
                        btn.click()
                        time.sleep(2)
                except:
                    pass
        except:
            pass
    
    def save_cookies(self, driver):
        """保存Cookie到文件"""
        print("\n💾 保存Cookie...")
        
        try:
            cookies = driver.get_cookies()
            
            # 保存为JSON格式
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            
            print(f"✅ 保存了 {len(cookies)} 个cookie")
            
            # 显示关键cookie
            for cookie in cookies:
                if 'cf' in cookie['name'].lower():
                    print(f"  🔑 {cookie['name']}: {cookie['value'][:50]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ 保存cookie失败: {e}")
            return False
    
    def save_screenshot(self, driver, filename=None):
        """保存截图"""
        if filename is None:
            filename = self.screenshot_file
        
        try:
            driver.save_screenshot(filename)
            print(f"📸 截图已保存: {filename}")
            return True
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return False
    
    def load_cookies(self):
        """从文件加载Cookie"""
        if not os.path.exists(self.cookies_file):
            return None
        
        try:
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
            print(f"✅ 加载了 {len(cookies)} 个cookie")
            return cookies
        except Exception as e:
            print(f"❌ 加载cookie失败: {e}")
            return None
    
    def run(self):
        """运行主流程"""
        print("="*60)
        print("🚀 CF人机验证自动化工具")
        print(f"目标: {self.url}")
        print("="*60)
        
        # 1. 设置WebDriver
        driver = self.setup_driver()
        if not driver:
            return False
        
        try:
            # 2. 访问目标页面
            print(f"\n🌐 访问页面: {self.url}")
            driver.get(self.url)
            
            # 等待页面加载
            time.sleep(5)
            
            # 3. 截图
            self.save_screenshot(driver, "cf_initial.png")
            
            # 4. 检测验证
            has_challenge = self.detect_challenge(driver)
            
            if has_challenge:
                print("\n⚠️ 检测到CF验证!")
                
                # 5. 尝试自动解决
                self.try_solve_challenge(driver)
                
                # 6. 等待验证完成（给用户时间手动验证）
                print("\n⏳ 等待验证完成...")
                print("   如果浏览器窗口可见，请手动完成验证")
                print("   等待60秒...")
                time.sleep(60)
                
                # 7. 再次检测
                has_challenge = self.detect_challenge(driver)
                
                if not has_challenge:
                    print("\n✅ 验证通过!")
                else:
                    print("\n⚠️ 验证可能仍在进行中")
                
                # 8. 保存Cookie
                self.save_cookies(driver)
                
            else:
                print("\n✅ 页面无需验证，直接访问成功!")
                self.save_cookies(driver)
            
            # 9. 最终截图
            self.save_screenshot(driver, "cf_final.png")
            
            # 10. 显示结果
            print("\n" + "="*60)
            print("📊 结果:")
            print(f"  当前URL: {driver.current_url}")
            print(f"  页面标题: {driver.title}")
            print(f"  Cookie文件: {self.cookies_file}")
            print(f"  截图文件: cf_initial.png, cf_final.png")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 运行时错误: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            # 保持浏览器打开，让用户可以手动操作
            print("\n💡 浏览器保持打开状态，请手动完成验证")
            print("   完成后可以手动保存cookie或直接关闭浏览器")
            # driver.quit()  # 注释掉这行，让浏览器保持打开

if __name__ == "__main__":
    bypass = CFBrowserBypass()
    bypass.run()
