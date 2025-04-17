#!/bin/bash

# 刮刀机器人管理脚本
# 用于在Linux系统下管理刮刀机器人的后台运行

# 配置项
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOT_DIR="${SCRIPT_DIR}"
PYTHON_PATH="${BOT_DIR}/.venv/bin/python"
MAIN_SCRIPT="${BOT_DIR}/main.py"
LOG_FILE="${BOT_DIR}/scraper-bot.log"
PID_FILE="${BOT_DIR}/.scraper-bot.pid"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # 无颜色

# 检查虚拟环境是否存在
check_venv() {
    if [ ! -f "${PYTHON_PATH}" ]; then
        echo -e "${RED}错误: 找不到Python虚拟环境，请先按照README中的说明创建虚拟环境${NC}"
        echo "预期路径: ${PYTHON_PATH}"
        exit 1
    fi
}

# 检查程序是否已在运行
is_running() {
    if [ -f "${PID_FILE}" ]; then
        pid=$(cat "${PID_FILE}")
        if ps -p "${pid}" > /dev/null; then
            return 0 # 正在运行
        fi
    fi
    return 1 # 未运行
}

# 启动机器人
start() {
    check_venv
    
    if is_running; then
        echo -e "${YELLOW}警告: 刮刀机器人已经在运行 (PID: $(cat ${PID_FILE}))${NC}"
        return
    fi
    
    echo -e "${GREEN}正在启动刮刀机器人...${NC}"
    cd "${BOT_DIR}"
    
    # 使用nohup在后台运行，将标准输出和错误输出都重定向到nohup.out
    nohup "${PYTHON_PATH}" "${MAIN_SCRIPT}" > nohup.out 2>&1 &
    
    # 保存PID到文件
    echo $! > "${PID_FILE}"
    echo -e "${GREEN}刮刀机器人已启动 (PID: $(cat ${PID_FILE}))${NC}"
}

# 停止机器人
stop() {
    if ! is_running; then
        echo -e "${YELLOW}警告: 刮刀机器人没有运行${NC}"
        return
    fi
    
    pid=$(cat "${PID_FILE}")
    echo -e "${GREEN}正在停止刮刀机器人 (PID: ${pid})...${NC}"
    
    # 发送终止信号
    kill "${pid}"
    
    # 等待程序终止
    for i in {1..10}; do
        if ! ps -p "${pid}" > /dev/null; then
            break
        fi
        echo "等待程序终止... (${i}/10)"
        sleep 1
    done
    
    # 如果程序仍在运行，强制终止
    if ps -p "${pid}" > /dev/null; then
        echo -e "${YELLOW}程序未响应，正在强制终止...${NC}"
        kill -9 "${pid}"
    fi
    
    rm -f "${PID_FILE}"
    echo -e "${GREEN}刮刀机器人已停止${NC}"
}

# 重启机器人
restart() {
    stop
    sleep 2
    start
}

# 查看状态
status() {
    if is_running; then
        pid=$(cat "${PID_FILE}")
        echo -e "${GREEN}刮刀机器人正在运行 (PID: ${pid})${NC}"
        # 显示运行时间
        if [ -x "$(command -v ps)" ]; then
            runtime=$(ps -p "${pid}" -o etime= 2>/dev/null)
            echo -e "运行时间: ${runtime}"
        fi
    else
        echo -e "${RED}刮刀机器人未运行${NC}"
    fi
}

# 查看日志
logs() {
    if [ ! -f "${LOG_FILE}" ]; then
        echo -e "${RED}错误: 找不到日志文件 (${LOG_FILE})${NC}"
        return
    fi
    
    lines=${1:-50}
    echo -e "${GREEN}显示最后 ${lines} 行日志:${NC}"
    tail -n "${lines}" "${LOG_FILE}"
}

# 查看实时日志
follow_logs() {
    if [ ! -f "${LOG_FILE}" ]; then
        echo -e "${RED}错误: 找不到日志文件 (${LOG_FILE})${NC}"
        return
    fi
    
    echo -e "${GREEN}正在实时查看日志 (按 Ctrl+C 退出):${NC}"
    tail -f "${LOG_FILE}"
}

# 显示帮助信息
usage() {
    echo "刮刀机器人管理脚本"
    echo "用法: $0 {start|stop|restart|status|logs|follow|help}"
    echo ""
    echo "  start      启动刮刀机器人"
    echo "  stop       停止刮刀机器人"
    echo "  restart    重启刮刀机器人"
    echo "  status     查看刮刀机器人运行状态"
    echo "  logs [n]   查看最后n行日志 (默认50行)"
    echo "  follow     实时查看日志"
    echo "  help       显示此帮助信息"
}

# 主逻辑
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs $2
        ;;
    follow)
        follow_logs
        ;;
    help|*)
        usage
        ;;
esac

exit 0 