#!/bin/bash
# v2rayA 健康检查与自动修复脚本

LOG_FILE="/home/lang/.openclaw/workspace/logs/v2ray_check.log"
TELEGRAM_TOKEN=""
TELEGRAM_CHAT_ID=""

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

send_telegram() {
    if [ -n "$TELEGRAM_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="$1" >/dev/null
    fi
}

check_internet() {
    # 测试外网连接（不使用代理）
    if curl -s --connect-timeout 5 --proxy-direct https://www.google.com >/dev/null 2>&1; then
        return 0
    fi
    # 备用测试
    if ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

check_v2raya_proxy() {
    # 测试v2rayA代理是否可用
    if curl -s --proxy http://127.0.0.1:20171 --connect-timeout 5 https://www.google.com >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

fix_v2raya() {
    log "检测到v2rayA代理异常，开始修复..."

    # 尝试重启v2rayA服务
    systemctl restart snap.v2raya.v2raya.service
    sleep 5

    # 检查是否重启成功
    if systemctl is-active --quiet snap.v2raya.v2raya.service; then
        log "v2rayA服务已重启"
        send_telegram "🔧 v2rayA代理异常，已自动修复重启"
        return 0
    fi

    log "v2rayA服务重启失败，尝试Docker容器方式..."
    # 如果是Docker部署，尝试重启容器
    if docker ps | grep -q v2raya; then
        docker restart v2raya 2>/dev/null
        sleep 5
        log "Docker容器已重启"
        send_telegram "🔧 v2rayA Docker容器已重启"
        return 0
    fi

    log "修复失败！需要人工干预"
    send_telegram "🚨 v2rayA修复失败，请人工检查！"
    return 1
}

# 主逻辑
log "========== 开始检查 =========="

# 1. 检查普通外网连接
if ! check_internet; then
    log "❌ 无法连接外网（直连）"
    exit 1
fi
log "✅ 外网连接正常"

# 2. 检查v2rayA代理
if check_v2raya_proxy; then
    log "✅ v2rayA代理正常"
    exit 0
else
    log "⚠️ v2rayA代理异常，尝试修复..."
    fix_v2raya
fi

log "========== 检查完成 =========="
