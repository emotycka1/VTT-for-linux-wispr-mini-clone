#!/bin/bash
# Manage Wispr-Flow Clone - Check status, start, stop, restart

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running
check_status() {
    if pgrep -f "python -m src.main" > /dev/null; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Show status
status() {
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║      Wispr-Flow Status Check              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
    echo ""
    
    if check_status; then
        PID=$(pgrep -f "python -m src.main")
        echo -e "${GREEN}✅ Status: RUNNING${NC}"
        echo -e "   PID: ${PID}"
        
        # Get process details
        PS_INFO=$(ps -p ${PID} -o %cpu,%mem,etime --no-headers)
        echo -e "   CPU: $(echo ${PS_INFO} | awk '{print $1}')%"
        echo -e "   RAM: $(echo ${PS_INFO} | awk '{print $2}')%"
        echo -e "   Uptime: $(echo ${PS_INFO} | awk '{print $3}')"
        echo ""
        
        # Check GPU usage
        if nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | grep -q ${PID}; then
            GPU_MEM=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | grep ${PID} | awk -F', ' '{print $2}')
            echo -e "${GREEN}🎮 GPU: Active (${GPU_MEM})${NC}"
        else
            echo -e "${YELLOW}🎮 GPU: Idle (will activate during transcription)${NC}"
        fi
        echo ""
        
        echo -e "${BLUE}📝 Ready to use!${NC}"
        echo -e "   Press ${GREEN}Ctrl+Alt${NC} and speak"
    else
        echo -e "${RED}❌ Status: NOT RUNNING${NC}"
        echo ""
        echo -e "${YELLOW}💡 To start:${NC}"
        echo -e "   ./start-wispr.sh"
        echo -e "   or"
        echo -e "   ./run.sh"
    fi
}

# Start
start() {
    if check_status; then
        echo -e "${YELLOW}⚠️  Already running!${NC}"
        echo -e "   Use './manage-wispr.sh stop' to stop it first"
        return 1
    fi
    
    echo -e "${GREEN}🚀 Starting Wispr-Flow...${NC}"
    cd "${SCRIPT_DIR}"
    nohup ./run.sh > /tmp/wispr-flow.log 2>&1 &
    sleep 2
    
    if check_status; then
        echo -e "${GREEN}✅ Started successfully!${NC}"
        status
    else
        echo -e "${RED}❌ Failed to start. Check /tmp/wispr-flow.log${NC}"
    fi
}

# Stop
stop() {
    if ! check_status; then
        echo -e "${YELLOW}⚠️  Not running${NC}"
        return 1
    fi
    
    PID=$(pgrep -f "python -m src.main")
    echo -e "${YELLOW}🛑 Stopping Wispr-Flow (PID: ${PID})...${NC}"
    pkill -f "python -m src.main"
    sleep 2
    
    if ! check_status; then
        echo -e "${GREEN}✅ Stopped successfully${NC}"
    else
        echo -e "${RED}❌ Failed to stop. Trying force kill...${NC}"
        pkill -9 -f "python -m src.main"
        sleep 1
        if ! check_status; then
            echo -e "${GREEN}✅ Force stopped${NC}"
        else
            echo -e "${RED}❌ Could not stop. Manual intervention needed.${NC}"
        fi
    fi
}

# Restart
restart() {
    echo -e "${BLUE}🔄 Restarting Wispr-Flow...${NC}"
    stop
    sleep 2
    start
}

# Logs
logs() {
    if [ -f /tmp/wispr-flow.log ]; then
        echo -e "${BLUE}📋 Recent logs:${NC}"
        echo "────────────────────────────────────────────"
        tail -n 20 /tmp/wispr-flow.log
        echo "────────────────────────────────────────────"
        echo ""
        echo "Full log: /tmp/wispr-flow.log"
    else
        echo -e "${YELLOW}⚠️  No log file found${NC}"
    fi
}

# GPU info
gpu() {
    echo -e "${BLUE}🎮 GPU Information:${NC}"
    echo "────────────────────────────────────────────"
    nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv,noheader | \
    while IFS=', ' read -r name temp gpu_util mem_util mem_used mem_total; do
        echo "  GPU: ${name}"
        echo "  Temperature: ${temp}"
        echo "  GPU Utilization: ${gpu_util}"
        echo "  Memory Utilization: ${mem_util}"
        echo "  Memory Used: ${mem_used} / ${mem_total}"
    done
    echo "────────────────────────────────────────────"
}

# Help
usage() {
    echo -e "${BLUE}Wispr-Flow Management Script${NC}"
    echo ""
    echo "Usage: $0 {status|start|stop|restart|logs|gpu|help}"
    echo ""
    echo "Commands:"
    echo "  status   - Check if running and show details"
    echo "  start    - Start in background"
    echo "  stop     - Stop the service"
    echo "  restart  - Restart the service"
    echo "  logs     - Show recent logs"
    echo "  gpu      - Show GPU information"
    echo "  help     - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 status        # Check current status"
    echo "  $0 start         # Start in background"
    echo "  $0 stop          # Stop the service"
    echo "  $0 restart       # Restart the service"
}

# Main
case "$1" in
    status)
        status
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    gpu)
        gpu
        ;;
    help|--help|-h|"")
        usage
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        usage
        exit 1
        ;;
esac
