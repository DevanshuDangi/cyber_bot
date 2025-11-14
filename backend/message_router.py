from fastapi import HTTPException
from .whatsapp_api import send_message
from .utils import loads
from . import complaint_flow, status_flow, account_unfreeze_flow
from .models import ConversationState

def route_message(db, wa_id, text, is_image=False, image_url=None):
    """Route incoming messages to appropriate handlers"""
    text_norm = (text or "").strip().lower()
    
    # Ensure user has a conversation state object
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        cs = ConversationState(wa_id=wa_id, state="idle", meta="{}")
        db.add(cs)
        db.commit()
        db.refresh(cs)

    # Handle start/menu commands
    if text_norm in ["start", "menu", "hi", "hello", "help"]:
        cs.state = "menu"
        cs.meta = "{}"
        db.commit()
        menu = ("Welcome to 1930 Cyber Crime Helpline, Odisha!\n\n"
                "Please select an option:\n"
                "A. For New Complaint\n"
                "B. For Status Check in Existing Complaint\n"
                "C. For Account Unfreeze Related\n"
                "D. Other Queries\n\n"
                "Reply with A, B, C, or D:")
        send_message(wa_id, menu)
        return

    # Handle menu selections
    if cs.state == "menu":
        if text_norm in ["a", "a.", "new complaint", "new"]:
            complaint_flow.start_new_complaint_flow(db, wa_id, complaint_type="A")
            return
        elif text_norm in ["b", "b.", "status", "status check", "check status"]:
            status_flow.start_status_check(db, wa_id)
            return
        elif text_norm in ["c", "c.", "account unfreeze", "unfreeze"]:
            account_unfreeze_flow.start_account_unfreeze(db, wa_id)
            return
        elif text_norm in ["d", "d.", "other", "other queries", "queries"]:
            send_message(wa_id, "For other queries, please contact our helpline directly or send 'start' to access the main menu.")
            cs.state = "idle"
            db.commit()
            return
        else:
            send_message(wa_id, "Invalid selection. Please reply with A, B, C, or D:")
            return

    # Handle new complaint flow
    if cs.state.startswith("new_complaint"):
        # Handle category selection
        if cs.state == "new_complaint:choose_category":
            if text_norm in ["1", "financial", "financial fraud"]:
                cs.state = "new_complaint:financial_type"
                db.commit()
                send_message(wa_id, complaint_flow.get_financial_fraud_menu())
                return
            elif text_norm in ["2", "social", "social media", "social media fraud"]:
                cs.state = "new_complaint:social_platform"
                db.commit()
                send_message(wa_id, complaint_flow.get_social_media_menu())
                return
            else:
                send_message(wa_id, "Invalid selection. Please reply with 1 or 2:")
                return
        
        # Handle financial fraud type
        if cs.state == "new_complaint:financial_type":
            complaint_flow.handle_financial_fraud_type(db, wa_id, text.strip())
            return
        
        # Handle social media platform
        if cs.state == "new_complaint:social_platform":
            complaint_flow.handle_social_media_platform(db, wa_id, text.strip())
            return
        
        # Handle social media subtype
        if cs.state == "new_complaint:social_subtype":
            complaint_flow.handle_social_media_subtype(db, wa_id, text.strip())
            return
        
        # Handle personal info collection
        if cs.state.startswith("new_complaint:personal_info:"):
            complaint_flow.handle_personal_info_answer(db, wa_id, text)
            return
        
        # Handle document collection
        if cs.state == "new_complaint:documents" or cs.state == "new_complaint:documents:collecting":
            if is_image and image_url:
                complaint_flow.handle_document_upload(db, wa_id, image_url)
            elif text_norm == "done":
                complaint_flow.finalize_complaint(db, wa_id)
            else:
                send_message(wa_id, "Please send images/photos or type 'done' to finish:")
            return
        
        # Fallback to general handler
        complaint_flow.handle_answer(db, wa_id, text, is_image, image_url)
        return

    # Handle status check flow
    if cs.state.startswith("status_check"):
        if cs.state == "status_check:ask_reference":
            status_flow.handle_status_reference(db, wa_id, text)
            return
        elif cs.state.startswith("status_check:personal_info:"):
            status_flow.handle_status_personal_info(db, wa_id, text)
            return

    # Handle account unfreeze flow
    if cs.state.startswith("account_unfreeze"):
        if cs.state == "account_unfreeze:ask_account":
            account_unfreeze_flow.handle_account_number(db, wa_id, text)
            return
        elif cs.state.startswith("account_unfreeze:personal_info:"):
            account_unfreeze_flow.handle_account_unfreeze_personal_info(db, wa_id, text)
            return

    # Fallback: if in any active state, try to handle it
    if cs.state != "idle":
        send_message(wa_id, "I didn't understand that. Please follow the prompts or send 'start' to restart.")
        return

    # Default fallback
    send_message(wa_id, "Sorry, I didn't understand. Send 'start' to see the menu.")
