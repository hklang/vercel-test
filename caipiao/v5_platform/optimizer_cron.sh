#!/bin/bash
# 七乐彩自动优化任务 - Cron版
# ==============================

# 配置
SCRIPT="/home/lang/.openclaw/workspace/caipiao/v5_platform/optimizer_auto.py"
LOG_DIR="/home/lang/.openclaw/workspace/caipiao/v5_platform/logs"
LOG_FILE="$LOG_DIR/optimizer_cron.log"
NOTIFY_SCRIPT="/home/lang/.openclaw/workspace/caipiao/v5_platform/notify_optimizer.py"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 运行优化任务
run_optimizer() {
    log "开始优化任务"
    python3 "$SCRIPT" --once 2>&1 | tee -a "$LOG_FILE"
}

# 生成Cron配置
cron_config() {
    echo "# 七乐彩自动优化 - Cron配置"
    echo "# 每小时运行一次"
    echo "5 * * * * /usr/bin/python3 $SCRIPT --once >> $LOG_FILE 2>&1"
    echo ""
    echo "添加到crontab:"
    echo "  (echo \"5 * * * * /usr/bin/python3 $SCRIPT --once >> $LOG_FILE 2>&1\") | crontab -"
}

# 主逻辑
case "$1" in
    run)
        run_optimizer
        ;;
    cron)
        cron_config
        ;;
    install)
        echo "安装Cron任务..."
        (echo "5 * * * * /usr/bin/python3 $SCRIPT --once >> $LOG_FILE 2>&1") | crontab -
        echo "✅ 已安装（每天小时5分运行）"
        ;;
    uninstall)
        echo "移除Cron任务..."
        crontab -l | grep -v "$SCRIPT" | crontab -
        echo "✅ 已移除"
        ;;
    status)
        echo "Cron任务:"
        crontab -l | grep "$SCRIPT" || echo "  未安装"
        echo ""
        echo "最近运行:"
        tail -20 "$LOG_FILE"
        ;;
    *)
        echo "用法: $0 {run|cron|install|uninstall|status}"
        echo ""
        echo "示例:"
        echo "  $0 run      # 运行一次"
        echo "  $0 cron     # 生成Cron配置"
        echo "  $0 install  # 安装Cron任务"
        echo "  $0 uninstall # 移除Cron任务"
        echo "  $0 status   # 查看状态"
        ;;
esac
