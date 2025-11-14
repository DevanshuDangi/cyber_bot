import os, json
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import PlainTextResponse, JSONResponse
from .config import VERIFY_TOKEN
from .db import SessionLocal, engine
from .models import User, Complaint, ConversationState, Base
from .message_router import route_message

Base.metadata.create_all(bind=engine)

app = FastAPI(title="1930 WhatsApp Chatbot (modular)")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"ok": True}

# inside backend/main.py (or wherever your FastAPI app is)
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from .config import VERIFY_TOKEN

app = FastAPI()

@app.get("/webhook")
async def verify_webhook(request: Request):
    # Meta sends hub.mode, hub.challenge, hub.verify_token
    # but some tools may send plain mode/challenge/verify_token -> support both
    qp = request.query_params
    mode = qp.get("hub.mode") or qp.get("mode")
    challenge = qp.get("hub.challenge") or qp.get("challenge")
    token = qp.get("hub.verify_token") or qp.get("verify_token") or qp.get("token")

    # debug logging (helpful while developing)
    print("[WEBHOOK-VERIFY] mode:", mode, "token:", token, "expected:", VERIFY_TOKEN, "challenge:", challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        # return the challenge string as plain text (Meta requires this)
        return PlainTextResponse(challenge or "")
    # If not matched:
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def incoming(request: Request, db=Depends(get_db)):
    payload = await request.json()
    # minimal parsing per WhatsApp Cloud API structure
    try:
        for entry in payload.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value', {})
                for msg in value.get('messages', []) or []:
                    wa_id = msg.get('from')
                    text = None
                    if msg.get('type') == 'text':
                        text = msg['text'].get('body')
                    elif msg.get('type') == 'interactive':
                        # handle quick reply or button reply
                        interactive = msg.get('interactive', {})
                        if 'button_reply' in interactive:
                            text = interactive['button_reply'].get('title') or interactive['button_reply'].get('id')
                        elif 'list_reply' in interactive:
                            text = interactive['list_reply'].get('title') or interactive['list_reply'].get('id')
                    if not wa_id or text is None:
                        continue
                    # ensure user exists
                    user = db.query(User).filter_by(wa_id=wa_id).first()
                    if not user:
                        user = User(wa_id=wa_id); db.add(user); db.commit(); db.refresh(user)
                    # route message
                    route_message(db, wa_id, text)
        return JSONResponse({"ok": True})
    except Exception as e:
        print('Error processing incoming webhook:', e)
        return JSONResponse({"ok": False, "error": str(e)})

# demo endpoint for dashboard
from fastapi.encoders import jsonable_encoder
@app.get("/_demo/reports")
def list_reports(db=Depends(get_db)):
    out = []
    for r in db.query(Complaint).order_by(Complaint.created_at.desc()).limit(200):
        out.append({
            "id": r.id,
            "category": r.category,
            "status": r.status,
            "created_at": r.created_at.isoformat() + "Z",
            "user": {"wa_id": r.wa_id},
            "data": r.data
        })
    return JSONResponse(jsonable_encoder(out))



from fastapi.responses import FileResponse
import os

@app.get("/reports/{report_id}.pdf")
def get_report_pdf(report_id: int):
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    path = os.path.join(reports_dir, f"report_{report_id}.pdf")
    if not os.path.exists(path):
        # optional: generate on-the-fly if the complaint exists but file missing
        db = next(get_db())
        comp = db.query(Complaint).filter_by(id=report_id).first()
        if comp:
            try:
                from .reports import save_pdf_for_complaint
                save_pdf_for_complaint(comp)
            except Exception as e:
                print("PDF on-demand error:", e)
        db.close()
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path, media_type="application/pdf", filename=f"report_{report_id}.pdf")
