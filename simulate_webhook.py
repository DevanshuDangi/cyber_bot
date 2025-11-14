# simulate_webhook.py - sends messages to local /webhook to emulate WhatsApp Cloud API
import requests, json, time

API = "http://localhost:8000/webhook"

def payload(wa_id, text):
    return {
      "entry":[{
        "changes":[{
          "value":{
            "messages":[{
              "from": wa_id,
              "id": "wamid.sim",                  "timestamp": "0",
              "type":"text",
              "text":{"body": text}
            }]
          }
        }]
      }]
    }

def send(wa_id, text):
    r = requests.post(API, json=payload(wa_id, text))
    print(r.status_code, r.text)

if __name__ == "__main__":
    # demo conversation from phone +91 99990 00000
    WA = "919835858883"
    send(WA, "start")   # show menu
    time.sleep(0.8)
    send(WA, "1")       # New Complaint
    time.sleep(0.8)
    send(WA, "1")       # Category: Financial
    time.sleep(0.8)
    send(WA, "5000")    # amount
    time.sleep(0.8)
    send(WA, "2025-11-11 18:12") # date/time
    time.sleep(0.8)
    send(WA, "GPay")    # bank/app
    time.sleep(0.8)
    send(WA, "upi@fraud") # recipient
    print('Done')