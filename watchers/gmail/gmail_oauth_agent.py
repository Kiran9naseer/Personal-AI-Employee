import os
import sys
import base64
import time
from datetime import datetime
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Add parent path to allow importing whatsapp alerter and .env
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# If modifying these scopes, delete the file token.json.
# This scope allows us to read, compose, and send emails securely.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# DIRECTORIES
NEEDS_ACTION_DIR = "./Needs_Action"
PENDING_APPROVAL_DIR = "./Pending_Approval"
LOG_FILE = "./Logs/activity_log.md"

def get_gmail_service():
    """Authenticates using OAuth 2.0 and returns the Gmail API service."""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    # The file token.json stores the user's access and refresh tokens
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"❌ '{creds_path}' not found!")
                print("⚠️ Please follow the Google Cloud Console instructions to download it.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        print("✅ Correctly Authenticated with Gmail API (OAuth 2.0)")
        return service
    except HttpError as error:
        print(f'❌ An error occurred: {error}')
        return None

def read_unread_emails(service):
    """
    Reads unread emails and saves them to the /Needs_Action/ directory.
    """
    try:
        # Request unread messages
        results = service.users().messages().list(userId='me', q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print("📭 No new unread messages in Gmail.")
            return

        print(f"📨 Found {len(messages)} unread messages. Processing...")
        
        if not os.path.exists(NEEDS_ACTION_DIR):
            os.makedirs(NEEDS_ACTION_DIR)

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['From', 'Subject']).execute()
            headers = msg.get('payload', {}).get('headers', [])
            
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            
            # Save the email to Needs_Action for the AI to process
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Email_Inquiry_{timestamp}.md"
            filepath = os.path.join(NEEDS_ACTION_DIR, filename)
            
            content = f"""# 📧 NEW EMAIL INQUIRY
**From:** {sender}
**Subject:** {subject}
**Message ID:** {message['id']}

---
**Agent Instruction:**
Claude, please read this inquiry, generate a tailored reply draft, and save the draft to `/Pending_Approval/`. Do NOT send it until the Human approves.
"""
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Remove UNREAD label (mark as read)
            service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
            
            print(f"📥 Saved to Needs_Action: {subject[:40]}... (From: {sender})")
            
            # Log it
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📧 GMAIL OAUTH: Downloaded new email from {sender} to /Needs_Action.\n")

    except HttpError as error:
        print(f'❌ An error occurred fetching emails: {error}')

def create_draft_email(service, to_email, subject, body_text):
    """
    Creates a draft email in the user's Gmail account (Visible in Drafts folder).
    """
    try:
        message = EmailMessage()
        message.set_content(body_text)
        message['To'] = to_email
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}
        
        draft = service.users().drafts().create(userId='me', body=create_message).execute()
        print(f"📝 Draft created successfully in Gmail! Draft ID: {draft['id']}")
        return draft
    except HttpError as error:
        print(f'❌ An error occurred while creating draft: {error}')
        return None

def send_email(service, to_email, subject, body_text):
    """
    Sends an email directly. Used by the Execution Engine AFTER human approval.
    """
    try:
        message = EmailMessage()
        message.set_content(body_text)
        message['To'] = to_email
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        send_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f"🚀 Email sent successfully (Approved by Human)! Message ID: {send_message['id']}")
        return send_message
    except HttpError as error:
        print(f'❌ An error occurred while sending email: {error}')
        return None

if __name__ == '__main__':
    print("====================================")
    print("📧 GMAIL OAUTH AGENT (LIVE)")
    print("====================================")
    
    # 1. Authenticate and build service
    service = get_gmail_service()
    
    if service:
        # 2. Read new emails and pull into Needs_Action
        read_unread_emails(service)
        
        # Testing specific functions manually if needed:
        # create_draft_email(service, "test@example.com", "Test Draft", "This is an automated AI draft.")
        # send_email(service, "test@example.com", "Approved Action", "This was sent fully automatically via OAuth.")
