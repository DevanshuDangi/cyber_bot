import os
from dotenv import load_dotenv
load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "cyberbot123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")  # from Meta WhatsApp Cloud API
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "")  # from Meta
GRAPH_VERSION = os.getenv("GRAPH_VERSION", "v21.0")
DEBUG_PRINT_REPLY = os.getenv("DEBUG_PRINT_REPLY", "1")  # if 1, prints replies when no token
