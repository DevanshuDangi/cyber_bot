import os
from .whatsapp_api import send_message, send_interactive_buttons, send_interactive_list
from .utils import loads, dumps, generate_reference_number, validate_phone, validate_email, validate_pin_code, validate_date_of_birth

# Financial Fraud Types (A1.1)
FINANCIAL_FRAUD_TYPES = {
    "1": "Investment/Trading/IPO Fraud",
    "2": "Customer Care Fraud",
    "3": "UPI Fraud (UPI/IMPS/INB/NEFT/RTGS)",
    "4": "APK Fraud",
    "5": "Fake Franchisee/Dealership Fraud",
    "6": "Online Job Fraud",
    "7": "Debit Card Fraud",
    "8": "Credit Card Fraud",
    "9": "E-Commerce Fraud",
    "10": "Loan App Fraud",
    "11": "Sextortion Fraud",
    "12": "OLX Fraud",
    "13": "Lottery Fraud",
    "14": "Hotel Booking Fraud",
    "15": "Gaming App Fraud",
    "16": "AEPS Fraud (Aadhar Enabled Payment System)",
    "17": "Tower Installation Fraud",
    "18": "E-Wallet Fraud",
    "19": "Digital Arrest Fraud",
    "20": "Fake Website Scam Fraud",
    "21": "Ticket Booking Fraud",
    "22": "Insurance Maturity Fraud",
    "23": "Others"
}

# Social Media Fraud Types (A2.1)
SOCIAL_MEDIA_PLATFORMS = {
    "1": "Facebook",
    "2": "Instagram",
    "3": "X (Twitter)",
    "4": "WhatsApp",
    "5": "Telegram",
    "6": "Gmail/YouTube",
    "7": "Fraud Call/SMS"
}

SOCIAL_MEDIA_SUB_TYPES = {
    "1": "Impersonation Account",
    "2": "Fake Account",
    "3": "Hack",
    "4": "Spread of Obscene content"
}

# Personal Information Fields (Common for A-1 & A-2)
PERSONAL_INFO_FIELDS = [
    ("name", "Name"),
    ("father_spouse_guardian_name", "Father/Spouse/Guardian Name"),
    ("date_of_birth", "Date of Birth (DD/MM/YYYY)"),
    ("phone_number", "Phone Number"),
    ("email_id", "Email ID"),
    ("gender", "Gender (Male/Female/Other)"),
    ("village", "Village"),
    ("post_office", "Post Office"),
    ("police_station", "Police Station"),
    ("district", "District"),
    ("pin_code", "PIN Code")
]

# Document types for Financial Fraud (A1.1.1)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_PREFIX = "/media/"

FINANCIAL_DOCUMENTS = [
    "Aadhar Card / PAN Card",
    "Debit Card/ Credit Card photo",
    "Bank account front page",
    "Bank Statement (highlighting fraudulent transactions with transaction reference number)",
    "Screenshot of debit messages (showing transaction reference number with date and time)",
    "UPI transactions Screenshot (showing UTR number with Date and time)",
    "Credit Card statement or Screenshots of spent message reference number",
    "Beneficiary account details (amount, transaction reference number, date and time)"
]

def get_financial_fraud_menu():
    """Generate menu for financial fraud types - returns text for fallback"""
    menu = "Select the type of Financial Fraud:\n"
    for key, value in FINANCIAL_FRAUD_TYPES.items():
        menu += f"{key}. {value}\n"
    menu += "\nReply with the number (1-23):"
    return menu

def send_financial_fraud_interactive(wa_id):
    """Send financial fraud types as interactive list"""
    from .whatsapp_api import send_interactive_list, send_message
    
    # Split into sections (max 10 rows per section)
    rows = []
    for key, value in FINANCIAL_FRAUD_TYPES.items():
        rows.append({
            "id": key,
            "title": value[:24],
            "description": ""
        })
    
    # Split into sections of 10 rows each
    sections = []
    for i in range(0, len(rows), 10):
        section_rows = rows[i:i+10]
        sections.append({
            "title": f"Types {i+1}-{min(i+10, len(rows))}",
            "rows": section_rows
        })
    
    print(f"[DEBUG] Sending financial fraud interactive list to {wa_id}")
    result = send_interactive_list(
        wa_id,
        "Select the type of Financial Fraud:",
        "Select Fraud Type",
        sections
    )
    
    # The send_interactive_list function already handles fallback internally
    # But we can add an extra check here for safety
    if result and isinstance(result, dict):
        if result.get("dry_run"):
            print(f"[DEBUG] Dry-run mode: interactive list would be sent")
        elif result.get("error") and not result.get("messages"):
            print(f"[DEBUG] Interactive list failed, fallback should have been sent")
        elif result.get("messages"):
            print(f"[DEBUG] Interactive list sent successfully")
    
    return result

def get_social_media_menu():
    """Generate menu for social media platforms - returns text for fallback"""
    menu = "Select the platform:\n"
    for key, value in SOCIAL_MEDIA_PLATFORMS.items():
        menu += f"{key}. {value}\n"
    menu += "\nReply with the number (1-7):"
    return menu

def send_social_media_interactive(wa_id):
    """Send social media platforms as interactive list"""
    from .whatsapp_api import send_interactive_list
    
    rows = []
    for key, value in SOCIAL_MEDIA_PLATFORMS.items():
        rows.append({
            "id": key,
            "title": value[:24],
            "description": ""
        })
    
    sections = [{
        "title": "Platforms",
        "rows": rows
    }]
    
    send_interactive_list(
        wa_id,
        "Select the platform:",
        "Select Platform",
        sections
    )

def get_social_media_subtype_menu():
    """Generate menu for social media fraud subtypes - returns text for fallback"""
    menu = "Select the type of fraud:\n"
    for key, value in SOCIAL_MEDIA_SUB_TYPES.items():
        menu += f"{key}. {value}\n"
    menu += "\nReply with the number (1-4):"
    return menu

def send_social_media_subtype_interactive(wa_id):
    """Send social media subtypes as interactive buttons"""
    from .whatsapp_api import send_interactive_buttons
    
    buttons = []
    for key, value in SOCIAL_MEDIA_SUB_TYPES.items():
        buttons.append({
            "id": key,
            "title": value[:20]
        })
    
    send_interactive_buttons(
        wa_id,
        "Select the type of fraud:",
        buttons
    )

def start_new_complaint_flow(db, wa_id, complaint_type="A"):
    """Start a new complaint flow"""
    from .models import Complaint, ConversationState
    
    # Create new complaint
    complaint = Complaint(
        wa_id=wa_id,
        complaint_type=complaint_type,
        status="draft"
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    
    # Update conversation state
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        cs = ConversationState(wa_id=wa_id, state="new_complaint:choose_category", meta=dumps({"complaint_id": complaint.id}))
        db.add(cs)
    else:
        cs.state = "new_complaint:choose_category"
        cs.meta = dumps({"complaint_id": complaint.id})
    db.commit()
    
    # Ask for category with interactive buttons
    if complaint_type == "A":
        buttons = [
            {"id": "1", "title": "Financial Fraud"},
            {"id": "2", "title": "Social Media Fraud"}
        ]
        send_interactive_buttons(wa_id, "Is your complaint related to:", buttons)
    return complaint.id

def handle_financial_fraud_type(db, wa_id, fraud_type_num):
    """Handle financial fraud type selection"""
    from .models import Complaint, ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return

    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    complaint = db.query(Complaint).filter_by(id=complaint_id).first()
    
    if not complaint:
        send_message(wa_id, "Error: Complaint not found. Please send 'start' to begin again.")
        return
    
    # Normalize the input (strip whitespace, handle both string and numeric)
    fraud_type_num = str(fraud_type_num).strip()
    
    print(f"[DEBUG] Processing financial fraud type: '{fraud_type_num}'")
    print(f"[DEBUG] Available types: {list(FINANCIAL_FRAUD_TYPES.keys())}")
    
    if fraud_type_num in FINANCIAL_FRAUD_TYPES:
        complaint.main_category = "financial_fraud"
        complaint.fraud_type = FINANCIAL_FRAUD_TYPES[fraud_type_num]
        db.commit()
        
        # Move to personal info collection
        cs.state = "new_complaint:personal_info:0"
        cs.meta = dumps({"complaint_id": complaint_id, "field_index": 0})
        db.commit()
        
        print(f"[DEBUG] Successfully selected: {FINANCIAL_FRAUD_TYPES[fraud_type_num]}")
        send_message(wa_id, f"✅ Selected: {FINANCIAL_FRAUD_TYPES[fraud_type_num]}\n\nNow, please provide your personal details:\n\n{PERSONAL_INFO_FIELDS[0][1]}:")
    else:
        print(f"[DEBUG] Invalid fraud type selection: '{fraud_type_num}'")
        # Resend the interactive list
        send_financial_fraud_interactive(wa_id)

def handle_social_media_platform(db, wa_id, platform_num):
    """Handle social media platform selection"""
    from .models import Complaint, ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    complaint = db.query(Complaint).filter_by(id=complaint_id).first()
    
    if not complaint:
        send_message(wa_id, "Error: Complaint not found. Please send 'start' to begin again.")
        return
    
    if platform_num in SOCIAL_MEDIA_PLATFORMS:
        complaint.main_category = "social_media_fraud"
        complaint.fraud_type = SOCIAL_MEDIA_PLATFORMS[platform_num]
        db.commit()
        
        # For fraud call/SMS, skip subtype
        if platform_num == "7":
            cs.state = "new_complaint:personal_info:0"
            cs.meta = dumps({"complaint_id": complaint_id, "field_index": 0})
            db.commit()
            send_message(wa_id, f"Selected: {SOCIAL_MEDIA_PLATFORMS[platform_num]}\n\nPlease provide your personal details:\n\n{PERSONAL_INFO_FIELDS[0][1]}:")
        else:
            # Ask for subtype with interactive buttons
            cs.state = "new_complaint:social_subtype"
            cs.meta = dumps({"complaint_id": complaint_id})
            db.commit()
            send_message(wa_id, f"Selected: {SOCIAL_MEDIA_PLATFORMS[platform_num]}")
            send_social_media_subtype_interactive(wa_id)
    else:
        send_message(wa_id, "Invalid selection. Please reply with a number between 1-7:")

def handle_social_media_subtype(db, wa_id, subtype_num):
    """Handle social media fraud subtype selection"""
    from .models import Complaint, ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    complaint = db.query(Complaint).filter_by(id=complaint_id).first()
    
    if not complaint:
        send_message(wa_id, "Error: Complaint not found. Please send 'start' to begin again.")
        return
    
    if subtype_num in SOCIAL_MEDIA_SUB_TYPES:
        complaint.sub_type = SOCIAL_MEDIA_SUB_TYPES[subtype_num]
        db.commit()
        
        # Move to personal info collection
        cs.state = "new_complaint:personal_info:0"
        cs.meta = dumps({"complaint_id": complaint_id, "field_index": 0})
        db.commit()

        send_message(wa_id, f"Selected: {SOCIAL_MEDIA_SUB_TYPES[subtype_num]}\n\nNow, please provide your personal details:\n\n{PERSONAL_INFO_FIELDS[0][1]}:")
    else:
        send_message(wa_id, "Invalid selection. Please reply with a number between 1-4:")

def handle_personal_info_answer(db, wa_id, text):
    """Handle personal information collection"""
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
        send_message(wa_id, "All personal information collected. Moving to document collection...")
        handle_document_collection(db, wa_id)
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
        cs.state = f"new_complaint:personal_info:{field_index}"
        cs.meta = dumps({"complaint_id": complaint_id, "field_index": field_index})
        db.commit()
        next_field_label = PERSONAL_INFO_FIELDS[field_index][1]
        send_message(wa_id, f"{next_field_label}:")
    else:
        # All personal info collected, move to documents
        cs.state = "new_complaint:documents"
        cs.meta = dumps({"complaint_id": complaint_id})
        db.commit()
        handle_document_collection(db, wa_id)

def handle_document_collection(db, wa_id):
    """Handle document collection phase"""
    from .models import Complaint, ConversationState
    from .whatsapp_api import send_interactive_buttons
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    complaint = db.query(Complaint).filter_by(id=complaint_id).first()
    
    if not complaint:
        send_message(wa_id, "Error: Complaint not found. Please send 'start' to begin again.")
        return
    
    # Generate platform-specific instructions
    instruction_text = ""
    if complaint.main_category == "financial_fraud":
        instruction_text = "Please provide the following documents:\n\n" + \
                    "\n".join([f"• {doc}" for doc in FINANCIAL_DOCUMENTS]) + \
                    "\n\nYou can send images/photos."
    elif complaint.main_category == "social_media_fraud":
        platform = complaint.fraud_type
        if platform == "Facebook":
            instruction_text = "First, register your complaint at Meta India Grievance Channel:\nhttps://help.meta.com/requests/1371776380779082/\n\nThen provide:\n• Request Letter\n• Aadhar Card/Any Govt. Issue ID\n• Disputed Screenshots\n• Alleged URL\n• Original ID Screenshot with URL (if Fake/Impersonation)"
        elif platform == "Instagram":
            instruction_text = "First, register your complaint at Meta India Grievance Channel:\nhttps://help.meta.com/requests/1371776380779082/\n\nThen provide:\n• Request Letter\n• Aadhar Card/Any Govt. Issue ID\n• Disputed Screenshots\n• Alleged URL\n• Original ID Screenshot with URL (if Fake/Impersonation)"
        elif platform == "X (Twitter)":
            instruction_text = "First, register your complaint at X India Grievance Channel:\nhttps://help.x.com/en/forms/account-access\n\nThen provide:\n• Request Letter\n• Aadhar Card/Any Govt. Issue ID\n• Disputed Screenshots\n• Alleged URL"
        elif platform == "WhatsApp":
            instruction_text = "First, dial ##002# from your hacked number to remove call forwarding.\n\nThen register at WhatsApp India Grievance Channel:\nhttps://www.whatsapp.com/contact/forms/1534459096974129\n\nProvide:\n• Request Letter\n• Aadhar Card/Any Govt. Issue ID\n• Disputed Screenshots with hacked Number"
        elif platform == "Telegram":
            instruction_text = "First, register your complaint at Telegram India Grievance Channel:\nhttps://telegram.org/support\n\nThen provide:\n• Request Letter\n• Aadhar Card/Any Govt. Issue ID\n• Disputed Screenshots with hacked Number/ID"
        elif platform == "Gmail/YouTube":
            instruction_text = "First, register your complaint at Google:\nhttps://accounts.google.com/v3/signin/recoveryidentifier?flowName=GlifWebSignIn&dsh=S-1358042667%3A1761737339859572\n\nThen provide:\n• Request Letter\n• Aadhar Card/Any Govt. Issue ID\n• Disputed Screenshots"
        elif platform == "Fraud Call/SMS":
            instruction_text = "Visit Sanchar Saathi to report:\nhttps://www.sancharsaathi.gov.in/sfc/Home/sfc-complaint.jsp\n\nOur agent will call or message you shortly to register your complaint."
    
    # Send instructions with interactive buttons
    buttons = [
        {"id": "done", "title": "✅ Done"},
        {"id": "send_more", "title": "📎 Send More"}
    ]
    message_text = instruction_text if instruction_text else "Please send your documents (images/photos)."
    send_interactive_buttons(wa_id, message_text + "\n\nWhat would you like to do?", buttons)
    
    cs.state = "new_complaint:documents:collecting"
    db.commit()

def _normalize_document_path(value: str) -> str:
    if not value:
        return value
    value = value.strip()
    if not value:
        return value
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if value.startswith(MEDIA_PREFIX):
        return value
    if value.startswith("media/"):
        return "/" + value.lstrip("/")
    if value.startswith("./media/"):
        return "/" + value.lstrip("./")
    abs_path = os.path.abspath(value)
    media_root = os.path.join(BASE_DIR, "media")
    if abs_path.startswith(media_root):
        rel = os.path.relpath(abs_path, BASE_DIR).replace("\\", "/")
        return "/" + rel
    return value


def handle_document_upload(db, wa_id, document_url_or_path):
    """Handle document upload (image URL or file path)"""
    from .models import Complaint, ConversationState
    from .whatsapp_api import send_interactive_buttons
    import json
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    complaint = db.query(Complaint).filter_by(id=complaint_id).first()
    
    if not complaint:
        send_message(wa_id, "Error: Complaint not found. Please send 'start' to begin again.")
        return
    
    # Add document to list
    documents = json.loads(complaint.documents or "[]")
    normalized = _normalize_document_path(document_url_or_path)
    documents.append(normalized)
    complaint.documents = json.dumps(documents)
    db.commit()
    
    # Send confirmation with interactive buttons
    buttons = [
        {"id": "done", "title": "✅ Done"},
        {"id": "send_more", "title": "📎 Send More"}
    ]
    send_interactive_buttons(wa_id, "✅ Document received successfully!\n\nWhat would you like to do next?", buttons)

def finalize_complaint(db, wa_id):
    """Finalize and submit the complaint"""
    from .models import Complaint, ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs:
        send_message(wa_id, "Session expired. Please send 'start' to begin again.")
        return
    
    meta = loads(cs.meta)
    complaint_id = meta.get("complaint_id")
    complaint = db.query(Complaint).filter_by(id=complaint_id).first()
    
    if not complaint:
        send_message(wa_id, "Error: Complaint not found. Please send 'start' to begin again.")
        return
    
    # Generate reference number
    reference_number = generate_reference_number(complaint.id)
    complaint.reference_number = reference_number
    complaint.status = "submitted"
    db.commit()
    
    # Generate PDF report
    try:
        from .reports import save_pdf_for_complaint
        save_pdf_for_complaint(complaint)
    except Exception as e:
        print(f"PDF generation error: {e}")

    # Reset conversation state
    cs.state = "idle"
    cs.meta = dumps({})
    db.commit()
    
    # Send confirmation
    send_message(wa_id, f"✅ Complaint submitted successfully!\n\n📋 Reference Number: {reference_number}\n\nOur agent will call or message you shortly to follow up on your complaint.\n\nThank you for using 1930 Cyber Crime Helpline, Odisha.")

def handle_answer(db, wa_id, text, is_image=False, image_url=None):
    """Main handler for complaint flow answers"""
    from .models import ConversationState
    
    cs = db.query(ConversationState).filter_by(wa_id=wa_id).first()
    if not cs or not cs.state.startswith("new_complaint"):
        send_message(wa_id, "No active complaint. Send 'start' to open the menu.")
        return
    
    state = cs.state
    
    # Handle document uploads
    if state == "new_complaint:documents:collecting":
        if text.lower().strip() == "done":
            finalize_complaint(db, wa_id)
        elif is_image and image_url:
            handle_document_upload(db, wa_id, image_url)
        else:
            send_message(wa_id, "Please send images/photos or type 'done' to finish:")
        return
    
    # Handle personal info collection
    if state.startswith("new_complaint:personal_info:"):
        handle_personal_info_answer(db, wa_id, text)
        return
    
    # Handle category selection (already handled in message_router, but keep for fallback)
    if state == "new_complaint:choose_category":
        if text.strip() == "1":
            cs.state = "new_complaint:financial_type"
            cs.meta = dumps({"complaint_id": loads(cs.meta).get("complaint_id")})
            db.commit()
            send_financial_fraud_interactive(wa_id)
        elif text.strip() == "2":
            cs.state = "new_complaint:social_platform"
            cs.meta = dumps({"complaint_id": loads(cs.meta).get("complaint_id")})
            db.commit()
            send_social_media_interactive(wa_id)
        else:
            send_message(wa_id, "Invalid selection. Please reply with 1 or 2:")
        return
    
    # Handle financial fraud type
    if state == "new_complaint:financial_type":
        handle_financial_fraud_type(db, wa_id, text.strip())
        return
    
    # Handle social media platform
    if state == "new_complaint:social_platform":
        handle_social_media_platform(db, wa_id, text.strip())
        return
    
    # Handle social media subtype
    if state == "new_complaint:social_subtype":
        handle_social_media_subtype(db, wa_id, text.strip())
        return
