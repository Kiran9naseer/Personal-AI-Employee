import os
import sys
import time
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from dotenv import load_dotenv

# Path setup to access whatsapp_alerter and .env running from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

INBOX_DIR = "./Inbox/Emails"
LOG_FILE = "./Logs/activity_log.md"

def get_real_gmail_alerts():
    """
    Connects to Gmail via IMAP, searches for unseen emails from LinkedIn, FB, Upwork.
    Creates urgent alerts in Inbox/Emails and triggers WhatsApp alerts.
    """
    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        print("⚠️ GMAIL_EMAIL or GMAIL_APP_PASSWORD not found in .env.")
        print("Please add them to enable LIVE scanning.")
        return
        
    print(f"📧 Connecting to Live Gmail IMAP ({GMAIL_EMAIL})...")
    
    try:
        # Create an IMAP4 class with SSL 
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
        
        # Select the mailbox you want to check (default: INBOX)
        mail.select("inbox")
        
        # Search for unseen emails
        status, messages = mail.search(None, 'UNSEEN')
        
        if status == "OK" and messages[0]:
            mail_ids = messages[0].split()
            print(f"📨 Found {len(mail_ids)} unseen emails. Scanning for social/urgent hits...")
            
            for _id in mail_ids:
                res, msg_data = mail.fetch(_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                            
                        from_ = msg.get("From")
                        
                        # Filtering Logic (LinkedIn, Facebook, Upwork, OR an explicit TEST email)
                        sender_lower = str(from_).lower()
                        subject_lower = str(subject).lower()
                        
                        is_social = "linkedin" in sender_lower or "facebook" in sender_lower or "upwork" in sender_lower
                        is_test = "test fte" in subject_lower

                        if is_social or is_test:
                            print(f"✅ Priority Email Detected: {subject[:50]} (From: {from_})")
                            
                            # Determine Domain
                            domain = "Social"
                            if "linkedin" in sender_lower: domain = "LinkedIn"
                            elif "facebook" in sender_lower: domain = "Facebook"
                            elif "upwork" in sender_lower: domain = "Upwork"
                            elif is_test: domain = "TEST"

                            
                            # Trigger WhatsApp Bridge
                            try:
                                from watchers.whatsapp_alerter import send_whatsapp_alert
                                alert_message = f"D-FTE 🚨 Alert: New {domain} Activity!\nSubject: {subject[:50]}...\nCheck Inbox to respond."
                                send_whatsapp_alert(alert_message)
                            except Exception as e:
                                print(f"⚠️ WhatsApp Alert bridge failed: {e}")
                                
                            # Save to Digital FTE Inbox
                            if not os.path.exists(INBOX_DIR):
                                os.makedirs(INBOX_DIR)
                                
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filepath = os.path.join(INBOX_DIR, f"Priority_Social_Alert_{timestamp}.md")
                            content = f"# 📧 LIVE PRIORITY ALERT: {domain}\n**From:** {from_}\n**Subject:** {subject}\n\n**Agent Notes:**\n- Immediate notification sent via WhatsApp.\n- Please review on your mobile app or PC."
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(content)
                                
                            with open(LOG_FILE, "a", encoding="utf-8") as log:
                                log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📧 GMAIL BRIDGE: Forwarded {domain} alert to WhatsApp.\n")
        else:
            print("📭 No new emails detected in this cycle.")
            
        mail.logout()
    except Exception as e:
        print(f"🛑 Error checking Gmail IMAP: {e}")

def run_watcher():
    print("====================================")
    print("📧 LIVE GMAIL -> WHATSAPP BRIDGE ON")
    print("====================================")
    try:
        while True:
            get_real_gmail_alerts()
            time.sleep(300) # Check every 5 minutes to avoid rate limits
    except KeyboardInterrupt:
        print("\n🛑 Live Bridge Stopped.")

if __name__ == "__main__":
    run_watcher()
