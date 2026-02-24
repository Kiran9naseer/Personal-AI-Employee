import os
import time
from datetime import datetime

# Configuration
INBOX_DIR = "./Inbox/Freelance"
LOG_FILE = "./Logs/activity_log.md"

if not os.path.exists(INBOX_DIR):
    os.makedirs(INBOX_DIR)

def simulate_freelance_feed():
    """
    Gold/Platinum Tier: Monitors Freelance platforms for new job postings.
    """
    print("🕵️‍♀️ Freelance Watcher Started: Scanning Upwork/Freelancer/Fiverr...")
    
    while True:
        # Simulation: Randomly detect a high-quality job every few minutes
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Freelance_Job_{timestamp}.md"
        filepath = os.path.join(INBOX_DIR, filename)

        # Simulated Job Posting
        job_description = """
        **Project Title:** AI Automation for Real Estate
        **Budget:** $500 - $1,500
        **Description:** I need a freelancer to build an automated follow-up system for my real estate leads. 
        It should use Claude/OpenAI and integrate with a CRM.
        """
        
        content = f"""# 📈 NEW FREELANCE JOB: {timestamp}
**Platform:** Upwork (Simulated)
**Budget:** $500 - $1,500
**Category:** AI & Automation

---
**Description:**
{job_description}

---
**Agent Instruction:**
1. Match skills with `Profile.md`.
2. Draft a Tailored Proposal focusing on our "Digital FTE" experience.
3. Move to `Needs_Action` for Kiran to review.
"""
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ New Job Detected: Created {filename}")

        # NEW: Trigger WhatsApp Mobile Alert
        try:
            from whatsapp_alerter import send_whatsapp_alert
            send_whatsapp_alert(f"New High-Value Job Detected on Upwork: {job_description[:50]}... Budget: $500+")
        except Exception as e:
            print(f"⚠️ WhatsApp Alert failed: {e}")
        
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📈 FREELANCE ALERT: New Job detected via RSS simulation ($500+).\n")
            
        time.sleep(600) # Check every 10 minutes in simulation

if __name__ == "__main__":
    try:
        simulate_freelance_feed()
    except KeyboardInterrupt:
        print("\n🛑 Freelance Watcher Stopped.")
