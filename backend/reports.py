# backend/reports.py
import os
import json
from io import BytesIO
from datetime import datetime

import requests  # type: ignore
from reportlab.lib.pagesizes import A4  # type: ignore
from reportlab.pdfgen import canvas  # type: ignore
from reportlab.lib.utils import ImageReader  # type: ignore

from .utils import loads

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
MEDIA_PREFIX = "/media/"


def _resolve_document_path(doc: str):
    if not doc:
        return None
    doc = str(doc).strip().replace("file://", "")
    if not doc:
        return None
    if doc.startswith("http://") or doc.startswith("https://"):
        return doc
    normalized = doc.lstrip("/")
    candidate_paths = []
    if os.path.isabs(doc):
        candidate_paths.append(doc)
    candidate_paths.append(os.path.join(BASE_DIR, normalized))
    candidate_paths.append(os.path.join(MEDIA_DIR, normalized.split("media/", 1)[-1]))
    candidate_paths.append(os.path.join(BASE_DIR, "reports", normalized))
    if doc.startswith(MEDIA_PREFIX):
        candidate_paths.append(os.path.join(BASE_DIR, normalized))
    if doc.startswith("media/"):
        candidate_paths.append(os.path.join(BASE_DIR, normalized))
    if doc.startswith("media_") and "." in doc:
        candidate_paths.append(os.path.join(MEDIA_DIR, doc))
    for path in candidate_paths:
        if path and os.path.exists(path):
            return path
    return None


def _is_image_file(doc: str) -> bool:
    _, ext = os.path.splitext(str(doc).split("?")[0])
    return ext.lower() in IMAGE_EXTENSIONS


def _draw_image(canvas_obj, source_path_or_url, x, y, max_width):
    """
    Draws an image on the PDF and returns the new Y position.
    """
    if y < 160:
        canvas_obj.showPage()
        y = A4[1] - 60
    try:
        if isinstance(source_path_or_url, str) and source_path_or_url.startswith(("http://", "https://")):
            response = requests.get(source_path_or_url, timeout=10)
            response.raise_for_status()
            img_reader = ImageReader(BytesIO(response.content))
        else:
            img_reader = ImageReader(source_path_or_url)
    except Exception as exc:
        canvas_obj.setFont("Helvetica-Oblique", 9)
        canvas_obj.drawString(x, y, f"[Image unavailable: {exc}]")
        return y - 14

    img_width, img_height = img_reader.getSize()
    scale = min(max_width / img_width, 300 / img_height, 1)
    draw_width = img_width * scale
    draw_height = img_height * scale

    if y - draw_height < 60:
        canvas_obj.showPage()
        y = A4[1] - 60

    canvas_obj.drawImage(
        img_reader,
        x,
        y - draw_height,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        mask="auto",
    )
    return y - draw_height - 15

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
        c.drawString(x, y, "Documents & Evidence:")
        y -= 18
        c.setFont("Helvetica", 11)
        for i, doc in enumerate(documents, 1):
            doc_str = str(doc)
            display_str = doc_str[:150]
            c.drawString(x + 10, y, f"{i}. {display_str}")
            y -= 14
            if _is_image_file(doc_str):
                resolved = _resolve_document_path(doc_str)
                if resolved:
                    y = _draw_image(c, resolved, x + 20, y, max_width=(w - 2 * (x + 20)))
                else:
                    c.setFont("Helvetica-Oblique", 9)
                    c.drawString(x + 20, y, "[Image file missing]")
                    y -= 14
                    c.setFont("Helvetica", 11)
            if y < 80:
                c.showPage()
                y = h - 50
                c.setFont("Helvetica", 11)

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
