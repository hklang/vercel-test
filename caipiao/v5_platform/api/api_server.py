#!/usr/bin/env python3
"""API服务"""

import json
from typing import Dict, List
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class PredictionAPI:
    """预测API"""
    
    def __init__(self):
        self.engine = None
        self.history = []
    
    def load_history(self, filepath: str = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'):
        """加载数据"""
        try:
            with open(filepath, 'r') as f:
                self.history = json.load(f)
            return True
        except:
            return False
    
    def predict(self, count: int = 100) -> List[List[int]]:
        """生成预测"""
        if not self.history:
            return []
        
        # 简化的预测逻辑
        from collections import Counter
        recent = self.history[-10:]
        
        all_nums = []
        for d in recent:
            all_nums.extend([int(n) for n in d['basic_numbers']])
        
        freq = Counter(all_nums)
        hot = [n for n, _ in freq.most_common(15)]
        
        predictions = []
        used = set()
        
        while len(predictions) < count:
            import random
            selected = sorted(random.sample(hot[:12], 7) if len(hot) >= 12 else list(range(1, 31)))
            if tuple(selected) not in used:
                used.add(tuple(selected))
                predictions.append(selected)
        
        return predictions
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "status": "running",
            "version": "5.0",
            "history_count": len(self.history),
            "latest_period": self.history[-1]['period'] if self.history else None,
        }
    
    def get_analysis(self) -> Dict:
        """获取分析"""
        if not self.history:
            return {}
        
        recent = self.history[-10:]
        
        from collections import Counter
        all_nums = []
        for d in recent:
            all_nums.extend([int(n) for n in d['numbers']])
        
        freq = Counter(all_nums)
        
        return {
            "hot_numbers": freq.most_common(10),
            "analysis_periods": len(recent),
        }

class APIHandler(BaseHTTPRequestHandler):
    """HTTP处理器"""
    
    api = None
    
    def log_message(self, format, *args):
        """日志"""
        print(f"[API] {args[0]}")
    
    def do_GET(self):
        """GET请求"""
        path = urllib.parse.urlparse(self.path).path
        
        if path == '/status':
            self.send_json_response(self.api.get_status())
        elif path == '/analysis':
            self.send_json_response(self.api.get_analysis())
        elif path == '/predict':
            predictions = self.api.predict()
            self.send_json_response({
                "predictions": predictions[:10],
                "total": len(predictions)
            })
        else:
            self.send_json_response({
                "error": "Unknown endpoint",
                "endpoints": ["/status", "/analysis", "/predict"]
            })
    
    def send_json_response(self, data: Dict, status: int = 200):
        """发送JSON响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

def run_server(host: str = '0.0.0.0', port: int = 8080):
    """运行服务器"""
    print("=" * 60)
    print(f"启动API服务器: http://{host}:{port}")
    print("=" * 60)
    
    APIHandler.api = PredictionAPI()
    
    if not APIHandler.api.load_history():
        print("⚠️ 加载历史数据失败")
    
    server = HTTPServer((host, port), APIHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n停止服务器")
        server.shutdown()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port=port)
