#!/bin/bash

# Start script for 1930 Cyber Crime Helpline WhatsApp Chatbot
# Starts both backend and frontend servers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run './setup.sh' first."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    print_error ".env file not found. Please run './setup.sh' first."
    exit 1
fi

echo ""
echo "=========================================="
echo "  Starting 1930 Cyber Crime Helpline"
echo "  WhatsApp Chatbot Servers"
echo "=========================================="
echo ""

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Function to cleanup on exit
cleanup() {
    print_info "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup SIGINT SIGTERM

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Start backend server
print_info "Starting backend server (FastAPI) on http://localhost:8000..."
source venv/bin/activate
uvicorn backend.main:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Check if backend started successfully
if ps -p $BACKEND_PID > /dev/null 2>&1; then
    print_success "Backend server started (PID: $BACKEND_PID)"
else
    print_error "Backend server failed to start. Check backend.log for details."
    cat backend.log
    exit 1
fi

# Start frontend server
print_info "Starting frontend server (React) on http://localhost:5173..."
cd admin-ui
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 5

# Check if frontend started successfully
if ps -p $FRONTEND_PID > /dev/null 2>&1; then
    print_success "Frontend server started (PID: $FRONTEND_PID)"
else
    print_error "Frontend server failed to start. Check frontend.log for details."
    cat ../frontend.log
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

cd "$SCRIPT_DIR"

echo ""
echo "=========================================="
echo "  Servers Running Successfully!"
echo "=========================================="
echo ""
print_success "Backend API: http://localhost:8000"
print_success "Frontend UI: http://localhost:5173"
print_success "API Docs: http://localhost:8000/docs"
echo ""
print_info "Logs:"
echo "  - Backend: tail -f backend.log"
echo "  - Frontend: tail -f frontend.log"
echo ""
print_info "Press Ctrl+C to stop all servers"
echo ""

# Store PIDs in file for cleanup
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID

