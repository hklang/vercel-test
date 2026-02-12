#!/usr/bin/env python3
"""飞书推送"""

import requests
import json
from typing import Dict, List, Optional

class FeishuSender:
    """飞书消息发送器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
    
    def get_tenant_access_token(self) -> str:
        """获取访问令牌"""
        if not self.app_id or not self.app_secret:
            print("❌ 未配置app_id和app_secret")
            return None
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            data = response.json()
            
            if data.get("code") == 0:
                self.tenant_access_token = data.get("tenant_access_token")
                return self.tenant_access_token
            else:
                print(f"❌ 获取token失败: {data}")
                return None
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return None
    
    def send_text(self, receive_id: str, text: str) -> bool:
        """发送文本消息"""
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return False
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        params = {"receive_id_type": "open_id"}
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        
        try:
            response = requests.post(url, params=params, headers=headers, json=payload, timeout=10)
            data = response.json()
            
            if data.get("code") == 0:
                print("✅ 消息发送成功")
                return True
            else:
                print(f"❌ 发送失败: {data}")
                return False
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return False
    
    def send_card(self, receive_id: str, title: str, content: str) -> bool:
        """发送卡片消息"""
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return False
        
        # 简化版卡片
        text = f"""
**{title}**

{content}

---
七乐彩预测平台 V5.0
"""
        
        return self.send_text(receive_id, text)
    
    def send_predictions(self, receive_id: str, predictions: List[List[int]], period: str):
        """发送预测结果"""
        content = f"""
**{period}期预测**

共{len(predictions)}组预测

前10组:
"""
        
        for i, pred in enumerate(predictions[:10], 1):
            content += f"{i:3d}: {' '.join(f'{n:02d}' for n in pred)}\n"
        
        content += "\n完整预测请查看附件"
        
        return self.send_card(receive_id, f"七乐彩 {period}期 预测", content)

def main():
    """测试发送"""
    print("=" * 60)
    print("飞书推送测试")
    print("=" * 60)
    
    # 检查配置
    import os
    app_id = os.environ.get('FEISHU_APP_ID')
    app_secret = os.environ.get('FEISHU_APP_SECRET')
    
    if not app_id or not app_secret:
        print("⚠️ 未配置飞书APP凭证，跳过实际发送")
        print("请设置环境变量:")
        print("  export FEISHU_APP_ID='xxx'")
        print("  export FEISHU_APP_SECRET='xxx'")
        return True
    
    sender = FeishuSender(app_id, app_secret)
    return sender.get_tenant_access_token() is not None

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
