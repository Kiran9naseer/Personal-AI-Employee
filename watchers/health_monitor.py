import os
import time

# Configuration
PROCESSES = {
    "Simple Watcher": "simple_watcher.py",
    "Execution Engine": "execution_engine.py",
    "LinkedIn Watcher": "comment_watcher.py",
    "Gmail Watcher": "gmail_watcher_sim.py"
}
DASHBOARD_FILE = "Dashboard.md"

def check_health():
    print("🏥 Digital FTE Health Monitor Started...")
    
    while True:
        try:
            # For simulation in this environment, we check if specific flag files or simply simulate logic
            # In a real system, we'd use psutil to check active PIDs.
            
            # For now, let's assume if the files exist, we are good, 
            # but we can simulate a 'failure' if we want to test UI.
            system_ok = True 
            
            with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
                content = f.read()

            if "System Health** | ✅ Optimal" in content:
                # Keep it optimal for now unless we manually trigger a test failure
                pass
            
            time.sleep(60)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    check_health()
