import os
import time
from datetime import datetime
from dotenv import load_dotenv
import pywhatkit

# Load environment logic so we can securely fetch phone number
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

MY_WHATSAPP_NUMBER = os.getenv("MY_WHATSAPP_NUMBER")
LOG_FILE = "./Logs/activity_log.md"

def send_whatsapp_alert(message_body):
    """
    Sends a real WhatsApp alert to Kiran's mobile using pywhatkit.
    """
    if not MY_WHATSAPP_NUMBER or "000000000" in MY_WHATSAPP_NUMBER:
        print("⚠️ [WHATSAPP ERROR] Please set your real MY_WHATSAPP_NUMBER (with Country Code) in the .env file.")
        return
        
    print(f"📲 [WHATSAPP BRIDGE] Preparing to send real WhatsApp message to {MY_WHATSAPP_NUMBER}...")
    
    full_message = f"🤖 *DIGITAL FTE ALERT:*\n\n{message_body}\n\nCheck your computer for details."
    
    try:
        now = datetime.now()
        # pywhatkit needs future time (hours, minutes) to schedule. Let's do 1 minute from now, 
        # or use "sendwhatmsg_instantly" to send in a new active tab right away.
        
        # 'sendwhatmsg_instantly' opens a browser tab (if WhatsApp Web is logged in) and sends it.
        # wait_time is how long it waits for browser to load.
        pywhatkit.sendwhatmsg_instantly(
            phone_no=MY_WHATSAPP_NUMBER,
            message=full_message,
            wait_time=25, 
            tab_close=False
        )
        
        print(f"🚀 [WHATSAPP SENT SUCCESSFULLY] to {MY_WHATSAPP_NUMBER}")
        
    except Exception as e:
        print(f"❌ [WHATSAPP ERROR] Failed to send real message: {e}")
    
    # Log the notification
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📲 WHATSAPP INSTANT SENT: {message_body[:30]}...\n")

if __name__ == "__main__":
    # Test your own number by running this directly
    send_whatsapp_alert("✅ System Integration Test: Live WhatsApp Alert Working!")
