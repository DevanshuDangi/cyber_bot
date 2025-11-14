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
    complaint: SQLAlchemy object or dict with fields:
      id, wa_id, category, status, data (JSON string), created_at
    returns: bytes of PDF
    """
    data = loads(getattr(complaint, "data", "{}"))
    created = getattr(complaint, "created_at", None)
    created_s = created.isoformat() if created is not None else datetime.utcnow().isoformat()

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    x = 40
    y = h - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "1930 Cybercrime Complaint Summary")
    y -= 28

    c.setFont("Helvetica", 11)
    c.drawString(x, y, f"Complaint ID: {complaint.id}   Status: {complaint.status}")
    y -= 16
    c.drawString(x, y, f"User WA ID: {complaint.wa_id}")
    y -= 16
    c.drawString(x, y, f"Category: {complaint.category}")
    y -= 16
    c.drawString(x, y, f"Created: {created_s}")
    y -= 24

    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "Details:")
    y -= 18
    c.setFont("Helvetica", 11)

    for k, v in data.items():
        line = f"- {k}: {v}"
        # wrap if necessary
        c.drawString(x + 10, y, line[:1000])
        y -= 14
        if y < 80:
            c.showPage()
            y = h - 50

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
