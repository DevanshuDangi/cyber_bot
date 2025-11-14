# backend/reports.py
import os, json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from .utils import loads

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def build_pdf_bytes(complaint):
    """
    complaint: SQLAlchemy object with all complaint fields
    returns: bytes of PDF
    """
    data = loads(getattr(complaint, "data", "{}"))
    documents = json.loads(getattr(complaint, "documents", "[]"))
    created = getattr(complaint, "created_at", None)
    updated = getattr(complaint, "updated_at", None)
    created_s = created.strftime("%d/%m/%Y %H:%M:%S") if created else datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    updated_s = updated.strftime("%d/%m/%Y %H:%M:%S") if updated else "N/A"

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    x = 40
    y = h - 50

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x, y, "1930 Cyber Crime Helpline, Odisha")
    y -= 25
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "Complaint Report")
    y -= 30

    # Reference Number and Status
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"Reference Number: {getattr(complaint, 'reference_number', 'N/A')}")
    y -= 18
    c.drawString(x, y, f"Complaint ID: {complaint.id}   Status: {getattr(complaint, 'status', 'N/A').upper()}")
    y -= 18
    c.drawString(x, y, f"Complaint Type: {getattr(complaint, 'complaint_type', 'N/A')}")
    y -= 25

    # Category Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Category Information:")
    y -= 18
    c.setFont("Helvetica", 11)
    main_category = getattr(complaint, 'main_category', '')
    if main_category:
        c.drawString(x + 10, y, f"Main Category: {main_category.replace('_', ' ').title()}")
        y -= 16
    fraud_type = getattr(complaint, 'fraud_type', '')
    if fraud_type:
        c.drawString(x + 10, y, f"Fraud Type: {fraud_type}")
        y -= 16
    sub_type = getattr(complaint, 'sub_type', '')
    if sub_type:
        c.drawString(x + 10, y, f"Sub Type: {sub_type}")
        y -= 16
    y -= 10

    # Personal Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Personal Information:")
    y -= 18
    c.setFont("Helvetica", 11)
    
    personal_fields = [
        ("name", "Name"),
        ("father_spouse_guardian_name", "Father/Spouse/Guardian Name"),
        ("date_of_birth", "Date of Birth"),
        ("phone_number", "Phone Number"),
        ("email_id", "Email ID"),
        ("gender", "Gender"),
    ]
    
    for field_name, field_label in personal_fields:
        value = getattr(complaint, field_name, '')
        if value:
            c.drawString(x + 10, y, f"{field_label}: {value}")
            y -= 16
            if y < 80:
                c.showPage()
                y = h - 50
    
    y -= 10

    # Address Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Address Information:")
    y -= 18
    c.setFont("Helvetica", 11)
    
    address_fields = [
        ("village", "Village"),
        ("post_office", "Post Office"),
        ("police_station", "Police Station"),
        ("district", "District"),
        ("pin_code", "PIN Code"),
    ]
    
    for field_name, field_label in address_fields:
        value = getattr(complaint, field_name, '')
        if value:
            c.drawString(x + 10, y, f"{field_label}: {value}")
            y -= 16
            if y < 80:
                c.showPage()
                y = h - 50
    
    y -= 10

    # Account Information (for account unfreeze)
    account_number = getattr(complaint, 'account_number', '')
    if account_number:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, "Account Information:")
        y -= 18
        c.setFont("Helvetica", 11)
        c.drawString(x + 10, y, f"Account Number: {account_number}")
        y -= 20

    # Additional Data
    if data:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, "Additional Information:")
        y -= 18
        c.setFont("Helvetica", 11)
        for k, v in data.items():
            line = f"{k}: {str(v)[:200]}"
            c.drawString(x + 10, y, line)
            y -= 14
            if y < 80:
                c.showPage()
                y = h - 50

    # Documents
    if documents:
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, y, "Documents:")
        y -= 18
        c.setFont("Helvetica", 11)
        for i, doc in enumerate(documents, 1):
            doc_str = str(doc)[:150]
            c.drawString(x + 10, y, f"{i}. {doc_str}")
            y -= 14
            if y < 80:
                c.showPage()
                y = h - 50

    # Footer
    y -= 20
    c.setFont("Helvetica", 9)
    c.drawString(x, y, f"Created: {created_s}")
    y -= 12
    c.drawString(x, y, f"Updated: {updated_s}")
    y -= 12
    c.drawString(x, y, f"WhatsApp ID: {getattr(complaint, 'wa_id', 'N/A')}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

def save_pdf_for_complaint(complaint):
    pdf_bytes = build_pdf_bytes(complaint)
    path = os.path.join(REPORTS_DIR, f"report_{complaint.id}.pdf")
    with open(path, "wb") as f:
        f.write(pdf_bytes)
    return path
