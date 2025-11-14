import os, json
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import VERIFY_TOKEN
from .db import SessionLocal, engine
from .models import User, Complaint, ConversationState, Base
from .message_router import route_message
from .migrations import ensure_schema

Base.metadata.create_all(bind=engine)
ensure_schema(engine)

app = FastAPI(title="1930 WhatsApp Chatbot (modular)")

# Add CORS middleware to allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media")
if os.path.isdir(MEDIA_DIR):
    app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"ok": True}

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
                    is_image = False
                    image_url = None
                    media_id = None
                    
                    msg_type = msg.get('type')
                    
                    if msg_type == 'text':
                        text = msg['text'].get('body')
                    elif msg_type == 'image':
                        is_image = True
                        image_data = msg.get('image', {})
                        media_id = image_data.get('id')
                        # Get media URL from WhatsApp API
                        if media_id:
                            from .whatsapp_api import download_media
                            from .config import WHATSAPP_TOKEN, GRAPH_VERSION
                            if WHATSAPP_TOKEN:
                                # Get media URL
                                media_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{media_id}"
                                headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
                                try:
                                    import requests
                                    r = requests.get(media_url, headers=headers, timeout=10)
                                    if r.status_code == 200:
                                        media_info = r.json()
                                        image_url = download_media(media_id, media_info.get('url'))
                                except Exception as e:
                                    print(f"Error fetching media URL: {e}")
                                    image_url = f"media_{media_id}"
                            else:
                                image_url = f"media_{media_id}"
                        # Check for caption
                        caption = image_data.get('caption', '')
                        if caption:
                            text = caption
                    elif msg_type == 'interactive':
                        # handle quick reply or button reply
                        interactive = msg.get('interactive', {})
                        if 'button_reply' in interactive:
                            # Prefer ID over title for better matching
                            button_reply = interactive['button_reply']
                            text = button_reply.get('id') or button_reply.get('title')
                        elif 'list_reply' in interactive:
                            # Prefer ID over title for better matching
                            list_reply = interactive['list_reply']
                            text = list_reply.get('id') or list_reply.get('title')
                    
                    if not wa_id:
                        continue
                    
                    # ensure user exists
                    user = db.query(User).filter_by(wa_id=wa_id).first()
                    if not user:
                        user = User(wa_id=wa_id); db.add(user); db.commit(); db.refresh(user)
                    
                    # route message (handle both text and images)
                    if is_image:
                        route_message(db, wa_id, text or "Image received", is_image=True, image_url=image_url)
                    elif text:
                        route_message(db, wa_id, text)
        return JSONResponse({"ok": True})
    except Exception as e:
        print('Error processing incoming webhook:', e)
        import traceback
        traceback.print_exc()
        return JSONResponse({"ok": False, "error": str(e)})

# demo endpoint for dashboard
from fastapi.encoders import jsonable_encoder
@app.get("/_demo/reports")
def list_reports(db=Depends(get_db)):
    out = []
    for r in db.query(Complaint).order_by(Complaint.created_at.desc()).limit(200):
        out.append({
            "id": r.id,
            "reference_number": r.reference_number,
            "complaint_type": r.complaint_type,
            "main_category": r.main_category,
            "fraud_type": r.fraud_type,
            "sub_type": r.sub_type,
            "status": r.status,
            "name": r.name,
            "phone_number": r.phone_number,
            "email_id": r.email_id,
            "district": r.district,
            "created_at": r.created_at.isoformat() + "Z",
            "updated_at": r.updated_at.isoformat() + "Z" if r.updated_at else None,
            "user": {"wa_id": r.wa_id},
            "data": r.data,
            "documents": r.documents
        })
    return JSONResponse(jsonable_encoder(out))



from fastapi.responses import FileResponse

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
