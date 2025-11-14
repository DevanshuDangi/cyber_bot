from .whatsapp_api import send_message
from .utils import loads

def check_status(db, wa_id):
    from .models import Complaint
    comp = db.query(Complaint).filter_by(wa_id=wa_id).order_by(Complaint.id.desc()).first()
    if not comp:
        send_message(wa_id, "No complaints found. Send 'start' and choose New Complaint to report.")
        return
    # simple status message
    msg = f"Complaint ID: {comp.id}\nStatus: {comp.status}\nCategory: {comp.category}\nCreated: {comp.created_at}"
    data = loads(comp.data)
    if data:
        msg += "\n--- Details ---\n" + "\n".join([f"{k}: {v}" for k,v in data.items()])
    send_message(wa_id, msg)
