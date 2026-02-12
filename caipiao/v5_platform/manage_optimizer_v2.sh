#!/bin/bash
# 自优化 V2.1 管理脚本
# =====================

SCRIPT="/home/lang/.openclaw/workspace/caipiao/v5_platform/optimizer_v2.py"
LOG_DIR="/home/lang/.openclaw/workspace/caipiao/v5_platform/optimizer_logs"
PID_FILE="/tmp/optimizer_v2.pid"

mkdir -p "$LOG_DIR"

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

start() {
    if check_running; then
        echo "[ERR] 已在运行 (PID: $PID)"
        return 1
    fi
    
    echo "[START] 启动自优化V2.1守护进程..."
    nohup python3 "$SCRIPT" --start >> "$LOG_DIR/daemon.log" 2>&1 &
    PID=$!
    echo "$PID" > "$PID_FILE"
    echo "[OK] 已启动 (PID: $PID)"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        kill $PID 2>/dev/null
        rm -f "$PID_FILE"
        echo "[OK] 已停止"
    else
        echo "[ERR] 未运行"
    fi
}

status() {
    if check_running; then
        echo "[OK] 运行中 (PID: $PID)"
    else
        echo "[ERR] 未运行"
    fi
    
    echo ""
    python3 "$SCRIPT" --status 2>/dev/null
}

run() {
    echo "="*50
    echo "运行自优化 V2.1"
    echo "="*50
    python3 "$SCRIPT" --run
    
    # 保存最新结果
    python3 "$SCRIPT" --status > "$LOG_DIR/latest_result.txt"
}

approve() {
    if [ -z "$2" ]; then
        echo "用法: $0 approve <功能名>"
        return
    fi
    python3 "$SCRIPT" --approve "$2"
}

rollback() {
    if [ -z "$2" ]; then
        echo "用法: $0 rollback <功能名>"
        return
    fi
    python3 "$SCRIPT" --rollback "$2"
}

case "$1" in
    start) start ;;
    stop) stop ;;
    status) status ;;
    run) run ;;
    approve) approve "$@" ;;
    rollback) rollback "$@" ;;
    restart) stop; sleep 2; start ;;
    *) 
        echo "用法: $0 {start|stop|status|run|approve|rollback|restart}"
        echo ""
        echo "示例:"
        echo "  $0 status           # 查看状态（显示3+/4+/5+命中率）"
        echo "  $0 run              # 运行一次"
        echo "  $0 approve 太极生算法  # 审批发布到预测帮助"
        echo "  $0 rollback 太极生算法 # 回滚"
        ;;
esac
