# Quick Start Guide

## 🚀 One-Command Setup & Run

### For Linux/macOS Users

```bash
# Clone the repository
git clone <repository-url>
cd whatsapp-1930-chatbot-v2

# Run automated setup
./setup.sh

# Start servers
./start.sh
```

### For Windows Users

```cmd
REM Clone the repository
git clone <repository-url>
cd whatsapp-1930-chatbot-v2

REM Run automated setup
python setup.py

REM Start servers
start.bat
```

### Using Make (Linux/macOS)

```bash
# Setup everything
make setup

# Start servers
make start

# Stop servers
make stop

# Clean everything
make clean
```

## 📝 What the Setup Script Does

1. ✅ Checks for Python 3.8+, Node.js 18+, and npm
2. ✅ Creates Python virtual environment (`venv/`)
3. ✅ Installs all backend Python packages
4. ✅ Installs all frontend Node.js packages
5. ✅ Creates `.env` template file
6. ✅ Creates necessary directories (`media/`, `reports/`)
7. ✅ Optionally starts both servers

## 🔧 Configuration

After setup, edit `.env` file with your credentials:

```env
VERIFY_TOKEN=cyberbot123
WHATSAPP_TOKEN=your_whatsapp_token_here
PHONE_NUMBER_ID=your_phone_number_id_here
GRAPH_VERSION=v21.0
DEBUG_PRINT_REPLY=1
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🌐 Access Points

Once servers are running:

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend Admin UI**: http://localhost:5173
- **Health Check**: http://localhost:8000/health

## 🛑 Stopping Servers

### Linux/macOS
Press `Ctrl+C` in the terminal where `start.sh` is running, or:
```bash
make stop
```

### Windows
Close the command prompt windows, or:
```cmd
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

## 🐛 Troubleshooting

### Virtual environment not found
```bash
# Re-run setup
./setup.sh
# or
python setup.py
```

### Port already in use
```bash
# Kill processes on ports 8000 and 5173
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Permission denied (Linux/macOS)
```bash
chmod +x setup.sh start.sh
```

### npm install fails
```bash
# Clear npm cache
npm cache clean --force
cd admin-ui
rm -rf node_modules package-lock.json
npm install
```

## 📚 Next Steps

1. Configure `.env` with your API credentials
2. Set up WhatsApp Business API webhook
3. Test the chatbot by sending messages
4. Access admin dashboard to view complaints

For detailed documentation, see `README.md` and `TECHNICAL_DOCUMENTATION.md`.

