import requests, json
from .config import WHATSAPP_TOKEN, PHONE_NUMBER_ID, GRAPH_VERSION, DEBUG_PRINT_REPLY

def _should_send():
    return bool(WHATSAPP_TOKEN and PHONE_NUMBER_ID)

def send_message(to: str, text: str):
    """Send a text message to a user via WhatsApp Cloud API.
    If credentials are not set, fallback to printing (helpful for local dev).
    """
    if not _should_send():
        if DEBUG_PRINT_REPLY == "1":
            print(f"[DRY-RUN] To: {to} | Message: {text}")
        return {"ok": True, "dry_run": True}

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    r = requests.post(url, json=payload, headers=headers, timeout=10)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "status_code": r.status_code, "text": r.text}
