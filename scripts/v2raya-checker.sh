#!/bin/bash
# V2RayA 自动健康检查脚本 - 增强版
# 每20分钟执行一次

# 配置
V2RAYA_API="http://127.0.0.1:20170"
LOG_FILE="/home/lang/.openclaw/workspace/logs/v2raya-checker.log"
TEST_URL="https://www.google.com"
PROXY_PORT="20170"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查代理进程
check_process() {
    pgrep -f "v2raya" > /dev/null 2>&1
}

# 检查代理端口
check_port() {
    ss -tlnp 2>/dev/null | grep -q ":${PROXY_PORT} "
}

# 检查代理连接（关键指标）
check_proxy_connection() {
    curl -s --proxy "socks5://127.0.0.1:${PROXY_PORT}" --connect-timeout 10 -o /dev/null -w "%{http_code}" "$TEST_URL" 2>/dev/null | grep -qE "200|302"
}

# 检查直连网络
check_direct_connection() {
    curl -s --connect-timeout 5 -o /dev/null -w "%{http_code}" "https://www.baidu.com" | grep -qE "200|302"
}

# 保存状态
save_status() {
    local status="$1"
    local issues="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "{\"status\":\"$status\",\"issues\":\"$issues\",\"timestamp\":\"$timestamp\"}" > /home/lang/.openclaw/workspace/logs/v2raya-status.json
}

# 主逻辑
main() {
    log "========== V2RayA健康检查 =========="
    
    # 1. 检查进程
    if ! check_process; then
        log "⚠️ V2RayA进程未运行"
        save_status "异常" "进程未运行"
        echo "❌ V2RayA进程未运行"
        exit 1
    fi
    
    log "✅ 进程运行正常"
    
    # 2. 检查端口
    if ! check_port; then
        log "⚠️ 代理端口未监听"
        save_status "异常" "端口未监听"
        echo "⚠️ 代理端口未监听"
    else
        log "✅ 代理端口正常"
    fi
    
    # 3. 检查直连网络
    if ! check_direct_connection; then
        log "⚠️ 直连网络异常"
        save_status "异常" "直连网络异常"
        echo "⚠️ 直连网络异常"
    else
        log "✅ 直连网络正常"
    fi
    
    # 4. 检查代理连接（最重要）
    if check_proxy_connection; then
        log "✅ V2RayA代理运行正常 - 可以访问外网"
        save_status "正常" ""
        echo "✅ V2RayA代理正常 (socks5://127.0.0.1:${PROXY_PORT})"
    else
        log "❌ 代理无法连接外网"
        save_status "异常" "代理无连接"
        echo "❌ 代理无法连接外网"
    fi
    
    log "========== 检查完成 =========="
}

main "$@"
