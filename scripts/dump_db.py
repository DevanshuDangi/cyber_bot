"""
Utility script to dump the current SQLite/Postgres data to stdout.

Usage:
    python scripts/dump_db.py
"""
from pprint import pprint

from sqlalchemy import text

from backend.db import SessionLocal
from backend.models import Complaint, ConversationState, User


def _safe_iso(value):
    if not value:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    # fall back to raw string representation
    return str(value)


def serialize_complaint(complaint):
    return {
        "id": complaint.id,
        "reference_number": complaint.reference_number,
        "wa_id": complaint.wa_id,
        "status": complaint.status,
        "complaint_type": complaint.complaint_type,
        "main_category": complaint.main_category,
        "fraud_type": complaint.fraud_type,
        "sub_type": complaint.sub_type,
        "name": complaint.name,
        "phone_number": complaint.phone_number,
        "district": complaint.district,
        "documents": complaint.documents,
        "created_at": complaint.created_at.isoformat() if complaint.created_at else None,
        "updated_at": _safe_iso(complaint.updated_at),
    }


def serialize_state(state):
    return {
        "wa_id": state.wa_id,
        "state": state.state,
        "meta": state.meta,
        "updated_at": _safe_iso(state.updated_at),
    }


def serialize_user(user):
    return {"id": user.id, "wa_id": user.wa_id, "language": user.language}


def sanitize_db(session):
    session.execute(text("UPDATE complaints SET created_at=NULL WHERE created_at=''"))
    session.execute(text("UPDATE complaints SET updated_at=NULL WHERE updated_at=''"))
    session.execute(text("UPDATE conversation_states SET updated_at=NULL WHERE updated_at=''"))
    session.commit()


def main():
    session = SessionLocal()
    sanitize_db(session)

    print("\n=== Complaints ===")
    complaints = session.query(Complaint).order_by(Complaint.id).all()
    if not complaints:
        print("(none)")
    else:
        for complaint in complaints:
            pprint(serialize_complaint(complaint), sort_dicts=False)
            print("-" * 60)

    print("\n=== Conversation States ===")
    states = session.query(ConversationState).order_by(ConversationState.id).all()
    if not states:
        print("(none)")
    else:
        for state in states:
            pprint(serialize_state(state), sort_dicts=False)
            print("-" * 60)

    print("\n=== Users ===")
    users = session.query(User).order_by(User.id).all()
    if not users:
        print("(none)")
    else:
        for user in users:
            pprint(serialize_user(user), sort_dicts=False)

    session.close()


if __name__ == "__main__":
    main()

