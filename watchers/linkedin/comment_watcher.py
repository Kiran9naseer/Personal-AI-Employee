import os
import time
from datetime import datetime

# Configuration
INBOX_DIR = "./Inbox/WhatsApp" # Using WhatsApp folder as a generic 'Social' inbox for now
LOG_FILE = "./Logs/activity_log.md"

def simulate_linkedin_comments():
    """
    Simulates watching for specific keywords in LinkedIn comments (e.g., 'AUTOPILOT').
    In Silver Tier, this brings leads directly into the vault.
    """
    print("🎨 LinkedIn Engagement Watcher Started...")
    
    try:
        while True:
            # Simulation: Randomly detect a comment every few minutes (simulated)
            # For testing, we create a lead immediately if the user wants
            
            # Simulated comment data
            leads = [
                {"name": "Sarah Khan", "comment": "AUTOPILOT! I need this for my boutique."},
                {"name": "John Doe", "comment": "Interested. AUTOPILOT please."}
            ]
            
            for lead in leads:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"LinkedIn_Lead_{lead['name'].replace(' ', '_')}_{timestamp}.md"
                filepath = os.path.join(INBOX_DIR, filename)
                
                if not os.path.exists(filepath):
                    content = f"""# 🚀 NEW LEAD: LinkedIn Engagement
**Client:** {lead['name']}
**Keyword Detected:** AUTOPILOT
**Timestamp:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Platform:** LinkedIn

---
**Message/Comment:**
"{lead['comment']}"

---
**Agent Instruction:**
1. Refer to `Profile.md` for consultation rates.
2. Draft a personalized response for Kiran Naseer.
3. Move to `Needs_Action` for approval.
"""
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    
                    print(f"📈 Found new lead: {lead['name']}! Created {filename}")
                    
                    with open(LOG_FILE, "a", encoding="utf-8") as log:
                        log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📈 LEAD GENERATED: {lead['name']} via LinkedIn comment monitoring.\n")
            
            time.sleep(300) # Check every 5 minutes
    except KeyboardInterrupt:
        print("\n🛑 LinkedIn Watcher Stopped.")

if __name__ == "__main__":
    simulate_linkedin_comments()
