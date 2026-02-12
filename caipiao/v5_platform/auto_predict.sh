#!/bin/bash
# 七乐彩自动预测任务 - V7.1
# ============================

# 配置
SCRIPT="/home/lang/.openclaw/workspace/caipiao/v5_platform/main_v71.py"
LOG_DIR="/home/lang/.openclaw/workspace/caipiao/v5_platform/logs"
LOG_FILE="$LOG_DIR/auto_predict.log"
PID_FILE="/tmp/v71_predictor.pid"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查是否在运行
check_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# 启动守护进程
start() {
    if check_running; then
        echo "❌ 已在运行 (PID: $PID)"
        return 1
    fi
    
    echo "🚀 启动V7.1自动预测任务..."
    log "启动自动预测任务"
    
    # 后台运行
    nohup python3 "$SCRIPT" --auto --interval 3600 >> "$LOG_FILE" 2>&1 &
    PID=$!
    
    echo "$PID" > "$PID_FILE"
    echo "✅ 已启动 (PID: $PID)"
    log "已启动 (PID: $PID)"
}

# 停止
stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        kill $PID 2>/dev/null
        rm -f "$PID_FILE"
        echo "✅ 已停止"
        log "已停止"
    else
        echo "❌ 未运行"
    fi
}

# 状态
status() {
    if check_running; then
        echo "✅ 运行中 (PID: $PID)"
        log "状态检查：运行中"
    else
        echo "❌ 未运行"
        log "状态检查：未运行"
    fi
    
    # 显示最近运行
    if [ -f "$LOG_FILE" ]; then
        echo ""
        echo "最近运行:"
        tail -3 "$LOG_FILE"
    fi
}

# 运行一次
run_once() {
    echo "="*50
    echo "运行预测任务"
    echo "="*50
    log "运行预测任务"
    python3 "$SCRIPT"
}

# 生成Cron配置
cron() {
    echo "# 七乐彩V7.1自动预测 - Cron配置"
    echo "#"
    echo "# 每小时运行一次"
    echo "0 * * * * /usr/bin/python3 $SCRIPT >> $LOG_FILE 2>&1"
    echo ""
    echo "添加到crontab:"
    echo "  (echo \"0 * * * * /usr/bin/python3 $SCRIPT >> $LOG_FILE 2>&1\") | crontab -"
}

# 主逻辑
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    run)
        run_once
        ;;
    cron)
        cron
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    *)
        echo "用法: $0 {start|stop|status|run|cron|restart}"
        echo ""
        echo "示例:"
        echo "  $0 start    # 启动守护进程"
        echo "  $0 stop     # 停止"
        echo "  $0 status   # 查看状态"
        echo "  $0 run      # 运行一次"
        echo "  $0 cron     # 生成Cron配置"
        echo "  $0 restart  # 重启"
        exit 1
        ;;
esac
