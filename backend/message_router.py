from fastapi import HTTPException
from .whatsapp_api import send_message
from .utils import loads
from . import complaint_flow, status_flow
from .models import ConversationState

def route_message(db, wa_id, text):
    text_norm = (text or "").strip().lower()
    # ensure user has a conversation state object
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        cs = ConversationState(wa_id=wa_id, state="idle", meta="{}")
        db.add(cs); db.commit(); db.refresh(cs)

    # If user types 'start' or 'menu'
    if text_norm in ["start", "menu", "hi", "hello"]:
        cs.state = "menu"; cs.meta = "{}"; db.commit()
        menu = ("Welcome to 1930 Cybercrime Bot!\n"
                "Reply with the number:\n"
                "1. New Complaint\n"
                "2. Check Complaint Status\n"
                "3. Help / Info\n")
        send_message(wa_id, menu)
        return

    # If in a new complaint flow
    if cs.state.startswith("new_complaint"):
        complaint_flow.handle_answer(db, wa_id, text)
        return

    # If user responded with menu option
    if cs.state == "menu" and text_norm in ["1","1.","new complaint","new"]:
        # ask category selection
        send_message(wa_id, "Choose category:\n1. Financial Fraud\n2. Account Compromise\n3. Online Harassment\n4. Other\nReply with 1-4.")
        cs.state = "menu:choose_category"; db.commit(); return
    if cs.state == "menu:choose_category" and text_norm in ["1","2","3","4"]:
        mapping = {"1":"financial","2":"account_compromise","3":"online_harassment","4":"other"}
        category = mapping.get(text_norm, "other")
        complaint_flow.start_flow(db, wa_id, category=category); return

    if cs.state == "menu" and text_norm in ["2","2.","check","status","check status"]:
        status_flow.check_status(db, wa_id); return

    if cs.state == "menu" and text_norm in ["3","3.","help","info"]:
        send_message(wa_id, "This bot helps you report cybercrimes to 1930 team. Use '1' to file a complaint or '2' to check status."); return

    # fallback:
    send_message(wa_id, "Sorry, I didn't understand. Send 'start' to see the menu.")
