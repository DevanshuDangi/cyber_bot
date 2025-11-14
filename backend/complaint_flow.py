from .whatsapp_api import send_message
from .utils import loads, dumps

FLOWS = {
    "financial": [
        "Amount lost (₹)?",
        "Date & time of transaction?",
        "Bank/app used?",
        "UPI ID / account details of recipient (if any)?"
    ],
    "account_compromise": [
        "Which platform (WhatsApp/Instagram/etc.)?",
        "Approx time when you lost access?",
        "Have you enabled 2FA before? (yes/no)",
        "Phone/email linked to the account?"
    ],
    "online_harassment": [
        "Platform/user handle?",
        "Describe the content or threat briefly.",
        "Do you have screenshots? (yes/no)",
        "Have you blocked the offender? (yes/no)"
    ],
    "other": [
        "Briefly describe what happened.",
        "Where did it occur (platform/app)?",
        "Any monetary loss? If yes, how much (₹)?"
    ]
}

def start_flow(db, wa_id, category="other"):
    # create new complaint and return first question
    from .models import Complaint, ConversationState
    c = Complaint(wa_id=wa_id, category=category, data=dumps({}))
    db.add(c); db.commit(); db.refresh(c)
    # set conv state
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        cs = ConversationState(wa_id=wa_id, state=f"new_complaint:0", meta=dumps({}))
        db.add(cs)
    else:
        cs.state = f"new_complaint:0"
        cs.meta = dumps({})
    db.commit()
    q = FLOWS.get(category, FLOWS['other'])[0]
    send_message(wa_id, f"New complaint created (ID: {c.id}).\n{q}")
    return c.id

def handle_answer(db, wa_id, text):
    from .models import Complaint, ConversationState
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs or not cs.state.startswith("new_complaint") :
        send_message(wa_id, "No active complaint. Send 'start' to open the menu.")
        return

    step = int(cs.state.split(":")[1])
    # find complaint (latest draft)
    comp = db.query(Complaint).filter_by(wa_id=wa_id).order_by(Complaint.id.desc()).first()
    if not comp:
        send_message(wa_id, "Internal error: no complaint found. Please restart.")
        cs.state = "idle"; cs.meta = dumps({}); db.commit(); return

    # get flow
    flow = FLOWS.get(comp.category, FLOWS['other'])
    meta = loads(cs.meta)
    meta[f"answer_{step+1}"] = text.strip()
    cs.meta = dumps(meta)
    step += 1
    if step < len(flow):
        cs.state = f"new_complaint:{step}"
        db.commit()
        send_message(wa_id, flow[step])
        return
    else:
        # finish
        comp.data = dumps(meta)
        comp.status = "submitted"
        db.commit()

        # generate & save PDF (calls the new reports module)
        try:
            from .reports import save_pdf_for_complaint
            save_pdf_for_complaint(comp)
        except Exception as e:
            # don't break user flow if PDF generation fails
            print("PDF generation error:", e)

        cs.state = "idle"
        cs.meta = dumps({})
        db.commit()
        send_message(wa_id, f"Thank you — your complaint (ID: {comp.id}) has been submitted. Our team will follow up.")
        return
