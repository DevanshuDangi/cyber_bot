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

def send_interactive_buttons(to: str, text: str, buttons: list):
    """Send an interactive button message.
    buttons: List of dicts with 'id' and 'title' keys. Max 3 buttons.
    Example: [{"id": "A", "title": "New Complaint"}, {"id": "B", "title": "Status Check"}]
    """
    if not _should_send():
        if DEBUG_PRINT_REPLY == "1":
            button_text = "\n".join([f"[{b.get('id', '')}] {b.get('title', '')}" for b in buttons])
            print(f"[DRY-RUN] To: {to} | Interactive Buttons:\n{text}\n{button_text}")
        return {"ok": True, "dry_run": True}

    if len(buttons) > 3:
        buttons = buttons[:3]  # WhatsApp allows max 3 buttons

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    interactive_buttons = []
    for btn in buttons:
        interactive_buttons.append({
            "type": "reply",
            "reply": {
                "id": str(btn.get("id", "")),
                "title": btn.get("title", "")[:20]  # Max 20 chars
            }
        })
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text[:1024]},
            "action": {
                "buttons": interactive_buttons
            }
        }
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        result = r.json()
        
        # Check if message was sent successfully
        if result.get("messages"):
            print(f"[DEBUG] Interactive buttons sent successfully to {to}")
            return result
        
        # If there's an error, log it and fallback
        if result.get("error"):
            error_msg = result.get("error", {}).get("message", "Unknown error")
            print(f"[ERROR] Failed to send interactive buttons to {to}: {error_msg}")
            print(f"[DEBUG] Falling back to text message")
            # Fallback to text message if interactive fails
            button_text = "\n".join([f"{b.get('id', '')}. {b.get('title', '')}" for b in buttons])
            fallback_text = text + "\n\n" + button_text
            return send_message(to, fallback_text)
        
        # If no messages and no error, something unexpected happened
        print(f"[WARNING] Unexpected response from WhatsApp API: {result}")
        button_text = "\n".join([f"{b.get('id', '')}. {b.get('title', '')}" for b in buttons])
        fallback_text = text + "\n\n" + button_text
        return send_message(to, fallback_text)
        
    except Exception as e:
        print(f"[ERROR] Exception sending interactive buttons to {to}: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to text message
        button_text = "\n".join([f"{b.get('id', '')}. {b.get('title', '')}" for b in buttons])
        fallback_text = text + "\n\n" + button_text
        return send_message(to, fallback_text)

def send_interactive_list(to: str, text: str, button_text: str, sections: list):
    """Send an interactive list message.
    sections: List of dicts with 'title' and 'rows' (list of {id, title, description})
    Example: [{"title": "Fraud Types", "rows": [{"id": "1", "title": "UPI Fraud"}]}]
    """
    if not _should_send():
        if DEBUG_PRINT_REPLY == "1":
            list_text = "\n".join([
                f"{row.get('id', '')}. {row.get('title', '')}" 
                for section in sections 
                for row in section.get('rows', [])
            ])
            print(f"[DRY-RUN] To: {to} | Interactive List:\n{text}\n{list_text}")
        return {"ok": True, "dry_run": True}

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Format sections for WhatsApp API
    formatted_sections = []
    for section in sections[:10]:  # Max 10 sections
        rows = []
        for row in section.get('rows', [])[:10]:  # Max 10 rows per section
            rows.append({
                "id": str(row.get("id", "")),
                "title": row.get("title", "")[:24],  # Max 24 chars
                "description": row.get("description", "")[:72] if row.get("description") else ""  # Max 72 chars
            })
        if rows:
            formatted_sections.append({
                "title": section.get("title", "")[:24],
                "rows": rows
            })
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": text[:1024]},
            "action": {
                "button": button_text[:20],
                "sections": formatted_sections
            }
        }
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        result = r.json()
        
        # Check if message was sent successfully
        if result.get("messages"):
            print(f"[DEBUG] Interactive list sent successfully to {to}")
            return result
        
        # If there's an error, log it and fallback
        if result.get("error"):
            error_msg = result.get("error", {}).get("message", "Unknown error")
            print(f"[ERROR] Failed to send interactive list to {to}: {error_msg}")
            print(f"[DEBUG] Falling back to text message")
            # Fallback to text message if interactive fails
            fallback_text = text + "\n\n" + "\n".join([
                f"{row.get('id', '')}. {row.get('title', '')}" 
                for section in sections 
                for row in section.get('rows', [])
            ])
            return send_message(to, fallback_text)
        
        # If no messages and no error, something unexpected happened
        print(f"[WARNING] Unexpected response from WhatsApp API: {result}")
        fallback_text = text + "\n\n" + "\n".join([
            f"{row.get('id', '')}. {row.get('title', '')}" 
            for section in sections 
            for row in section.get('rows', [])
        ])
        return send_message(to, fallback_text)
        
    except Exception as e:
        print(f"[ERROR] Exception sending interactive list to {to}: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to text message
        fallback_text = text + "\n\n" + "\n".join([
            f"{row.get('id', '')}. {row.get('title', '')}" 
            for section in sections 
            for row in section.get('rows', [])
        ])
        return send_message(to, fallback_text)

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
