#!/usr/bin/env python3
"""
使用昨天成功的方法进行CF验证
1. 打开可见的浏览器窗口
2. 访问CF验证页面
3. 等待人工交互完成验证
"""

import time
import subprocess
import os

def open_browser_with_yesterday_method():
    """使用昨天成功的方法打开浏览器"""
    print("🚀 使用昨天成功的方法打开浏览器...")
    
    # 昨天成功的方法：使用Chrome浏览器，非无头模式
    # 使用与昨天相同的参数
    chrome_cmd = [
        "chromium-browser",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1280,800",
        "--disable-blink-features=AutomationControlled",
        "--remote-debugging-port=9232",
        "--user-data-dir=/tmp/chrome-cf-yesterday",
        "https://cf.2hg.com/?action=mc"
    ]
    
    print(f"📝 启动命令: {' '.join(chrome_cmd[:5])}...")
    
    try:
        # 启动浏览器进程
        process = subprocess.Popen(
            chrome_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ 浏览器已启动")
        print("💡 请切换到浏览器窗口完成验证")
        print("⏳ 等待30秒让浏览器加载...")
        time.sleep(30)
        
        return process
        
    except Exception as e:
        print(f"❌ 启动浏览器失败: {e}")
        return None

def check_verification_status():
    """检查验证状态"""
    print("\n🔍 检查验证状态...")
    
    try:
        # 检查是否有cf_clearance cookie
        cookie_check = subprocess.run(
            ["curl", "-s", "http://127.0.0.1:9232/json"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if cookie_check.returncode == 0:
            print("✅ 可以连接到浏览器调试端口")
            
            # 检查页面标题
            title_check = subprocess.run(
                ["curl", "-s", "http://127.0.0.1:9232/json/version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if title_check.returncode == 0:
                print("✅ 浏览器调试接口正常")
                
        # 检查进程是否还在运行
        ps_check = subprocess.run(
            ["ps", "aux", "|", "grep", "-i", "chrome", "|", "grep", "-v", "grep", "|", "wc", "-l"],
            shell=True,
            capture_output=True,
            text=True
        )
        
        chrome_count = int(ps_check.stdout.strip())
        print(f"📊 当前Chrome进程数: {chrome_count}")
        
    except Exception as e:
        print(f"⚠️ 检查状态时出错: {e}")

def provide_manual_instructions():
    """提供手动验证说明"""
    print("\n" + "="*60)
    print("👆 手动验证步骤 (昨天成功的方法):")
    print("="*60)
    print("1. 找到新打开的Chrome浏览器窗口")
    print("2. 页面应该显示CF验证 (可能是拼图或复选框)")
    print("3. 手动完成验证:")
    print("   - 拼图验证: 拖动拼图块到正确位置")
    print("   - 复选框: 点击 '我不是机器人'")
    print("   - 其他: 按照页面提示操作")
    print("4. 验证成功后，页面会显示 'it works'")
    print("5. 完成后告诉我，我会检查验证状态")
    print("="*60)
    
    print("\n📌 重要提示:")
    print("   - 使用与昨天相同的浏览器配置")
    print("   - 非无头模式 (可以看到浏览器窗口)")
    print("   - 用户数据目录: /tmp/chrome-cf-yesterday")
    print("   - 调试端口: 9232")

def main():
    """主函数"""
    print("🎯 开始使用昨天成功的方法进行CF验证")
    
    # 1. 打开浏览器
    browser_process = open_browser_with_yesterday_method()
    
    if not browser_process:
        print("❌ 无法启动浏览器，尝试备用方法...")
        print("💡 请手动打开Chrome浏览器访问: https://cf.2hg.com/?action=mc")
        provide_manual_instructions()
        return
    
    # 2. 提供手动验证说明
    provide_manual_instructions()
    
    # 3. 等待用户完成验证
    print("\n⏳ 等待人工验证完成...")
    print("✅ 完成后请输入 'done' 或告诉我验证状态")
    
    # 4. 检查验证状态
    time.sleep(10)  # 给用户一些时间
    check_verification_status()
    
    # 5. 保持进程运行
    try:
        print("\n📝 浏览器进程ID:", browser_process.pid)
        print("💡 按 Ctrl+C 可以停止脚本，但浏览器会继续运行")
        
        # 等待用户输入
        while True:
            user_input = input("\n输入 'status' 检查状态，'quit' 退出: ").strip().lower()
            
            if user_input == 'status':
                check_verification_status()
            elif user_input == 'quit':
                print("👋 退出脚本，浏览器继续运行")
                break
            elif user_input == 'done':
                print("🎉 验证完成！检查状态...")
                check_verification_status()
                break
                
    except KeyboardInterrupt:
        print("\n👋 脚本被中断，浏览器继续运行")
    finally:
        # 不终止浏览器进程，让用户继续使用
        print("💻 浏览器窗口保持打开状态")

if __name__ == '__main__':
    main()