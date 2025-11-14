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
    status = Column(String, default="draft")  # draft | submitted | resolved
    category = Column(String, default="")
    data = Column(Text, default="{}")  # JSON string of answers
    created_at = Column(DateTime, default=datetime.utcnow)

class ConversationState(Base):
    __tablename__ = "conversation_states"
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True)
    state = Column(String, default="idle")  # idle | menu | new_complaint:stepX | status_check
    meta = Column(Text, default="{}")  # small JSON to store temporary answers
    updated_at = Column(DateTime, default=datetime.utcnow)
