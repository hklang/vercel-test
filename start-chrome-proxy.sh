#!/bin/bash
# 启动Chrome浏览器，使用v2rayA代理

# v2rayA代理配置
SOCKS5_PROXY="127.0.0.1:20170"
HTTP_PROXY="127.0.0.1:20171"

echo "🚀 启动Chrome浏览器（使用v2rayA代理）..."
echo "📡 SOCKS5代理: $SOCKS5_PROXY"
echo "🌐 HTTP代理: $HTTP_PROXY"
echo ""

# 使用代理参数启动浏览器
/usr/bin/chromium-browser \
  --proxy-server="socks5://$SOCKS5_PROXY;http://$HTTP_PROXY" \
  --no-sandbox \
  --disable-setuid-sandbox \
  --disable-dev-shm-usage \
  --ignore-certificate-errors \
  --test-type \
  --disable-gpu \
  "$@" &

echo "✅ 浏览器已启动！"
echo ""
echo "💡 测试访问："
echo "   - Google: https://www.google.com"
echo "   - YouTube: https://www.youtube.com"
echo ""
echo "按 Ctrl+C 关闭"
