#!/usr/bin/env python3
"""
CF人机验证实用演示脚本
演示如何绕过 https://cf.2hg.com/?action=mc 的验证
"""

import requests
import json
import time
import os

class CFVerificationDemo:
    def __init__(self):
        self.url = "https://cf.2hg.com/?action=mc"
        self.proxies = {
            'http': 'socks5://127.0.0.1:20170',
            'https': 'socks5://127.0.0.1:20170'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    def test_without_cookie(self):
        """测试无cookie访问"""
        print("🔍 测试无cookie访问...")
        try:
            response = requests.get(
                self.url, 
                headers=self.headers, 
                proxies=self.proxies,
                timeout=10
            )
            print(f"  状态码: {response.status_code}")
            
            # 检查CloudFlare头部
            for key, value in response.headers.items():
                if 'cf-' in key.lower():
                    print(f"  {key}: {value}")
            
            if response.status_code == 403:
                print("  ❌ 被CloudFlare阻止")
                return False
            elif response.status_code == 200:
                print("  ✅ 成功访问")
                return True
                
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
            return False
    
    def load_cookies_from_file(self, filename="cf_cookies.json"):
        """从文件加载cookie"""
        print(f"\n📂 尝试从 {filename} 加载cookie...")
        
        if not os.path.exists(filename):
            print(f"  ❌ 文件不存在: {filename}")
            print("  💡 请先运行人工验证获取cookie")
            return None
        
        try:
            with open(filename, 'r') as f:
                cookies_list = json.load(f)
            
            # 转换为字典格式
            cookies_dict = {}
            for cookie in cookies_list:
                cookies_dict[cookie['name']] = cookie['value']
            
            print(f"  ✅ 加载了 {len(cookies_dict)} 个cookie")
            
            # 检查是否有cf_clearance
            if 'cf_clearance' in cookies_dict:
                print(f"  ✅ 找到cf_clearance cookie")
                return cookies_dict
            else:
                print("  ⚠️ 未找到cf_clearance cookie")
                return cookies_dict
                
        except Exception as e:
            print(f"  ❌ 加载cookie失败: {e}")
            return None
    
    def test_with_cookie(self, cookies):
        """使用cookie测试访问"""
        print("\n🍪 使用cookie测试访问...")
        
        if not cookies:
            print("  ❌ 无可用cookie")
            return False
        
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                cookies=cookies,
                proxies=self.proxies,
                timeout=10
            )
            
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("  ✅ 成功绕过验证!")
                
                # 检查页面内容
                content_length = len(response.text)
                print(f"  页面大小: {content_length} 字符")
                
                # 保存成功响应的示例
                sample_file = "cf_success_sample.html"
                with open(sample_file, 'w', encoding='utf-8') as f:
                    f.write(response.text[:2000])  # 保存前2000字符
                print(f"  示例已保存到: {sample_file}")
                
                return True
            else:
                print(f"  ❌ 访问失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
            return False
    
    def show_manual_instructions(self):
        """显示人工验证说明"""
        print("\n" + "="*60)
        print("📋 人工验证获取cookie步骤:")
        print("="*60)
        print("1. 使用Chrome/Firefox浏览器访问:")
        print(f"   {self.url}")
        print("\n2. 完成人机验证（点击、滑动等）")
        print("\n3. 验证成功后，获取cookie:")
        print("   - Chrome: F12 → Application → Cookies")
        print("   - 查找 cf_clearance 和 __cf_bm 等cookie")
        print("\n4. 将cookie保存为JSON格式:")
        print("""
   [
     {
       "name": "cf_clearance",
       "value": "your_cf_clearance_value_here"
     },
     {
       "name": "__cf_bm",
       "value": "your_cf_bm_value_here"
     }
   ]
        """)
        print("\n5. 保存为 cf_cookies.json 文件")
        print("="*60)
    
    def create_cookie_template(self):
        """创建cookie模板文件"""
        template = [
            {
                "name": "cf_clearance",
                "value": "YOUR_CF_CLEARANCE_COOKIE_VALUE_HERE",
                "domain": ".2hg.com",
                "path": "/"
            },
            {
                "name": "__cf_bm",
                "value": "YOUR_CF_BM_COOKIE_VALUE_HERE",
                "domain": ".2hg.com",
                "path": "/"
            }
        ]
        
        with open("cf_cookies_template.json", "w") as f:
            json.dump(template, f, indent=2)
        
        print("\n📝 已创建cookie模板: cf_cookies_template.json")
        print("   请将人工验证后获得的真实cookie值填入")
    
    def run_demo(self):
        """运行演示"""
        print("🚀 CF人机验证实用演示")
        print(f"目标网址: {self.url}")
        print("-" * 60)
        
        # 步骤1: 测试无cookie访问
        print("\n步骤1: 测试无cookie访问")
        self.test_without_cookie()
        
        # 步骤2: 尝试加载已有cookie
        print("\n步骤2: 尝试使用已有cookie")
        cookies = self.load_cookies_from_file()
        
        if cookies:
            success = self.test_with_cookie(cookies)
            if success:
                print("\n🎉 演示完成: 成功使用cookie绕过验证!")
                return
        
        # 步骤3: 显示人工验证说明
        print("\n步骤3: 需要人工验证")
        self.show_manual_instructions()
        
        # 步骤4: 创建模板文件
        self.create_cookie_template()
        
        print("\n💡 提示:")
        print("1. 人工验证一次后，cookie通常有效2-24小时")
        print("2. 可以定期更新cookie文件")
        print("3. 对于生产环境，建议使用验证码服务")

if __name__ == "__main__":
    demo = CFVerificationDemo()
    demo.run_demo()