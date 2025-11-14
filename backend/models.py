from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True, unique=True)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True)
    reference_number = Column(String, index=True, unique=True)  # Generated reference number
    status = Column(String, default="draft")  # draft | submitted | in_progress | resolved
    complaint_type = Column(String, default="")  # A, B, C, D
    main_category = Column(String, default="")  # financial_fraud, social_media_fraud, etc.
    fraud_type = Column(String, default="")  # Specific fraud type (1-23 for financial, platform name for social)
    sub_type = Column(String, default="")  # For social media: impersonation, fake, hack, etc.
    
    # Personal Information
    name = Column(String, default="")
    father_spouse_guardian_name = Column(String, default="")
    date_of_birth = Column(String, default="")
    phone_number = Column(String, default="")
    email_id = Column(String, default="")
    gender = Column(String, default="")
    
    # Address Information
    village = Column(String, default="")
    post_office = Column(String, default="")
    police_station = Column(String, default="")
    district = Column(String, default="")
    pin_code = Column(String, default="")
    
    # Additional data and documents
    data = Column(Text, default="{}")  # JSON string for additional answers
    documents = Column(Text, default="[]")  # JSON array of document file paths/URLs
    account_number = Column(String, default="")  # For account unfreeze (type C)
    acknowledgement_number = Column(String, default="")  # For status check (type B)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConversationState(Base):
    __tablename__ = "conversation_states"
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True)
    state = Column(String, default="idle")  # idle | menu | new_complaint:stepX | status_check | account_unfreeze
    meta = Column(Text, default="{}")  # small JSON to store temporary answers
    updated_at = Column(DateTime, default=datetime.utcnow)
