# 1930 WhatsApp Chatbot Starter (Modular)

This project is a hackathon-ready starter that implements a modular FastAPI backend for a WhatsApp chatbot.
Key features:
- "start" to open menu (New Complaint, Check Status, Help)
- Guided complaint flow with categories and multi-step Q&A
- SQLite backend (no external paid services required)
- Dry-run mode: if WHATSAPP_TOKEN is not set, bot prints replies instead of sending
- Lightweight dashboard to view complaints and download PDFs (PDF generation endpoint included)
- Simulate webhook locally with `simulate_webhook.py`

## Quick start (local)

1. create virtualenv and install:
    python -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements.txt

2. create .env in project root and add:
    VERIFY_TOKEN=cyberbot123
    WHATSAPP_TOKEN=   # paste token if you have one
    PHONE_NUMBER_ID=  # paste phone number id if you have one
    GRAPH_VERSION=v21.0

3. run backend:
    cd backend
    uvicorn backend.main:app --reload --port 8000

4. (optional) run simulator in parallel window:
    python3 simulate_webhook.py

5. (optional) expose via ngrok/cloudflared and set webhook in Meta dashboard:
    ngrok http 8000
    Set Callback URL to https://<your-tunnel>/webhook and Verify Token to the value in .env

## Notes
- This repo intentionally keeps sending logic abstracted in `whatsapp_api.py`.
- For production use: create long-lived WhatsApp token, secure .env, add auth for dashboard, and harden the server.
