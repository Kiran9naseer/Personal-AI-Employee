import os
import time
from datetime import datetime
import shutil

# Configuration
APPROVED_DIR = "./Approved"
DONE_DIR = "./Done"
LOG_FILE = "./Logs/activity_log.md"

def start_execution_engine():
    """
    Silver Tier Engine: This script watches the /Approved folder.
    When a user moves a Plan.md there, it 'executes' the task.
    """
    print("🚀 Silver Tier Execution Engine Started...")
    print(f"Monitoring: {APPROVED_DIR} for human approvals...")

    if not os.path.exists(DONE_DIR):
        os.makedirs(DONE_DIR)

    try:
        while True:
            files = [f for f in os.listdir(APPROVED_DIR) if f.endswith(".md")]
            for filename in files:
                file_path = os.path.join(APPROVED_DIR, filename)
                
                print(f"🎯 Execution Triggered: {filename}")
                
                # SIMULATION: In a real Silver Tier, this is where we would call MCP servers
                # For now, we simulate the 'Action' (Email, LinkedIn Post, etc.)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Logic to determine action based on file content
                action_type = "External Communication" if "REPLY" in content.upper() or "INVOICE" in content.upper() else "General Task"

                print(f"⚙️ Executing {action_type}...")
                
                # LINKEDIN AUTO-POST INTEGRATION
                if "LINKEDIN" in filename.upper() or "POST" in filename.upper():
                    print("🌐 LinkedIn Post detected. Sending to LinkedIn Poster...")
                    try:
                        import sys
                        sys.path.append(os.path.dirname(__file__))
                        from linkedin_poster import post_to_linkedin
                        # Pass the content to the poster
                        post_to_linkedin(content)
                    except Exception as e:
                        print(f"❌ Failed to auto-post to LinkedIn: {e}")
                        
                else:
                    time.sleep(2) # Simulate work for other tasks

                # Move to Done
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"EXECUTED_{timestamp}_{filename}"
                shutil.move(file_path, os.path.join(DONE_DIR, new_name))

                # Log the Success
                with open(LOG_FILE, "a", encoding='utf-8') as log:
                    log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 🚀 AGENT ACTION: Successfully executed and archived {filename}\n")

                print(f"✅ {filename} processed and moved to /Done.")

            time.sleep(5) # Poll every 5 seconds
    except KeyboardInterrupt:
        print("\n🛑 Execution Engine Stopped.")

if __name__ == "__main__":
    start_execution_engine()
