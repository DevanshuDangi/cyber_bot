#!/usr/bin/env python3
"""
Generate a comprehensive PDF presentation for the 1930 Cyber Crime Helpline WhatsApp Chatbot
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def create_presentation():
    """Create the PDF presentation"""
    filename = "1930_Cyber_Crime_Chatbot_Presentation.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#283593'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3949ab'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#212121'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#212121'),
        spaceAfter=6,
        leftIndent=20,
        bulletIndent=10,
        leading=14
    )
    
    # ========== SLIDE 1: TITLE ==========
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("WhatsApp Chatbot for", title_style))
    story.append(Paragraph("Cyber Crime Helpline (1930)", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Odisha", subheading_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("A Comprehensive Solution for Digital Grievance Management", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, 
                                        alignment=TA_CENTER, textColor=colors.HexColor('#616161'))))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", 
                          ParagraphStyle('Date', parent=styles['Normal'], fontSize=10, 
                                        alignment=TA_CENTER, textColor=colors.HexColor('#757575'))))
    story.append(PageBreak())
    
    # ========== SLIDE 2: PROBLEM STATEMENT ==========
    story.append(Paragraph("Problem Statement", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Background:</b>", subheading_style))
    story.append(Paragraph(
        "The Cyber Crime Helpline 1930 is a critical platform through which citizens report "
        "online financial frauds and cyber-related offenses. However, due to the increasing number "
        "of calls received daily, many complainants are required to wait in long call queues before "
        "their issues can be addressed.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<b>Objective:</b>", subheading_style))
    story.append(Paragraph(
        "Design and develop a WhatsApp Chatbot that can act as an alternative communication channel "
        "to the 1930 Helpline. The chatbot should automatically collect complainant information, "
        "register the complaint/query, and generate a reference number for tracking or follow-up.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<b>Key Challenges:</b>", subheading_style))
    challenges = [
        "Long waiting times in call queues",
        "Limited availability (working hours only)",
        "Manual data collection process",
        "High volume of complaints",
        "Need for 24/7 accessibility"
    ]
    for challenge in challenges:
        story.append(Paragraph(f"• {challenge}", bullet_style))
    
    story.append(PageBreak())
    
    # ========== SLIDE 3: SOLUTION OVERVIEW ==========
    story.append(Paragraph("Solution Overview", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "A comprehensive WhatsApp-based chatbot system that provides an instant, user-friendly, "
        "and accessible channel for submitting cybercrime complaints, thereby improving the efficiency "
        "of grievance registration under the Cyber Crime Helpline framework.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Key Benefits:</b>", subheading_style))
    benefits = [
        "24/7 availability - No waiting queues",
        "Automated data collection - Step-by-step guidance",
        "Instant reference number generation",
        "Multiple complaint types supported",
        "Document/image upload support",
        "Status tracking capability",
        "Admin dashboard for management",
        "Natural Language Understanding (NLU) integration"
    ]
    for benefit in benefits:
        story.append(Paragraph(f"✓ {benefit}", bullet_style))
    
    story.append(PageBreak())
    
    # ========== SLIDE 4: FUNCTIONAL REQUIREMENTS ==========
    story.append(Paragraph("Functional Requirements", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>1. WhatsApp Business API Integration</b>", subheading_style))
    story.append(Paragraph(
        "• Two-way messaging through WhatsApp Business API",
        bullet_style
    ))
    story.append(Paragraph(
        "• Interactive buttons and lists for better user experience",
        bullet_style
    ))
    story.append(Paragraph(
        "• Media handling (images, documents)",
        bullet_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<b>2. Data Collection</b>", subheading_style))
    data_fields = [
        "Name, Father/Spouse/Guardian Name",
        "Date of Birth, Phone Number, Email ID",
        "Gender, Village, Post Office",
        "Police Station, District, PIN Code"
    ]
    for field in data_fields:
        story.append(Paragraph(f"• {field}", bullet_style))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<b>3. Natural Language Understanding (NLU)</b>", subheading_style))
    story.append(Paragraph(
        "• Intent detection for common queries (\"I have been scammed\", \"My money is stuck\")",
        bullet_style
    ))
    story.append(Paragraph(
        "• Auto-routing based on user intent",
        bullet_style
    ))
    story.append(Paragraph(
        "• Intelligent query handling using Google Gemini AI",
        bullet_style
    ))
    
    story.append(PageBreak())
    
    # ========== SLIDE 5: COMPLAINT TYPES ==========
    story.append(Paragraph("Complaint Types & Categories", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>A. New Complaint</b>", subheading_style))
    story.append(Paragraph("<b>A-1. Financial Fraud (23 Types)</b>", 
                          ParagraphStyle('ListHeader', parent=styles['Normal'], fontSize=12, 
                                        fontName='Helvetica-Bold')))
    
    financial_types = [
        "Investment/Trading/IPO Fraud", "Customer Care Fraud", "UPI Fraud",
        "APK Fraud", "Fake Franchisee/Dealership Fraud", "Online Job Fraud",
        "Debit Card Fraud", "Credit Card Fraud", "E-Commerce Fraud",
        "Loan App Fraud", "Sextortion Fraud", "OLX Fraud",
        "Lottery Fraud", "Hotel Booking Fraud", "Gaming App Fraud",
        "AEPS Fraud", "Tower Installation Fraud", "E-Wallet Fraud",
        "Digital Arrest Fraud", "Fake Website Scam Fraud",
        "Ticket Booking Fraud", "Insurance Maturity Fraud", "Others"
    ]
    
    # Split into two columns
    col1 = financial_types[:12]
    col2 = financial_types[12:]
    
    data = [["Financial Fraud Types (1-12)", "Financial Fraud Types (13-23)"]]
    for i in range(max(len(col1), len(col2))):
        row = [
            f"{i+1}. {col1[i]}" if i < len(col1) else "",
            f"{i+13}. {col2[i]}" if i < len(col2) else ""
        ]
        data.append(row)
    
    table = Table(data, colWidths=[3.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table)
    
    story.append(PageBreak())
    
    # ========== SLIDE 6: SOCIAL MEDIA FRAUD ==========
    story.append(Paragraph("Social Media Fraud Support", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>A-2. Social Media Fraud Platforms:</b>", subheading_style))
    
    platforms = [
        ("Facebook", "Meta India Grievance Channel", "Impersonation/Fake Account/Hack/Obscene Content"),
        ("Instagram", "Meta India Grievance Channel", "Impersonation/Fake Account/Hack/Obscene Content"),
        ("X (Twitter)", "X India Grievance Channel", "Impersonation/Fake Account/Hack/Obscene Content"),
        ("WhatsApp", "WhatsApp India Grievance Channel", "Impersonation/Fake Account/Hack (with call forwarding removal)"),
        ("Telegram", "Telegram India Grievance Channel", "Impersonation/Fake Account/Hack/Obscene Content"),
        ("Gmail/YouTube", "Google Recovery", "Impersonation/Hack/Obscene Content"),
        ("Fraud Call/SMS", "Sanchar Saathi", "Fraud call and SMS reporting")
    ]
    
    for platform, channel, types in platforms:
        story.append(Paragraph(f"<b>{platform}:</b> {types}", 
                              ParagraphStyle('Platform', parent=styles['Normal'], fontSize=10, 
                                            leftIndent=20, spaceAfter=4)))
        story.append(Paragraph(f"   Channel: {channel}", 
                              ParagraphStyle('Channel', parent=styles['Normal'], fontSize=9, 
                                            leftIndent=30, textColor=colors.HexColor('#616161'), 
                                            spaceAfter=6)))
    
    story.append(PageBreak())
    
    # ========== SLIDE 7: WORKFLOW ==========
    story.append(Paragraph("System Workflow", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Main Menu Options:</b>", subheading_style))
    
    workflow_data = [
        ["Option", "Function", "Details"],
        ["A", "New Complaint", "Financial Fraud (23 types) or Social Media Fraud (7 platforms)"],
        ["B", "Status Check", "Check existing complaint using Acknowledgement Number or Mobile Number"],
        ["C", "Account Unfreeze", "Request account unfreezing with account number"],
        ["D", "Other Queries", "General queries handled by NLU/Gemini AI"]
    ]
    
    workflow_table = Table(workflow_data, colWidths=[0.8*inch, 1.5*inch, 4.7*inch])
    workflow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(workflow_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>New Complaint Flow:</b>", subheading_style))
    flow_steps = [
        "User selects complaint type (Financial/Social Media)",
        "Selects specific fraud type or platform",
        "Provides personal information (11 fields)",
        "Provides address information (5 fields)",
        "Uploads supporting documents/images",
        "Receives unique Reference Number"
    ]
    for i, step in enumerate(flow_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))
    
    story.append(PageBreak())
    
    # ========== SLIDE 8: TECHNICAL ARCHITECTURE ==========
    story.append(Paragraph("Technical Architecture", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Technology Stack:</b>", subheading_style))
    
    tech_data = [
        ["Component", "Technology", "Purpose"],
        ["Backend Framework", "FastAPI (Python)", "RESTful API, Webhook handling"],
        ["Database", "SQLite", "Data storage (lightweight, no setup)"],
        ["ORM", "SQLAlchemy", "Database abstraction"],
        ["PDF Generation", "ReportLab", "Complaint reports"],
        ["WhatsApp API", "Meta WhatsApp Business API", "Two-way messaging"],
        ["NLU/AI", "Google Gemini API", "Intent detection, query handling"],
        ["Frontend (Admin)", "React + TypeScript", "Admin dashboard"],
        ["Server", "Uvicorn", "ASGI server"],
        ["Testing", "ngrok", "Webhook testing"]
    ]
    
    tech_table = Table(tech_data, colWidths=[1.8*inch, 2*inch, 3.2*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(tech_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>System Architecture:</b>", subheading_style))
    story.append(Paragraph(
        "WhatsApp Business API → Webhook Endpoint → FastAPI Backend → SQLite Database → "
        "Response Generation → WhatsApp API → User",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ========== SLIDE 9: KEY FEATURES ==========
    story.append(Paragraph("Key Features & Innovations", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    features = [
        ("Interactive UI", "WhatsApp interactive buttons and lists for seamless navigation"),
        ("NLU Integration", "Google Gemini AI for intent detection and natural query handling"),
        ("Auto-routing", "Intelligent routing based on user messages (e.g., \"I have been scammed\")"),
        ("Data Validation", "Real-time validation for phone numbers, emails, PIN codes, dates"),
        ("Document Upload", "Support for images, screenshots, PDFs with secure storage"),
        ("Reference Generation", "Unique ticket numbers (1930-OD-YYYYMMDD-XXXXX) for tracking"),
        ("PDF Reports", "Automated PDF generation with embedded images for each complaint"),
        ("Admin Dashboard", "React-based admin console with stats, filters, and exports"),
        ("Status Tracking", "Check complaint status using reference number or mobile number"),
        ("Platform Guidance", "Platform-specific links and instructions for social media frauds")
    ]
    
    for feature, description in features:
        story.append(Paragraph(f"<b>• {feature}:</b> {description}", bullet_style))
    
    story.append(PageBreak())
    
    # ========== SLIDE 10: DATA VALIDATION ==========
    story.append(Paragraph("Data Validation & Security", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Validation Rules:</b>", subheading_style))
    validation_rules = [
        "Phone Number: 10-digit Indian mobile number format",
        "Email ID: Standard email format validation",
        "PIN Code: 6-digit Indian postal code",
        "Date of Birth: DD/MM/YYYY format validation",
        "Account Number: Alphanumeric validation"
    ]
    for rule in validation_rules:
        story.append(Paragraph(f"✓ {rule}", bullet_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Security Measures:</b>", subheading_style))
    security_measures = [
        "SQL injection protection (SQLAlchemy ORM)",
        "Input sanitization and validation",
        "Secure webhook verification",
        "Local data storage (no third-party sharing)",
        "Encrypted API communications",
        "Access control for admin dashboard"
    ]
    for measure in security_measures:
        story.append(Paragraph(f"✓ {measure}", bullet_style))
    
    story.append(PageBreak())
    
    # ========== SLIDE 11: DELIVERABLES ==========
    story.append(Paragraph("Deliverables", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    deliverables = [
        ("Working Prototype", 
         "Fully functional WhatsApp chatbot integrated with WhatsApp Business API, "
         "test database, and complete workflow implementation"),
        
        ("Admin Dashboard", 
         "React/TypeScript-based admin console with:\n"
         "• View all complaints with filters\n"
         "• Statistics and analytics\n"
         "• Export to CSV/JSON\n"
         "• PDF report generation\n"
         "• Image/document preview\n"
         "• Search and filter capabilities"),
        
        ("Documentation", 
         "Comprehensive documentation including:\n"
         "• System architecture diagrams\n"
         "• Data flow documentation\n"
         "• API specifications\n"
         "• Security measures\n"
         "• Deployment guide\n"
         "• User manual\n"
         "• Admin guide"),
        
        ("Database Schema", 
         "Structured database with:\n"
         "• User management\n"
         "• Complaint records\n"
         "• Conversation state tracking\n"
         "• Document storage references"),
        
        ("PDF Report Generation", 
         "Automated PDF reports for each complaint with:\n"
         "• All collected information\n"
         "• Embedded images/documents\n"
         "• Reference number\n"
         "• Timestamp and status")
    ]
    
    for title, description in deliverables:
        story.append(Paragraph(f"<b>{title}:</b>", subheading_style))
        story.append(Paragraph(description, body_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # ========== SLIDE 12: EVALUATION PARAMETERS ==========
    story.append(Paragraph("Evaluation Parameters", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    eval_params = [
        ("User Experience", 
         "• Simple and intuitive interface\n"
         "• Step-by-step guidance\n"
         "• Interactive buttons for easy navigation\n"
         "• Clear prompts and error messages\n"
         "• Fast response times"),
        
        ("System Security & Data Protection", 
         "• Input validation and sanitization\n"
         "• SQL injection protection\n"
         "• Secure API communications\n"
         "• Local data storage\n"
         "• Access control mechanisms"),
        
        ("Scalability and Performance", 
         "• Stateless backend design\n"
         "• Efficient database queries\n"
         "• Fast response generation\n"
         "• Support for concurrent users\n"
         "• Optimized media handling"),
        
        ("Innovation in Design", 
         "• NLU integration for intelligent routing\n"
         "• Auto-detection of complaint intent\n"
         "• Interactive WhatsApp components\n"
         "• Automated PDF generation with images\n"
         "• Real-time admin dashboard\n"
         "• Platform-specific guidance")
    ]
    
    for title, details in eval_params:
        story.append(Paragraph(f"<b>{title}:</b>", subheading_style))
        story.append(Paragraph(details, body_style))
        story.append(Spacer(1, 0.15*inch))
    
    story.append(PageBreak())
    
    # ========== SLIDE 13: IMPACT ==========
    story.append(Paragraph("Impact & Benefits", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "This solution significantly enhances citizen convenience by offering an instant, "
        "user-friendly, and accessible channel for submitting cybercrime complaints, thereby "
        "improving the efficiency of grievance registration under the Cyber Crime Helpline framework.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Key Impacts:</b>", subheading_style))
    
    impacts = [
        "Reduced waiting times - No call queues, instant access",
        "24/7 availability - Citizens can file complaints anytime",
        "Improved efficiency - Automated data collection",
        "Better tracking - Unique reference numbers for all complaints",
        "Enhanced user experience - Interactive, guided process",
        "Comprehensive coverage - 23 financial fraud types + 7 social media platforms",
        "Document support - Easy evidence submission",
        "Admin efficiency - Centralized dashboard for complaint management"
    ]
    
    for impact in impacts:
        story.append(Paragraph(f"✓ {impact}", bullet_style))
    
    story.append(PageBreak())
    
    # ========== SLIDE 14: IMPLEMENTATION STATUS ==========
    story.append(Paragraph("Implementation Status", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>✅ Completed Features:</b>", subheading_style))
    
    completed = [
        "Complete workflow implementation (A, B, C, D)",
        "All 23 financial fraud types",
        "All 7 social media platforms with platform-specific guidance",
        "Complete data collection (11 personal + 5 address fields)",
        "Data validation (phone, email, PIN, DOB)",
        "Document/image upload and storage",
        "Reference number generation",
        "PDF report generation with embedded images",
        "Admin dashboard (React/TypeScript)",
        "Status check functionality",
        "Account unfreeze flow",
        "NLU integration with Google Gemini",
        "Intent detection and auto-routing",
        "Interactive buttons and lists",
        "CSV/JSON export functionality"
    ]
    
    for item in completed:
        story.append(Paragraph(f"✓ {item}", bullet_style))
    
    story.append(PageBreak())
    
    # ========== SLIDE 15: CONCLUSION ==========
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Conclusion", heading_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph(
        "The WhatsApp Chatbot for Cyber Crime Helpline (1930) provides a comprehensive, "
        "user-friendly, and efficient solution for digital grievance management. With its "
        "advanced features including NLU integration, interactive UI, and automated workflows, "
        "it significantly improves the accessibility and efficiency of the cybercrime reporting process.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "The system is ready for deployment and can handle high volumes of complaints while "
        "maintaining data security and providing an excellent user experience.",
        body_style
    ))
    
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Thank You", 
                          ParagraphStyle('ThankYou', parent=styles['Heading1'], fontSize=24, 
                                        alignment=TA_CENTER, textColor=colors.HexColor('#283593'),
                                        spaceBefore=20)))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Presentation generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_presentation()

