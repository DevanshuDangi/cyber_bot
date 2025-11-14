from .whatsapp_api import send_message
from .utils import loads, dumps, validate_phone, validate_email, validate_pin_code, validate_date_of_birth
from .complaint_flow import PERSONAL_INFO_FIELDS

def start_account_unfreeze(db, wa_id):
    """Start account unfreeze flow"""
    from .models import ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        cs = ConversationState(wa_id=wa_id, state="account_unfreeze:ask_account", meta=dumps({}))
        db.add(cs)
    else:
        cs.state = "account_unfreeze:ask_account"
        cs.meta = dumps({})
    db.commit()
    
    send_message(wa_id, "Please provide your Account Number:")

def handle_account_number(db, wa_id, account_number):
    """Handle account number input"""
    from .models import Complaint, ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    account_number = account_number.strip()
    
    # Create a complaint record for account unfreeze
    complaint = Complaint(
        wa_id=wa_id,
        complaint_type="C",
        main_category="account_unfreeze",
        account_number=account_number,
        status="draft"
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    
    # Start collecting personal details
    cs.state = "account_unfreeze:personal_info:0"
    cs.meta = dumps({"complaint_id": complaint.id, "field_index": 0})
    db.commit()
    
    send_message(wa_id, f"Account Number: {account_number}\n\nPlease provide your details:\n\n{PERSONAL_INFO_FIELDS[0][1]}:")

def handle_account_unfreeze_personal_info(db, wa_id, text):
    """Handle personal information for account unfreeze"""
    from .models import Complaint, ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    field_index = meta.get("field_index", 0)
    complaint = db.query(Complaint).filter_by(id=complaint_id).first()
    
    if not complaint:
        send_message(wa_id, "Error: Complaint not found. Please send 'start' to begin again.")
        return
    
    if field_index >= len(PERSONAL_INFO_FIELDS):
        # All info collected, finalize
        from .utils import generate_reference_number
        reference_number = generate_reference_number(complaint.id)
        complaint.reference_number = reference_number
        complaint.status = "submitted"
        db.commit()
        
        # Generate PDF
        try:
            from .reports import save_pdf_for_complaint
            save_pdf_for_complaint(complaint)
        except Exception as e:
            print(f"PDF generation error: {e}")
        
        cs.state = "idle"
        cs.meta = dumps({})
        db.commit()
        
        send_message(wa_id, f"✅ Account Unfreeze Request Submitted!\n\n📋 Reference Number: {reference_number}\n\nOur agent will call or message you shortly to solve your issue.\n\nThank you for using 1930 Cyber Crime Helpline, Odisha.")
        return
    
    field_name, field_label = PERSONAL_INFO_FIELDS[field_index]
    text = text.strip()
    
    # Validation
    if field_name == "phone_number" and not validate_phone(text):
        send_message(wa_id, "Invalid phone number. Please enter a valid 10-digit Indian phone number:")
        return
    
    if field_name == "email_id" and not validate_email(text):
        send_message(wa_id, "Invalid email address. Please enter a valid email:")
        return
    
    if field_name == "pin_code" and not validate_pin_code(text):
        send_message(wa_id, "Invalid PIN code. Please enter a valid 6-digit PIN code:")
        return
    
    if field_name == "date_of_birth" and not validate_date_of_birth(text):
        send_message(wa_id, "Invalid date format. Please enter date in DD/MM/YYYY format:")
        return
    
    # Save the answer
    setattr(complaint, field_name, text)
    db.commit()
    
    # Move to next field
    field_index += 1
    if field_index < len(PERSONAL_INFO_FIELDS):
        cs.state = f"account_unfreeze:personal_info:{field_index}"
        cs.meta = dumps({"complaint_id": complaint_id, "field_index": field_index})
        db.commit()
        next_field_label = PERSONAL_INFO_FIELDS[field_index][1]
        send_message(wa_id, f"{next_field_label}:")
    else:
        # All info collected, finalize
        from .utils import generate_reference_number
        reference_number = generate_reference_number(complaint.id)
        complaint.reference_number = reference_number
        complaint.status = "submitted"
        db.commit()
        
        # Generate PDF
        try:
            from .reports import save_pdf_for_complaint
            save_pdf_for_complaint(complaint)
        except Exception as e:
            print(f"PDF generation error: {e}")
        
        cs.state = "idle"
        cs.meta = dumps({})
        db.commit()
        
        send_message(wa_id, f"✅ Account Unfreeze Request Submitted!\n\n📋 Reference Number: {reference_number}\n\nOur agent will call or message you shortly to solve your issue.\n\nThank you for using 1930 Cyber Crime Helpline, Odisha.")

