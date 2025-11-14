import json
import re
from datetime import datetime

def dumps(obj):
    try:
        return json.dumps(obj)
    except Exception:
        return '{}'

def loads(s):
    try:
        return json.loads(s or '{}')
    except Exception:
        return {}

def generate_reference_number(complaint_id):
    """Generate a reference number in format: 1930-YYYYMMDD-XXXXX"""
    date_str = datetime.now().strftime("%Y%m%d")
    return f"1930-{date_str}-{str(complaint_id).zfill(5)}"

def validate_phone(phone):
    """Validate Indian phone number (10 digits, optionally with +91)"""
    phone = phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("+91"):
        phone = phone[3:]
    elif phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]
    return len(phone) == 10 and phone.isdigit()

def validate_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def validate_pin_code(pin):
    """Validate Indian PIN code (6 digits)"""
    pin = pin.strip().replace(" ", "")
    return len(pin) == 6 and pin.isdigit()

def validate_date_of_birth(dob):
    """Validate date of birth (DD/MM/YYYY or DD-MM-YYYY)"""
    patterns = [
        r'^\d{2}/\d{2}/\d{4}$',
        r'^\d{2}-\d{2}-\d{4}$',
        r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
    ]
    for pattern in patterns:
        if re.match(pattern, dob.strip()):
            return True
    return False
