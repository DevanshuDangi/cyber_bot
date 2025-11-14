import os
import requests, json
from .config import WHATSAPP_TOKEN, PHONE_NUMBER_ID, GRAPH_VERSION, DEBUG_PRINT_REPLY

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
os.makedirs(MEDIA_DIR, exist_ok=True)

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
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.json()
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return {"ok": False, "error": str(e)}

def send_image(to: str, image_url: str, caption: str = ""):
    """Send an image message via WhatsApp Cloud API.
    image_url: Public URL of the image
    caption: Optional caption text
    """
    if not _should_send():
        if DEBUG_PRINT_REPLY == "1":
            print(f"[DRY-RUN] To: {to} | Image: {image_url} | Caption: {caption}")
        return {"ok": True, "dry_run": True}

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption[:1024] if caption else ""
        }
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.json()
    except Exception as e:
        print(f"Error sending WhatsApp image: {e}")
        return {"ok": False, "error": str(e)}

def download_media(media_id: str, media_url: str = None):
    """Download media (image/document) and return a /media/... path the UI can load."""
    filename = f"{media_id}.jpg"
    file_path = os.path.join(MEDIA_DIR, filename)
    relative_path = f"/media/{filename}"

    if not _should_send():
        # Dry-run mode cannot download, but keep path consistent
        return relative_path

    if media_url:
        try:
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
            response = requests.get(media_url, headers=headers, timeout=30)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            return relative_path
        except Exception as e:
            print(f"Error downloading media: {e}")

    return relative_path
