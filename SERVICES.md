# Services and Credentials Used

This document lists all the services used in this project and how to obtain free credentials.

## 🆓 Free Services Used

### 1. WhatsApp Business API (Meta/Facebook)
**Status**: ✅ FREE for development/testing

**What it does**: 
- Enables WhatsApp messaging functionality
- Receives and sends messages via webhooks
- Handles media (images, documents)

**How to get credentials**:
1. Go to https://developers.facebook.com/
2. Sign up for a free Facebook Developer account
3. Create a new app
4. Add "WhatsApp" product
5. Get your credentials:
   - **WhatsApp Token**: Available immediately in the API setup
   - **Phone Number ID**: Provided when you add a test phone number
   - **Verify Token**: You can set any value (e.g., "cyberbot123")

**Free Tier Limits**:
- 1,000 conversations/month (free tier)
- Unlimited messages during development
- Test phone numbers available

**Setup Guide**: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started

**Cost**: FREE for development, paid plans available for production

---

### 2. ngrok
**Status**: ✅ FREE tier available

**What it does**:
- Creates secure tunnels to expose local server to internet
- Required for WhatsApp webhook testing
- Provides HTTPS URL for webhook callbacks

**How to get**:
1. Go to https://ngrok.com/
2. Sign up for free account
3. Download ngrok
4. Get your authtoken from dashboard
5. Configure: `ngrok config add-authtoken YOUR_TOKEN`

**Free Tier Limits**:
- 1 tunnel at a time
- Random subdomain (changes on restart)
- Sufficient for development/testing

**Cost**: FREE (paid plans for static domains)

---

### 3. SQLite Database
**Status**: ✅ FREE (Built-in)

**What it does**:
- Stores all complaint data
- No external database server needed
- File-based, easy to backup

**Setup**: No setup required - Python includes SQLite

**Cost**: FREE

---

### 4. Python Libraries (All Free)
**Status**: ✅ All FREE and open-source

**Libraries used**:
- FastAPI: Web framework
- SQLAlchemy: Database ORM
- Uvicorn: ASGI server
- ReportLab: PDF generation
- python-dotenv: Environment variables
- requests: HTTP client

**Cost**: FREE (all open-source)

---

## 📋 Credentials Summary

### Required Credentials (All Free)

1. **WhatsApp Business API** (Meta)
   - WhatsApp Token: Get from Meta Developer Dashboard
   - Phone Number ID: Get from Meta Developer Dashboard
   - Verify Token: Set your own value (e.g., "cyberbot123")

2. **ngrok** (Optional, for local testing)
   - Authtoken: Get from ngrok dashboard
   - Not required if deploying to cloud

### Environment Variables (.env file)

```env
VERIFY_TOKEN=cyberbot123                    # Your chosen verify token
WHATSAPP_TOKEN=your_token_here              # From Meta Dashboard
PHONE_NUMBER_ID=your_phone_id_here          # From Meta Dashboard
GRAPH_VERSION=v21.0                         # WhatsApp API version
DEBUG_PRINT_REPLY=1                         # Set to 1 for dry-run mode
```

---

## 🚀 Quick Setup Guide

### Step 1: Get WhatsApp Credentials
1. Visit https://developers.facebook.com/
2. Create account → Create App → Add WhatsApp
3. Copy Token and Phone Number ID

### Step 2: Setup ngrok (for local testing)
1. Visit https://ngrok.com/
2. Sign up and download
3. Run: `ngrok config add-authtoken YOUR_TOKEN`
4. Run: `ngrok http 8000`

### Step 3: Configure Webhook
1. Use ngrok URL: `https://your-url.ngrok.io/webhook`
2. Set Verify Token: `cyberbot123`
3. Subscribe to `messages` events

### Step 4: Test
1. Send "start" to your WhatsApp number
2. Follow the chatbot flow

---

## 💰 Total Cost

**Development/Testing**: $0 (completely FREE)

**Production** (if needed):
- WhatsApp Business API: Pay per conversation (after free tier)
- ngrok: Optional paid plan for static domain
- Hosting: Can use free tiers (Heroku, Railway, etc.)

---

## 🔒 Security Notes

- All credentials stored in `.env` file (not committed to git)
- WhatsApp tokens should be kept secret
- Use HTTPS for webhooks (ngrok provides this)
- Database is local and secure

---

## 📞 Support

- WhatsApp API Docs: https://developers.facebook.com/docs/whatsapp
- ngrok Docs: https://ngrok.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/

---

**Last Updated**: 2024  
**All services verified as FREE for development use**

