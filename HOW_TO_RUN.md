# How to Run the Project

## 🚀 Quick Start (Recommended)

### Step 1: Run Setup (One Time)

**For Linux/macOS:**
```bash
./setup.sh
```

**For Windows:**
```bash
python setup.py
```

This will:
- ✅ Check all prerequisites
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies
- ✅ Install all frontend dependencies
- ✅ Create `.env` file template
- ✅ Create necessary directories

### Step 2: Configure Environment

Edit the `.env` file with your API credentials:

```env
VERIFY_TOKEN=cyberbot123
WHATSAPP_TOKEN=your_whatsapp_token_here
PHONE_NUMBER_ID=your_phone_number_id_here
GRAPH_VERSION=v21.0
DEBUG_PRINT_REPLY=1
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note:** For testing without WhatsApp credentials, you can leave `WHATSAPP_TOKEN` empty. The system will run in dry-run mode (prints messages to console).

### Step 3: Start Servers

**For Linux/macOS:**
```bash
./start.sh
```

**For Windows:**
```batch
start.bat
```

**Using Make (Linux/macOS):**
```bash
make start
```

This will start:
- 🟢 **Backend API** on http://localhost:8000
- 🟢 **Frontend Admin UI** on http://localhost:5173
- 🟢 **API Documentation** on http://localhost:8000/docs

### Step 4: Access the Application

Once servers are running, open your browser:

- **Admin Dashboard**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📋 Detailed Instructions

### Prerequisites Check

Before running, ensure you have:

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **Node.js 18+**
   ```bash
   node --version
   ```

3. **npm** (comes with Node.js)
   ```bash
   npm --version
   ```

### Manual Setup (Alternative)

If you prefer manual setup:

#### 1. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

#### 2. Frontend Setup

```bash
# Navigate to admin-ui directory
cd admin-ui

# Install dependencies
npm install

# Go back to root
cd ..
```

#### 3. Start Backend

```bash
# Make sure venv is activated
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Start server
uvicorn backend.main:app --reload --port 8000
```

#### 4. Start Frontend (in a new terminal)

```bash
cd admin-ui
npm run dev
```

---

## 🛑 Stopping the Servers

### If using start.sh (Linux/macOS)
Press `Ctrl+C` in the terminal

### If using start.bat (Windows)
Close the command prompt windows

### Manual Stop
```bash
# Stop backend
pkill -f "uvicorn backend.main:app"

# Stop frontend
pkill -f "vite"
```

Or using Make:
```bash
make stop
```

---

## 🧪 Testing Without WhatsApp API

The system works in **dry-run mode** if you don't have WhatsApp credentials:

1. Leave `WHATSAPP_TOKEN` empty in `.env`
2. Run the servers
3. Messages will be printed to console instead of sent to WhatsApp
4. You can test the complete flow locally

---

## 📱 Setting Up WhatsApp Webhook (Optional)

If you have WhatsApp Business API credentials:

1. **Start ngrok** (in a new terminal):
   ```bash
   ngrok http 8000
   ```

2. **Copy the ngrok URL** (e.g., `https://abc123.ngrok.io`)

3. **Configure webhook in Meta Developer Console**:
   - Go to https://developers.facebook.com/
   - Navigate to your WhatsApp app
   - Go to Configuration → Webhook
   - Set Callback URL: `https://abc123.ngrok.io/webhook`
   - Set Verify Token: `cyberbot123` (or your VERIFY_TOKEN)
   - Subscribe to `messages` event

4. **Test by sending a message** to your WhatsApp Business number

---

## 🐛 Troubleshooting

### Port Already in Use

**Linux/macOS:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Virtual Environment Issues

```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### Frontend Dependencies Issues

```bash
cd admin-ui
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Permission Denied (Linux/macOS)

```bash
chmod +x setup.sh start.sh
```

---

## ✅ Verification

After starting, verify everything is working:

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"ok":true}`

2. **Frontend:**
   - Open http://localhost:5173 in browser
   - Should see the admin dashboard

3. **API Docs:**
   - Open http://localhost:8000/docs
   - Should see Swagger UI

---

## 📚 Next Steps

1. ✅ Servers are running
2. ✅ Configure `.env` with API credentials
3. ✅ Set up WhatsApp webhook (if needed)
4. ✅ Test the chatbot
5. ✅ View complaints in admin dashboard

For more details, see:
- `README.md` - Full documentation
- `TECHNICAL_DOCUMENTATION.md` - Technical details
- `QUICK_START.md` - Quick reference

