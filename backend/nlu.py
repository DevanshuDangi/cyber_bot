"""
Natural Language Understanding (NLU) module using Google Gemini API
Handles intent detection and query understanding for the 1930 Cyber Crime Helpline chatbot
"""
import os
import json
from typing import Dict, Optional, Tuple
from .config import GEMINI_API_KEY

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[WARNING] google-generativeai not installed. Install with: pip install google-generativeai")

# Initialize Gemini if available
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Use gemini-1.5-flash for fast responses
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("[INFO] Gemini API initialized successfully")
    except Exception as e:
        print(f"[ERROR] Failed to initialize Gemini API: {e}")
        model = None
else:
    model = None

# Intent categories
INTENTS = {
    "new_complaint_financial": [
        "scammed", "fraud", "money stuck", "lost money", "cheated", "fraudulent transaction", 
        "upi fraud", "payment fraud", "stuck", "money", "payment", "transaction", "upi", 
        "debit card", "credit card", "bank", "transfer", "scam", "fraudulent"
    ],
    "new_complaint_social": [
        "account hacked", "fake account", "impersonation", "social media", "facebook", 
        "instagram", "whatsapp hacked", "hacked", "fake", "impersonat", "twitter", "x.com",
        "telegram", "gmail", "youtube", "account"
    ],
    "status_check": [
        "status", "complaint status", "reference number", "acknowledgement", "check my complaint",
        "check status", "where is", "what is the status", "track"
    ],
    "account_unfreeze": [
        "account frozen", "account blocked", "unfreeze", "account locked", "bank account",
        "frozen", "blocked", "locked", "unblock", "unlock"
    ],
    "other_query": [
        "help", "information", "guidance", "how to", "what to do", "advice", "question",
        "query", "tell me", "explain", "guide"
    ]
}

def detect_intent(user_message: str) -> Tuple[str, float]:
    """
    Detect user intent from message using Gemini API
    
    Returns:
        Tuple of (intent, confidence) where intent is one of:
        - "new_complaint_financial"
        - "new_complaint_social"
        - "status_check"
        - "account_unfreeze"
        - "other_query"
        - "unknown"
    """
    if not model:
        # Fallback to keyword matching
        return _keyword_intent_detection(user_message)
    
    user_message_lower = user_message.lower().strip()
    
    # Create prompt for intent detection
    prompt = f"""You are an AI assistant for the 1930 Cyber Crime Helpline, Odisha. 
Analyze the user's message and determine their intent.

User message: "{user_message}"

Possible intents:
1. new_complaint_financial - User wants to file a complaint about financial fraud (money lost, scammed, UPI fraud, payment issues)
2. new_complaint_social - User wants to file a complaint about social media fraud (hacked account, fake account, impersonation)
3. status_check - User wants to check status of existing complaint
4. account_unfreeze - User wants to unfreeze/unblock their bank account
5. other_query - User has a general question or needs guidance

Respond ONLY with a JSON object in this exact format:
{{
    "intent": "intent_name",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}
"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response (might have markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response_text)
        intent = result.get("intent", "unknown")
        confidence = float(result.get("confidence", 0.0))
        
        print(f"[NLU] Intent detected: {intent} (confidence: {confidence:.2f})")
        return intent, confidence
        
    except Exception as e:
        print(f"[NLU ERROR] Failed to detect intent: {e}")
        return _keyword_intent_detection(user_message)

def _keyword_intent_detection(user_message: str) -> Tuple[str, float]:
    """Fallback keyword-based intent detection"""
    user_message_lower = user_message.lower()
    
    # Check each intent category
    best_intent = "unknown"
    best_confidence = 0.0
    
    for intent, keywords in INTENTS.items():
        matches = sum(1 for keyword in keywords if keyword in user_message_lower)
        if matches > 0:
            # Calculate confidence based on number of matches and message length
            confidence = min(0.8, 0.3 + (matches * 0.15))
            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent
    
    return best_intent, best_confidence

def handle_other_query(user_message: str) -> str:
    """
    Handle other queries using Gemini API
    Provides helpful responses for general questions about cybercrime, helpline, etc.
    """
    if not model:
        return _fallback_other_query_response()
    
    prompt = f"""You are a helpful assistant for the 1930 Cyber Crime Helpline, Odisha. 
The user has asked: "{user_message}"

Provide a helpful, concise response (max 300 words) that:
1. Answers their question if it's about cybercrime, fraud, or the helpline
2. Guides them to the appropriate option (A for new complaint, B for status check, etc.)
3. Provides relevant information about reporting cybercrime
4. Is friendly and professional
5. If the query is not related to cybercrime, politely redirect them

Keep the response conversational and suitable for WhatsApp messaging.
"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response (remove markdown if present)
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
            if response_text.startswith("markdown"):
                response_text = response_text[8:].strip()
        
        print(f"[NLU] Generated response for other query")
        return response_text
        
    except Exception as e:
        print(f"[NLU ERROR] Failed to generate response: {e}")
        return _fallback_other_query_response()

def handle_unclear_input(user_message: str, context: Optional[str] = None) -> str:
    """
    Handle unclear or unexpected user input using Gemini
    Provides helpful guidance when the system doesn't understand the input
    """
    if not model:
        return _fallback_unclear_response()
    
    context_text = f"Context: {context}\n\n" if context else ""
    
    prompt = f"""You are a helpful assistant for the 1930 Cyber Crime Helpline, Odisha.
{context_text}The user sent: "{user_message}"

The system didn't understand this input. Provide a helpful response that:
1. Acknowledges the confusion
2. Suggests what the user might want to do
3. Reminds them of the available options (A, B, C, D)
4. Is friendly and helpful

Keep it concise (max 200 words) and suitable for WhatsApp.
"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        print(f"[NLU] Generated response for unclear input")
        return response_text
        
    except Exception as e:
        print(f"[NLU ERROR] Failed to generate response: {e}")
        return _fallback_unclear_response()

def _fallback_other_query_response() -> str:
    """Fallback response for other queries when Gemini is unavailable"""
    return """Thank you for contacting 1930 Cyber Crime Helpline, Odisha.

For general queries and guidance:
• Send 'A' to file a new complaint
• Send 'B' to check complaint status
• Send 'C' for account unfreeze requests
• Send 'start' to see the main menu

For urgent matters, please call the helpline directly at 1930.

How can I help you today?"""

def _fallback_unclear_response() -> str:
    """Fallback response for unclear input when Gemini is unavailable"""
    return """I didn't quite understand that. 

Please choose from the following options:
• A - New Complaint
• B - Status Check
• C - Account Unfreeze
• D - Other Queries

Or send 'start' to see the main menu."""

def should_route_to_complaint(user_message: str) -> Tuple[bool, Optional[str]]:
    """
    Determine if user message indicates they want to file a complaint
    Returns: (should_route, complaint_type) where complaint_type is "financial" or "social"
    """
    intent, confidence = detect_intent(user_message)
    
    if intent == "new_complaint_financial" and confidence > 0.5:
        return True, "financial"
    elif intent == "new_complaint_social" and confidence > 0.5:
        return True, "social"
    
    return False, None

