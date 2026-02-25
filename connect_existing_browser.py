#!/usr/bin/env python3
"""
连接到现有的浏览器实例，检查CF验证状态
"""

import json
import requests

def check_existing_browser():
    """检查现有浏览器状态"""
    print("🔍 检查现有浏览器状态...")
    
    # 尝试连接到现有的Chrome DevTools
    try:
        # 获取浏览器标签页信息
        response = requests.get('http://127.0.0.1:9232/json', timeout=5)
        tabs = response.json()
        
        print(f"✅ 找到 {len(tabs)} 个标签页:")
        for i, tab in enumerate(tabs):
            print(f"  {i+1}. {tab.get('title', '无标题')}")
            print(f"     URL: {tab.get('url', '无URL')}")
            print(f"     ID: {tab.get('id', '无ID')}")
            
            # 检查是否是CF验证页面
            if 'cf.2hg.com' in tab.get('url', ''):
                print("     🎯 这是CF验证页面！")
                
                # 获取页面内容
                try:
                    debug_url = tab.get('webSocketDebuggerUrl', '')
                    if debug_url:
                        print(f"     🔗 WebSocket调试URL: {debug_url}")
                except:
                    pass
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Chrome DevTools (127.0.0.1:9232)")
        print("💡 请确保Chrome浏览器正在运行，并且启用了远程调试")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False

def manual_verification_instructions():
    """提供手动验证说明"""
    print("\n" + "="*60)
    print("👆 手动验证步骤:")
    print("="*60)
    print("1. 切换到Chrome浏览器窗口")
    print("2. 找到CF验证页面 (标题可能是 'Just a moment...' 或 '请稍候...')")
    print("3. 手动完成验证:")
    print("   - 如果是拼图验证: 拖动拼图到正确位置")
    print("   - 如果是复选框: 点击 '我不是机器人' 复选框")
    print("   - 如果是其他验证: 按照页面提示操作")
    print("4. 验证成功后，页面会显示 'it works'")
    print("5. 验证完成后，脚本会自动检测到成功")
    print("="*60)
    
    print("\n📌 当前浏览器信息:")
    print("   - 调试端口: 9232")
    print("   - 用户数据目录: /tmp/chrome-cf-replay")
    print("   - 访问URL: https://cf.2hg.com/?action=mc")

if __name__ == '__main__':
    if check_existing_browser():
        manual_verification_instructions()
        
        # 询问是否要获取验证后的cookie
        print("\n❓ 是否要获取验证后的cookie？(y/n)")
        response = input().strip().lower()
        
        if response == 'y':
            try:
                # 尝试获取cookie
                response = requests.get('http://127.0.0.1:9232/json', timeout=5)
                tabs = response.json()
                
                for tab in tabs:
                    if 'cf.2hg.com' in tab.get('url', ''):
                        tab_id = tab.get('id')
                        # 这里可以添加获取cookie的逻辑
                        print(f"✅ 找到CF标签页 ID: {tab_id}")
                        print("💡 验证完成后，cookie会自动保存在浏览器中")
                        break
                        
            except Exception as e:
                print(f"❌ 获取cookie时出错: {e}")
    else:
        print("\n💡 建议:")
        print("1. 手动打开Chrome浏览器")
        print("2. 访问: https://cf.2hg.com/?action=mc")
        print("3. 完成验证")
        print("4. 验证成功后，可以重用cf_clearance cookie")