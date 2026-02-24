import os
import time
from datetime import datetime

# Configuration
INBOX_DIR = "./Inbox/Emails"
LOG_FILE = "./Logs/activity_log.md"

def simulate_gmail_watcher():
    """
    Simulates monitoring Gmail for high-priority keywords.
    """
    print("📧 Gmail Priority Watcher Started...")
    
    try:
        while True:
            # Simulated sensitive/high-priority email
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Priority_Email_{timestamp}.md"
            filepath = os.path.join(INBOX_DIR, filename)
            
            if len(os.listdir(INBOX_DIR)) < 2: # Keep it simple for simulation
                content = f"""# 📧 PRIORITY EMAIL: Project Inquiry
**From:** hrm@tech-startup.com
**Subject:** Digital FTE Implementation for our Team
**Body:**
Dear Kiran, we saw your LinkedIn post about Digital FTE systems. 
We want to automate our HR onboarding. Can we discuss a $5,000 package?

---
**Agent Notes:**
- High Value Detected ($5,000).
- Immediate Human Attention required.
"""
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                
                print(f"📧 New priority email detected! Saved to {filename}")
                
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📧 GMAIL ALERT: High-value inquiry detected ($5,000).\n")

            time.sleep(600) # Check every 10 minutes
    except KeyboardInterrupt:
        print("\n🛑 Gmail Watcher Stopped.")

if __name__ == "__main__":
    simulate_gmail_watcher()
