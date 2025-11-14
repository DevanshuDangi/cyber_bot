# 1930 Cyber Crime Helpline WhatsApp Chatbot

A comprehensive WhatsApp chatbot system for the 1930 Cyber Crime Helpline, Odisha. This system allows citizens to report cybercrimes, check complaint status, and request account unfreezing through WhatsApp.

## 🎯 Problem Statement

The Cyber Crime Helpline 1930 receives a large number of calls daily, leading to long wait times. This WhatsApp chatbot provides an alternative communication channel that:
- Reduces waiting time for complainants
- Automatically collects complaint information
- Generates reference numbers for tracking
- Provides 24/7 availability

## ✨ Features

### Complete Workflow Implementation
- **A. New Complaint**: File complaints for Financial Fraud or Social Media Fraud
- **B. Status Check**: Check status of existing complaints using reference number or mobile number
- **C. Account Unfreeze**: Request account unfreezing
- **D. Other Queries**: General query handling

### Financial Fraud Types (23 Types)
1. Investment/Trading/IPO Fraud
2. Customer Care Fraud
3. UPI Fraud
4. APK Fraud
5. Fake Franchisee/Dealership Fraud
6. Online Job Fraud
7. Debit Card Fraud
8. Credit Card Fraud
9. E-Commerce Fraud
10. Loan App Fraud
11. Sextortion Fraud
12. OLX Fraud
13. Lottery Fraud
14. Hotel Booking Fraud
15. Gaming App Fraud
16. AEPS Fraud
17. Tower Installation Fraud
18. E-Wallet Fraud
19. Digital Arrest Fraud
20. Fake Website Scam Fraud
21. Ticket Booking Fraud
22. Insurance Maturity Fraud
23. Others

### Social Media Fraud Support
- Facebook, Instagram, X (Twitter), WhatsApp, Telegram, Gmail/YouTube
- Fraud Call/SMS reporting
- Platform-specific guidance and links

### Data Collection
- Personal Information (Name, DOB, Phone, Email, Gender, etc.)
- Address Information (Village, Post Office, Police Station, District, PIN Code)
- Document/Image Upload Support
- Data Validation (Phone, Email, PIN Code, Date formats)

### Admin Consoles
- **React/TypeScript app (`admin-ui/`)** for police/ops teams with live stats, attachment previews, exports
- **Static HTML dashboard (`dashboard/index.html`)** for quick offline inspection

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight database (no external setup required)
- **ReportLab**: PDF generation
- **Uvicorn**: ASGI server

### WhatsApp Integration
- **WhatsApp Business API** (Meta/Facebook)
  - Free tier available for development
  - Easy to get credentials from Meta for Business

### Services Used (All Free)
1. **WhatsApp Business API** (Meta)
   - Free for development/testing
   - Get credentials from: https://developers.facebook.com/
   - Setup guide: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started

2. **ngrok** (for local testing)
   - Free tier available
   - Exposes local server to internet for webhook testing
   - Download: https://ngrok.com/

3. **SQLite Database**
   - Built-in, no setup required
   - File-based database

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm (comes with Node.js)
- ngrok (for webhook testing - optional)
- WhatsApp Business API credentials (from Meta)

## 🚀 Quick Setup (Automated)

### One-Command Setup

For **Linux/macOS**:
```bash
./setup.sh
```

For **Windows**:
```bash
python setup.py
```

This will automatically:
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies
- ✅ Install all frontend dependencies
- ✅ Create .env template file
- ✅ Create necessary directories
- ✅ Optionally start both servers

### Start Servers

After setup, start both backend and frontend:

**Linux/macOS:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

This will start:
- Backend API on http://localhost:8000
- Frontend UI on http://localhost:5173
- API Documentation on http://localhost:8000/docs

## 🛠️ Manual Setup Instructions

If you prefer manual setup:

```bash
# Navigate to project directory
cd whatsapp-1930-chatbot-v2

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
VERIFY_TOKEN=cyberbot123
WHATSAPP_TOKEN=your_whatsapp_token_here
PHONE_NUMBER_ID=your_phone_number_id_here
GRAPH_VERSION=v21.0
DEBUG_PRINT_REPLY=1
```

### 3. Get WhatsApp Business API Credentials (Free)

1. Go to https://developers.facebook.com/
2. Create a Facebook Developer account (free)
3. Create a new app
4. Add "WhatsApp" product to your app
5. Get your:
   - **WhatsApp Token** (temporary token available immediately)
   - **Phone Number ID** (provided when you add a test phone number)
   - **Verify Token** (you can set this to any value, e.g., "cyberbot123")

**Note**: For production, you'll need to go through Meta's verification process, but for development/testing, you can use the free tier.

### 4. Run the Server

```bash
# From project root
uvicorn backend.main:app --reload --port 8000
```

The server will start at `http://localhost:8000`

### 5. Expose Server with ngrok (for Webhook)

In a new terminal:

```bash
# Install ngrok (if not installed)
# macOS: brew install ngrok/ngrok/ngrok
# Or download from https://ngrok.com/

# Start ngrok tunnel
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 6. Configure WhatsApp Webhook

1. Go to your Meta App Dashboard
2. Navigate to WhatsApp > Configuration
3. Set Webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
4. Set Verify Token: `cyberbot123` (or your VERIFY_TOKEN)
5. Subscribe to `messages` events

### 7. Access Admin / Police Dashboards

#### React (TypeScript) Admin Console
```bash
cd admin-ui
npm install
# optional: export VITE_API_BASE="http://localhost:8000"
npm run dev
```
Visit the Vite dev URL (defaults to `http://localhost:5173`) and refresh data. You can change the API base URL from the UI header. This console shows stats, full complaint lists, inline evidence galleries, and PDF links.

#### Static HTML Dashboard
Open `dashboard/index.html` directly, or serve it via:
```bash
python -m http.server 8080
# visit http://localhost:8080/dashboard/index.html
```

## 📱 Usage

### For Users (WhatsApp)

1. Send "start" or "hi" to the WhatsApp number
2. Select an option:
   - **A**: File a new complaint
   - **B**: Check status of existing complaint
   - **C**: Request account unfreeze
   - **D**: Other queries

3. Follow the prompts to provide information
4. Upload documents/images when requested
5. Receive reference number upon submission

### For Admins

1. Open the dashboard
2. View all complaints
3. Click "Details" to see full information
4. Click "PDF" to download complaint report
5. Use "Export CSV" to export data

## 📁 Project Structure

```
whatsapp-1930-chatbot-v2/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── db.py                   # Database configuration
│   ├── config.py               # Configuration management
│   ├── message_router.py       # Message routing logic
│   ├── complaint_flow.py        # New complaint workflow
│   ├── status_flow.py          # Status check workflow
│   ├── account_unfreeze_flow.py # Account unfreeze workflow
│   ├── whatsapp_api.py         # WhatsApp API integration
│   ├── reports.py              # PDF report generation
│   ├── utils.py                # Utility functions
│   └── requirements.txt        # Python dependencies
├── dashboard/
│   └── index.html              # Legacy (static) admin dashboard
├── admin-ui/                   # React/TS admin console (npm run dev/build)
├── reports/                    # Generated PDF reports
├── media/                      # Uploaded documents/images
├── scripts/
│   └── dump_db.py              # Utility to print DB contents
├── chatbot.db                  # SQLite database
├── .env                        # Environment variables (create this)
└── README.md                   # This file
```

## 🔒 Security & Privacy

- All data is stored locally in SQLite database
- WhatsApp messages are processed securely
- Personal information is validated before storage
- PDF reports are generated securely
- No data is shared with third parties

## 🧪 Testing

### Test Webhook Locally

Use the provided `simulate_webhook.py`:

```bash
python simulate_webhook.py
```

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Webhook verification
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.challenge=test123&hub.verify_token=cyberbot123"

# Get complaints list
curl http://localhost:8000/_demo/reports
```

## 📊 Database Schema

### Complaints Table
- Personal Information: name, father_spouse_guardian_name, date_of_birth, phone_number, email_id, gender
- Address: village, post_office, police_station, district, pin_code
- Complaint Details: reference_number, complaint_type, main_category, fraud_type, sub_type, status
- Documents: documents (JSON array)
- Timestamps: created_at, updated_at

## 🧰 Utilities
- `scripts/dump_db.py` – prints every complaint/state/user for quick debugging. Run with:
  ```bash
  PYTHONPATH=. python3 scripts/dump_db.py
  ```

## 🚨 Troubleshooting

### Server won't start
- Check if port 8000 is available
- Verify all dependencies are installed
- Check Python version (3.8+)

### WhatsApp webhook not working
- Verify ngrok is running
- Check webhook URL in Meta dashboard
- Verify VERIFY_TOKEN matches
- Check server logs for errors

### Database errors
- Delete `chatbot.db` to reset database
- Check file permissions
- Verify SQLite is working

## 📝 Notes

- **Dry-run mode**: If `WHATSAPP_TOKEN` is not set, the bot will print messages instead of sending (useful for testing)
- **Reference Numbers**: Generated in format `1930-YYYYMMDD-XXXXX`
- **PDF Reports**: Automatically generated when complaint is submitted
- **Image Uploads**: Supported via WhatsApp media messages

## 🔄 Future Enhancements

- [ ] Multi-language support
- [ ] SMS notifications
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Automated response system
- [ ] Integration with government databases

## 📄 License

This project is developed for the 1930 Cyber Crime Helpline, Odisha.

## 👥 Support

For issues or questions:
- Check the troubleshooting section
- Review Meta's WhatsApp API documentation
- Contact the development team

---

**Developed for**: 1930 Cyber Crime Helpline, Odisha  
**Version**: 2.0  
**Last Updated**: 2024
