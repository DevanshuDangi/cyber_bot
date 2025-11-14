from fastapi import HTTPException
from .whatsapp_api import send_message, send_interactive_buttons, send_interactive_list
from .utils import loads
from . import complaint_flow, status_flow, account_unfreeze_flow
from .models import ConversationState
from . import nlu

def route_message(db, wa_id, text, is_image=False, image_url=None):
    """Route incoming messages to appropriate handlers"""
    text_norm = (text or "").strip().lower()
    original_text = text or ""
    
    # Ensure user has a conversation state object
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        cs = ConversationState(wa_id=wa_id, state="idle", meta="{}")
        db.add(cs)
        db.commit()
        db.refresh(cs)
    
    # NLU: Check if user wants to file a complaint from free text (when idle)
    if cs.state == "idle" and original_text and not is_image:
        should_route, complaint_type = nlu.should_route_to_complaint(original_text)
        if should_route and complaint_type:
            print(f"[NLU] Detected complaint intent: {complaint_type}")
            if complaint_type == "financial":
                complaint_flow.start_new_complaint_flow(db, wa_id, complaint_type="A")
                # Auto-select financial fraud
                cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
                if cs:
                    cs.state = "new_complaint:financial_type"
                    db.commit()
                complaint_flow.send_financial_fraud_interactive(wa_id)
            elif complaint_type == "social":
                complaint_flow.start_new_complaint_flow(db, wa_id, complaint_type="A")
                # Auto-select social media fraud
                cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
                if cs:
                    cs.state = "new_complaint:social_platform"
                    db.commit()
                complaint_flow.send_social_media_interactive(wa_id)
            return

    # Handle start/menu commands
    if text_norm in ["start", "menu", "hi", "hello", "help"]:
        cs.state = "menu"
        cs.meta = "{}"
        db.commit()
        menu_text = "Welcome to 1930 Cyber Crime Helpline, Odisha!\n\nPlease select an option:"
        buttons = [
            {"id": "A", "title": "New Complaint"},
            {"id": "B", "title": "Status Check"},
            {"id": "C", "title": "Account Unfreeze"},
            {"id": "D", "title": "Other Queries"}
        ]
        # Send as buttons (max 3) or fallback to text
        if len(buttons) <= 3:
            send_interactive_buttons(wa_id, menu_text, buttons)
        else:
            # Split into multiple button messages or use list
            send_interactive_buttons(wa_id, menu_text, buttons[:3])
            send_message(wa_id, "Or type D for Other Queries")
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
            # Use Gemini NLU to handle other queries
            cs.state = "other_query"
            db.commit()
            response = nlu.handle_other_query(original_text if original_text else "I need help")
            send_message(wa_id, response)
            # Offer to return to menu
            buttons = [
                {"id": "start", "title": "Back to Menu"},
                {"id": "help", "title": "More Help"}
            ]
            send_interactive_buttons(wa_id, "Would you like to:", buttons)
            return
        else:
            # Use Gemini NLU to understand unclear menu selection
            response = nlu.handle_unclear_input(original_text, context="User is at main menu")
            send_message(wa_id, response)
            # Resend menu
            menu_text = "Welcome to 1930 Cyber Crime Helpline, Odisha!\n\nPlease select an option:"
            buttons = [
                {"id": "A", "title": "New Complaint"},
                {"id": "B", "title": "Status Check"},
                {"id": "C", "title": "Account Unfreeze"},
                {"id": "D", "title": "Other Queries"}
            ]
            if len(buttons) <= 3:
                send_interactive_buttons(wa_id, menu_text, buttons)
            else:
                send_interactive_buttons(wa_id, menu_text, buttons[:3])
                send_message(wa_id, "Or type D for Other Queries")
            return

    # Handle new complaint flow
    if cs.state.startswith("new_complaint"):
        # Handle category selection
        if cs.state == "new_complaint:choose_category":
            # Handle both button ID ("1") and button title ("Financial Fraud")
            if text_norm in ["1", "financial", "financial fraud"] or "financial fraud" in text_norm:
                print(f"[DEBUG] Category selected: Financial Fraud (input: {text})")
                cs.state = "new_complaint:financial_type"
                db.commit()
                result = complaint_flow.send_financial_fraud_interactive(wa_id)
                print(f"[DEBUG] Interactive list send result: {result}")
                return
            elif text_norm in ["2", "social", "social media", "social media fraud"] or "social media" in text_norm:
                cs.state = "new_complaint:social_platform"
                db.commit()
                complaint_flow.send_social_media_interactive(wa_id)
                return
            else:
                # Use Gemini NLU to understand unclear category selection
                response = nlu.handle_unclear_input(original_text, context="User is selecting complaint category (Financial or Social Media)")
                send_message(wa_id, response)
                # Resend category buttons
                buttons = [
                    {"id": "1", "title": "Financial Fraud"},
                    {"id": "2", "title": "Social Media Fraud"}
                ]
                send_interactive_buttons(wa_id, "Please choose:", buttons)
                return
        
        # Handle financial fraud type
        if cs.state == "new_complaint:financial_type":
            print(f"[DEBUG] Financial fraud type selected: {text.strip()}")
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
            # Handle button clicks
            if text_norm in ["done", "✅ done", "done"]:
                complaint_flow.finalize_complaint(db, wa_id)
                return
            elif text_norm in ["send_more", "send more", "📎 send more", "more"]:
                # User wants to send more documents
                buttons = [
                    {"id": "done", "title": "✅ Done"},
                    {"id": "send_more", "title": "📎 Send More"}
                ]
                send_interactive_buttons(wa_id, "Please send your document (image/photo):", buttons)
                return
            elif is_image and image_url:
                complaint_flow.handle_document_upload(db, wa_id, image_url)
                return
            else:
                # Invalid input, show buttons again
                buttons = [
                    {"id": "done", "title": "✅ Done"},
                    {"id": "send_more", "title": "📎 Send More"}
                ]
                send_interactive_buttons(wa_id, "Please send images/photos or select an option:", buttons)
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
    
    # Handle other query state (after option D)
    if cs.state == "other_query":
        if text_norm in ["start", "back to menu", "menu"]:
            cs.state = "menu"
            cs.meta = "{}"
            db.commit()
            menu_text = "Welcome to 1930 Cyber Crime Helpline, Odisha!\n\nPlease select an option:"
            buttons = [
                {"id": "A", "title": "New Complaint"},
                {"id": "B", "title": "Status Check"},
                {"id": "C", "title": "Account Unfreeze"},
                {"id": "D", "title": "Other Queries"}
            ]
            if len(buttons) <= 3:
                send_interactive_buttons(wa_id, menu_text, buttons)
            else:
                send_interactive_buttons(wa_id, menu_text, buttons[:3])
                send_message(wa_id, "Or type D for Other Queries")
            return
        elif text_norm in ["help", "more help"]:
            response = nlu.handle_other_query(original_text if original_text else "I need more help")
            send_message(wa_id, response)
            return
        else:
            # Continue conversation with Gemini
            response = nlu.handle_other_query(original_text)
            send_message(wa_id, response)
            return

    # Fallback: if in any active state, use Gemini NLU to understand
    if cs.state != "idle":
        response = nlu.handle_unclear_input(original_text, context=f"User is in state: {cs.state}")
        send_message(wa_id, response)
        # Offer to restart
        buttons = [
            {"id": "start", "title": "Restart"}
        ]
        send_interactive_buttons(wa_id, "Would you like to start over?", buttons)
        return

    # Default fallback: use Gemini NLU
    intent, confidence = nlu.detect_intent(original_text)
    if intent != "unknown" and confidence > 0.6:
        # Route based on detected intent
        if intent == "new_complaint_financial":
            complaint_flow.start_new_complaint_flow(db, wa_id, complaint_type="A")
            cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
            if cs:
                cs.state = "new_complaint:financial_type"
                db.commit()
            complaint_flow.send_financial_fraud_interactive(wa_id)
        elif intent == "new_complaint_social":
            complaint_flow.start_new_complaint_flow(db, wa_id, complaint_type="A")
            cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
            if cs:
                cs.state = "new_complaint:social_platform"
                db.commit()
            complaint_flow.send_social_media_interactive(wa_id)
        elif intent == "status_check":
            status_flow.start_status_check(db, wa_id)
        elif intent == "account_unfreeze":
            account_unfreeze_flow.start_account_unfreeze(db, wa_id)
        else:
            response = nlu.handle_other_query(original_text)
            send_message(wa_id, response)
    else:
        # Use Gemini for general response
        response = nlu.handle_unclear_input(original_text)
        send_message(wa_id, response)
        # Show menu
        buttons = [
            {"id": "start", "title": "See Menu"}
        ]
        send_interactive_buttons(wa_id, "Send 'start' to see the menu:", buttons)
