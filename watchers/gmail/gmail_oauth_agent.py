import os
import sys
import base64
import time
from datetime import datetime
import email
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai
from dotenv import load_dotenv

# Path setup to access whatsapp_alerter and .env running from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# DIRECTORIES
NEEDS_ACTION_DIR = "./Needs_Action"
LOG_FILE = "./Logs/activity_log.md"

# Configure Gemini Brain
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gmail_service():
    """Authenticates using OAuth 2.0 and returns the Gmail API service."""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"❌ '{creds_path}' not found!")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        print("✅ Correctly Authenticated with Gmail API (OAuth 2.0)")
        return service
    except HttpError as error:
        print(f'❌ An error occurred: {error}')
        return None

def extract_email_body(email_msg):
    """Extracts text content from an email message."""
    if email_msg.is_multipart():
        for part in email_msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                return part.get_payload(decode=True).decode('utf-8', errors='ignore')
    else:
        return email_msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    return ""

def generate_ai_reply(sender, subject, body):
    """Uses Gemini API to Triage the email and generate a smart business reply if it's legit."""
    if not GEMINI_KEY:
        return "IGNORE_PROMO" # Safe fallback
    
    prompt = f"""You are the AI Assistant / Inbox Manager for Kiran Naseer's Digital FTE business. 
You received a new email from: {sender}.
Subject: {subject}
Message Body:
{body}

TASK 1: TRIAGE
Is this email a promotional newsletter, automated alert, spam, marketing, or from a company like foodpanda, streamlabs, canva, facebook, linkedin, etc?
If YES, you must reply with exactly this exact word and nothing else: IGNORE_PROMO

TASK 2: REPLY
If it is from a real human making a business inquiry or sending a direct message, write a professional, short, and polite reply addressing their message. Sign it off as:
Best regards,
Digital FTE (On behalf of Kiran Naseer)"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ AI Generation Error: {e}")
        return "IGNORE_PROMO"

def send_email(service, to_email, subject, body_text):
    """Sends an email directly using Gmail API."""
    try:
        message = EmailMessage()
        message.set_content(body_text)
        message['To'] = to_email
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        send_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f"🚀 Reply sent successfully! Message ID: {send_message['id']}")
        return send_message
    except HttpError as error:
        print(f'❌ Error sending email: {error}')
        return None

def read_unread_emails_and_autoreply(service):
    """Reads unread emails, asks the Gemini AI Brain, and automatically sends the reply."""
    try:
        results = service.users().messages().list(userId='me', q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print("📭 No new unread messages... watching...")
            return

        print(f"📨 Found {len(messages)} unread messages. AI Processor Initialized.")
        
        for message in messages:
            # Fetch full RAW format to get the body
            msg_raw = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
            msg_str = base64.urlsafe_b64decode(msg_raw['raw'].encode('ASCII')).decode('utf-8', errors='ignore')
            email_msg = email.message_from_string(msg_str)
            
            sender = email_msg.get("From", "Unknown")
            subject = email_msg.get("Subject", "No Subject")
            body = extract_email_body(email_msg)
            
            # Simple check to avoid replying to our own automated messages or no-reply addresses
            if "no-reply" in sender.lower() or "noreply" in sender.lower() or "mailer-daemon" in sender.lower():
                service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                continue
                
            print(f"📥 Processing Mail from: {sender} | Subject: {subject}")
            
            # --- 1. AI Triage & Reply Generation ---
            print("🧠 Gemini AI Brain analyzing if this is Promo or Real Inquiry...")
            ai_reply = generate_ai_reply(sender, subject, body)
            
            # AI decided this is a promotional/marketing email, DO NOT REPLY
            if ai_reply == "IGNORE_PROMO":
                print(f"🛑 AI Triage: Trashed Promotional/Auto Email from {sender}.")
                # Mark as read so we don't process it again
                service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
                continue
            
            reply_subject = f"Re: {subject}" if not subject.startswith("Re:") else subject
            
            # --- 2. Automatically Send the Reply (Only to Humans) ---
            print(f"🚀 Sending automated reply to {sender}...")
            send_email(service, sender, reply_subject, ai_reply)
            
            # --- 3. Save Record and Mark as Read ---
            service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
            
            if not os.path.exists(NEEDS_ACTION_DIR):
                os.makedirs(NEEDS_ACTION_DIR)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(NEEDS_ACTION_DIR, f"AutoReplied_{timestamp}.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# 🤖 AUTO-REPLIED RECORD\n**From:** {sender}\n**Subject:** {subject}\n\n**-- Original Message --**\n{body}\n\n**-- AI Sent This Auto-Reply --**\n{ai_reply}")
            
            # --- 4. WhatsApp Alert ---
            try:
                from watchers.whatsapp_alerter import send_whatsapp_alert
                send_whatsapp_alert(f"I just Auto-Replied to an INQUIRY from {sender[:20]}!\nThe AI handled it completely. Promo emails were ignored.")
            except Exception as e:
                pass
            
            # Log it
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 🤖 AUTO-REPLY SENT to human {sender}.\n")

    except HttpError as error:
        print(f'❌ An error occurred fetching emails: {error}')

def run_watcher():
    print("=====================================================")
    print("🤖 GMAIL FULLY AUTONOMOUS AI AGENT (GEMINI POWERED)")
    print("=====================================================")
    service = get_gmail_service()
    if service:
        while True:
            read_unread_emails_and_autoreply(service)
            time.sleep(30) # Fast check (Every 30 seconds) so you don't have to wait

if __name__ == '__main__':
    run_watcher()
