#!/usr/bin/env python3
"""
尝试使用Chromium浏览器访问目标网站
"""

import subprocess
import time
import os

def start_chromium_with_url(url):
    """启动Chromium浏览器访问指定URL"""
    print(f"启动Chromium浏览器访问: {url}")
    
    # 创建临时用户数据目录
    temp_dir = "/tmp/chromium_temp_" + str(int(time.time()))
    os.makedirs(temp_dir, exist_ok=True)
    
    # Chromium启动命令
    cmd = [
        "chromium-browser",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        f"--user-data-dir={temp_dir}",
        "--window-size=1920,1080",
        url
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 启动浏览器（非阻塞）
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Chromium已启动，PID: {process.pid}")
        print("请手动完成人机验证...")
        
        # 等待一段时间
        time.sleep(30)
        
        # 尝试获取cookies
        cookies_file = os.path.join(temp_dir, "Default", "Cookies")
        if os.path.exists(cookies_file):
            print(f"Cookies文件存在: {cookies_file}")
            # 这里可以添加读取cookies的逻辑
        else:
            print("未找到Cookies文件")
            
        # 让用户手动操作
        print("\n=== 操作说明 ===")
        print("1. 在打开的Chromium浏览器中完成人机验证")
        print("2. 验证通过后，浏览器会显示目标页面")
        print("3. 按Ctrl+C停止脚本")
        print("4. 脚本会尝试获取验证后的cookies")
        
        # 等待用户操作
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"启动浏览器时出错: {e}")
    finally:
        # 清理
        if 'process' in locals():
            process.terminate()
            print("已终止浏览器进程")

if __name__ == "__main__":
    url = "https://cf.2hg.com/?action=mc"
    start_chromium_with_url(url)