import requests, json
import os
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
    """Download media (image/document) from WhatsApp Cloud API.
    Returns the file path or URL where the media is stored.
    For now, returns the media_url if provided, or media_id.
    In production, you would download and store the file locally.
    """
    if not _should_send():
        # In dry-run mode, return a placeholder
        return f"media_{media_id}.jpg"
    
    # If media_url is provided, download it
    if media_url:
        try:
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
            response = requests.get(media_url, headers=headers, timeout=30)
            if response.status_code == 200:
                # Save to local storage
                media_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media")
                os.makedirs(media_dir, exist_ok=True)
                file_path = os.path.join(media_dir, f"{media_id}.jpg")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return file_path
        except Exception as e:
            print(f"Error downloading media: {e}")
    
    # Fallback: return media_id or URL
    return media_url or f"media_{media_id}"
