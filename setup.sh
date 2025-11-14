#!/bin/bash

# Setup script for 1930 Cyber Crime Helpline WhatsApp Chatbot
# This script sets up the entire project including backend and frontend

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print header
echo ""
echo "=========================================="
echo "  1930 Cyber Crime Helpline Chatbot"
echo "  Automated Setup Script"
echo "=========================================="
echo ""

# Check Python installation
print_info "Checking Python installation..."
if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Python $PYTHON_VERSION found"

# Check Node.js installation
print_info "Checking Node.js installation..."
if ! command_exists node; then
    print_error "Node.js is not installed. Please install Node.js 18 or higher."
    print_info "Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Node.js $NODE_VERSION found"

# Check npm installation
if ! command_exists npm; then
    print_error "npm is not installed. Please install npm."
    exit 1
fi

NPM_VERSION=$(npm --version)
print_success "npm $NPM_VERSION found"

echo ""
print_info "Starting setup process..."
echo ""

# Step 1: Create virtual environment
print_info "Step 1: Setting up Python virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Step 2: Activate virtual environment and install backend dependencies
print_info "Step 2: Installing backend dependencies..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet

# Install backend requirements
print_info "Installing Python packages..."
pip install -r backend/requirements.txt

print_success "Backend dependencies installed"

# Step 3: Install frontend dependencies
print_info "Step 3: Installing frontend dependencies..."
cd admin-ui

if [ ! -f "package.json" ]; then
    print_error "package.json not found in admin-ui directory"
    exit 1
fi

print_info "Running npm install..."
npm install

print_success "Frontend dependencies installed"
cd ..

# Step 4: Create .env file if it doesn't exist
print_info "Step 4: Checking environment configuration..."
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating template..."
    cat > .env << EOF
# WhatsApp Business API Configuration
VERIFY_TOKEN=cyberbot123
WHATSAPP_TOKEN=
PHONE_NUMBER_ID=
GRAPH_VERSION=v21.0
DEBUG_PRINT_REPLY=1

# Google Gemini API Configuration
GEMINI_API_KEY=

# Note: Fill in the above values with your actual API credentials
EOF
    print_success ".env template created"
    print_warning "Please update .env file with your API credentials"
else
    print_success ".env file exists"
fi

# Step 5: Create necessary directories
print_info "Step 5: Creating necessary directories..."
mkdir -p media reports
print_success "Directories created"

# Step 6: Database will be auto-created on first run
print_info "Step 6: Database will be auto-created on first run"

echo ""
print_success "Setup completed successfully!"
echo ""

# Step 7: Ask if user wants to start servers
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update .env file with your API credentials"
echo "2. Run './start.sh' to start both backend and frontend servers"
echo ""
read -p "Do you want to start the servers now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    print_info "Starting servers..."
    echo ""
    
    # Deactivate venv for now (will be activated in start script)
    deactivate
    
    # Check if start.sh exists, if not create it
    if [ ! -f "start.sh" ]; then
        print_info "Creating start.sh script..."
        # We'll create this in the next step
    fi
    
    # Start servers
    ./start.sh
else
    echo ""
    print_info "To start servers later, run: ./start.sh"
    echo ""
fi

