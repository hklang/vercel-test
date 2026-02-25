#!/usr/bin/env python3
"""
CF人机验证手动验证脚本
使用昨天成功的方法：打开浏览器，等待人工点击验证
"""

import asyncio
from playwright.async_api import async_playwright
import time

async def manual_cf_verification():
    """手动CF验证方法"""
    print("🚀 启动浏览器进行CF人机验证...")
    print("📌 使用昨天成功的方法：打开浏览器 -> 等待人工交互")
    
    async with async_playwright() as p:
        # 启动浏览器（非无头模式，可以看到界面）
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        
        # 创建上下文
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 创建页面
        page = await context.new_page()
        
        try:
            # 访问CF验证页面
            print("🌐 访问CF验证页面: https://cf.2hg.com/?action=mc")
            await page.goto('https://cf.2hg.com/?action=mc', wait_until='networkidle')
            
            # 获取页面标题
            title = await page.title()
            print(f"📄 页面标题: {title}")
            
            # 检查页面内容
            content = await page.content()
            if 'Just a moment' in content or '请稍候' in content:
                print("⚠️ 检测到CF验证页面")
                print("👆 请在浏览器窗口中手动完成验证（点击验证按钮）")
                print("⏳ 等待人工交互...")
                
                # 等待人工交互（最长等待5分钟）
                start_time = time.time()
                timeout = 300  # 5分钟
                
                while time.time() - start_time < timeout:
                    # 检查页面是否变化
                    current_title = await page.title()
                    current_url = page.url
                    
                    if 'it works' in current_title or 'cf.2hg.com' not in current_url:
                        print(f"✅ 验证成功！页面标题: {current_title}")
                        print(f"🔗 当前URL: {current_url}")
                        break
                    
                    # 检查是否有cf_clearance cookie
                    cookies = await context.cookies()
                    cf_cookies = [c for c in cookies if 'cf_clearance' in c['name']]
                    if cf_cookies:
                        print(f"🍪 找到cf_clearance cookie: {cf_cookies[0]['value'][:20]}...")
                        print("✅ 验证成功！")
                        break
                    
                    # 等待5秒再检查
                    await asyncio.sleep(5)
                    elapsed = int(time.time() - start_time)
                    print(f"⏱️ 已等待 {elapsed} 秒...")
                
                else:
                    print("⏰ 等待超时，验证可能未完成")
            
            # 获取最终状态
            print("\n📊 最终状态检查:")
            print(f"📄 页面标题: {await page.title()}")
            print(f"🔗 当前URL: {page.url}")
            
            # 获取所有cookies
            cookies = await context.cookies()
            print(f"🍪 Cookies数量: {len(cookies)}")
            
            # 显示cf_clearance cookie
            cf_cookies = [c for c in cookies if 'cf_clearance' in c['name']]
            if cf_cookies:
                for cookie in cf_cookies:
                    print(f"✅ cf_clearance: {cookie['value'][:30]}... (过期时间: {cookie.get('expires', '无')})")
            else:
                print("❌ 未找到cf_clearance cookie")
            
            # 截图保存
            screenshot_path = 'cf_verification_result.png'
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 截图已保存: {screenshot_path}")
            
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        
        finally:
            # 询问是否关闭浏览器
            print("\n❓ 是否关闭浏览器？(y/n)")
            response = input().strip().lower()
            if response == 'y':
                await browser.close()
                print("👋 浏览器已关闭")
            else:
                print("💻 浏览器保持打开状态，可以继续操作")
                print("🔗 浏览器URL:", page.url)

if __name__ == '__main__':
    asyncio.run(manual_cf_verification())