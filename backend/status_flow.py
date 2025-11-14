from .whatsapp_api import send_message
from .utils import loads, dumps, validate_phone
from .complaint_flow import PERSONAL_INFO_FIELDS

def start_status_check(db, wa_id):
    """Start status check flow"""
    from .models import ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        cs = ConversationState(wa_id=wa_id, state="status_check:ask_reference", meta=dumps({}))
        db.add(cs)
    else:
        cs.state = "status_check:ask_reference"
        cs.meta = dumps({})
    db.commit()
    
    send_message(wa_id, "Please provide your Acknowledgement Number or Mobile Number:")

def handle_status_reference(db, wa_id, reference_or_phone):
    """Handle acknowledgement number or phone number input"""
    from .models import Complaint, ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    reference_or_phone = reference_or_phone.strip()
    
    # Try to find complaint by reference number or phone
    complaint = None
    if reference_or_phone.startswith("1930-"):
        complaint = db.query(Complaint).filter_by(reference_number=reference_or_phone).first()
    elif validate_phone(reference_or_phone):
        complaint = db.query(Complaint).filter_by(phone_number=reference_or_phone).order_by(Complaint.created_at.desc()).first()
    
    if not complaint:
        send_message(wa_id, "No complaint found with the provided reference number or mobile number. Please check and try again, or send 'start' to file a new complaint.")
        cs.state = "idle"
        cs.meta = dumps({})
        db.commit()
        return
    
    # Store complaint ID and start collecting personal details
    cs.state = "status_check:personal_info:0"
    cs.meta = dumps({"complaint_id": complaint.id, "field_index": 0})
    db.commit()
    
    send_message(wa_id, f"Found complaint: {complaint.reference_number}\n\nPlease provide your details for verification:\n\n{PERSONAL_INFO_FIELDS[0][1]}:")

def handle_status_personal_info(db, wa_id, text):
    """Handle personal information for status check"""
    from .models import Complaint, ConversationState
    from .utils import validate_phone, validate_email, validate_pin_code, validate_date_of_birth
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    field_index = meta.get("field_index", 0)
    
    if field_index >= len(PERSONAL_INFO_FIELDS):
        # All info collected, show status
        complaint = db.query(Complaint).filter_by(id=complaint_id).first()
        if complaint:
            status_msg = f"📋 Complaint Status\n\n"
            status_msg += f"Reference Number: {complaint.reference_number}\n"
            status_msg += f"Status: {complaint.status.upper()}\n"
            status_msg += f"Category: {complaint.main_category.replace('_', ' ').title()}\n"
            if complaint.fraud_type:
                status_msg += f"Fraud Type: {complaint.fraud_type}\n"
            status_msg += f"Created: {complaint.created_at.strftime('%d/%m/%Y %H:%M')}\n"
            status_msg += f"Updated: {complaint.updated_at.strftime('%d/%m/%Y %H:%M')}\n\n"
            status_msg += "Our agent will call or message you shortly to solve your issue."
            
            send_message(wa_id, status_msg)
        else:
            send_message(wa_id, "Error: Complaint not found.")
        
        cs.state = "idle"
        cs.meta = dumps({})
        db.commit()
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
    
    # Move to next field
    field_index += 1
    if field_index < len(PERSONAL_INFO_FIELDS):
        cs.state = f"status_check:personal_info:{field_index}"
        cs.meta = dumps({"complaint_id": complaint_id, "field_index": field_index})
        db.commit()
        next_field_label = PERSONAL_INFO_FIELDS[field_index][1]
        send_message(wa_id, f"{next_field_label}:")
    else:
        # All info collected, show status
        complaint = db.query(Complaint).filter_by(id=complaint_id).first()
        if complaint:
            status_msg = f"📋 Complaint Status\n\n"
            status_msg += f"Reference Number: {complaint.reference_number}\n"
            status_msg += f"Status: {complaint.status.upper()}\n"
            status_msg += f"Category: {complaint.main_category.replace('_', ' ').title()}\n"
            if complaint.fraud_type:
                status_msg += f"Fraud Type: {complaint.fraud_type}\n"
            status_msg += f"Created: {complaint.created_at.strftime('%d/%m/%Y %H:%M')}\n"
            status_msg += f"Updated: {complaint.updated_at.strftime('%d/%m/%Y %H:%M')}\n\n"
            status_msg += "Our agent will call or message you shortly to solve your issue."
            
            send_message(wa_id, status_msg)
        
        cs.state = "idle"
        cs.meta = dumps({})
        db.commit()

def check_status(db, wa_id):
    """Legacy function for backward compatibility"""
    start_status_check(db, wa_id)
