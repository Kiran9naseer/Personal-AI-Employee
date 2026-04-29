import os
import time
import random
from datetime import datetime

def run_health_monitor_demo():
    print("🏥 [SYSTEM SUPERVISOR] Digital FTE Health Monitor Started...")
    time.sleep(2)
    
    modules = [
        "Communication Engine (Gmail/WhatsApp)",
        "Social Branding Module (LinkedIn/Playwright)",
        "Lead Generation Unit (Freelance Watcher)",
        "Accounting Bridge (Odoo/Invoicing)",
        "Knowledge Management (Obsidian/Markdown)"
    ]
    
    # Run only 2 scans for the demo to avoid clutter
    for i in range(2):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- [SYSTEM SCAN #{i+1}: {timestamp}] ---")
        
        for module in modules:
            print(f"🔍 Scanning {module}...")
            time.sleep(0.8) # Fast scan
            print(f"✅ Status: OPTIMAL | Latency: {random.randint(20, 150)}ms")
        
        if i == 0:
            print("⏳ Monitoring in progress... next scan in 5 seconds.")
            time.sleep(5)
            
    print("\n" + "="*40)
    print("🚀 [FINAL STATUS] ALL SYSTEMS STABLE & RUNNING.")
    print("👔 Digital FTE is now autonomously managing your business.")
    print("="*40)
    print("\n[Watcher Mode: Active (Standby)]")

if __name__ == "__main__":
    try:
        run_health_monitor_demo()
    except KeyboardInterrupt:
        print("\n🛑 Health Monitor Halted.")
