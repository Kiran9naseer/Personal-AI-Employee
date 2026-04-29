import os
import time
from datetime import datetime

# Configuration
INBOX_DIR = "./Inbox/Freelance"
LOG_FILE = "./Logs/activity_log.md"

if not os.path.exists(INBOX_DIR):
    os.makedirs(INBOX_DIR)

def trigger_demo_freelance_alert():
    """
    Demo Version: Triggers a single freelance alert and then exits.
    """
    print("🕵️‍♀️ [DEMO MODE] Freelance Watcher Started...")
    time.sleep(3) # Wait 3 seconds so you can start recording
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Freelance_Job_{timestamp}.md"
    filepath = os.path.join(INBOX_DIR, filename)

    # Simulated Job Posting
    job_description = """
    **Project Title:** AI Automation for Real Estate
    **Budget:** $500 - $1,500
    **Description:** I need a freelancer to build an automated follow-up system for my real estate leads using Gemini and WhatsApp.
    """
    
    content = f"""# 📈 NEW FREELANCE JOB: {timestamp}
**Platform:** Upwork (Simulated)
**Budget:** $1,500
**Category:** AI & Automation

---
{job_description}
---
**Agent Instruction:** Draft a Tailored Proposal focusing on our "Digital FTE" experience.
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ New Job Detected: Created {filename}")

    # Trigger WhatsApp Mobile Alert
    try:
        from whatsapp_alerter import send_whatsapp_alert
        print("📲 Forwarding alert to CEO via WhatsApp...")
        send_whatsapp_alert(f"New High-Value Job Detected on Upwork: AI Automation for Real Estate ($1,500). Action Needed!")
    except Exception as e:
        print(f"⚠️ WhatsApp Alert failed: {e}")
    
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📈 FREELANCE ALERT: Demo alert sent successfully.\n")
    
    print("\n🎉 Demo alert sequence complete. Watcher standing by.")

if __name__ == "__main__":
    trigger_demo_freelance_alert()
