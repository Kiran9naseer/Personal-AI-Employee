import time
import os
from datetime import datetime

# Configuration
WATCH_DIR = "./Inbox"
LOG_FILE = "./Logs/watcher_log.md"

def simulate_watcher():
    """Simulates a watcher detecting a new email or message."""
    print("🚀 Digital FTE Watcher Started...")
    
    # Create Logs directory if it doesn't exist
    if not os.path.exists("./Logs"):
        os.makedirs("./Logs")

    # Run a simple loop to check for activity (simulated)
    # In a real scenario, this would be a Gmail API webhook or similar
    try:
        while True:
            # For demonstration, we'll create a dummy 'New Email' file if Inbox is empty
            files = os.listdir(WATCH_DIR)
            if not files or len(files) < 1:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"New_Email_{timestamp}.md"
                filepath = os.path.join(WATCH_DIR, filename)
                
                content = f"""# 📧 New Email Detected
**From:** client@example.com
**Subject:** Invoice Request for Project X
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
**Body:**
Hi, can you please send me the invoice for last month's consultation? Thanks!
"""
                with open(filepath, "w") as f:
                    f.write(content)
                
                print(f"✅ Detected new activity. Created: {filename}")
                
                with open(LOG_FILE, "a") as log:
                    log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] Created task: {filename}\n")
            
            time.sleep(60) # Watch every 60 seconds
    except KeyboardInterrupt:
        print("\n🛑 Watcher Stopped.")

if __name__ == "__main__":
    simulate_watcher()
