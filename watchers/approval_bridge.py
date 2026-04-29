import os
import time
from whatsapp_alerter import send_whatsapp_alert

def run_approval_demo():
    print("🤖 [DECISION ENGINE] Reviewing drafted proposals...")
    time.sleep(3)
    
    print("📝 Drafted Proposal for: 'AI Automation for Real Estate' (Budget $1,500)")
    print("-" * 50)
    print("PROPOSAL PREVIEW: 'Hello! I noticed you need a CRM automation system. My Digital FTE framework is perfect for this...'")
    print("-" * 50)
    
    # Send the approval request to WhatsApp
    print("\n📲 Sending approval request to CEO via WhatsApp...")
    approval_msg = "CEO, I have drafted a proposal for the Real Estate AI project ($1,500). Please reply 'Approve' to send it."
    send_whatsapp_alert(approval_msg)
    
    print("\n⏳ [WAITING FOR CEO APPROVAL]...")
    
    # Recording user interaction
    user_input = input("\n👉 Type 'APPROVE' to authorize the agent: ").strip().upper()
    
    if user_input == "APPROVE":
        print("\n✅ [AUTH GRANTED] Proceeding with submission...")
        time.sleep(2)
        print("🚀 Submitting proposal to Platform API...")
        time.sleep(3)
        print("🎯 [SUCCESS] Proposal sent to client. Moved to 'Interview' stage.")
        
        # Final confirmation to WhatsApp
        send_whatsapp_alert("Task Complete: Proposal has been sent to the Real Estate client. Tracking responses now.")
    else:
        print("\n🛑 [REJECTED] Action canceled by CEO.")

if __name__ == "__main__":
    print("💼 DIGITAL FTE: Starting Human-in-the-Loop Approval Bridge...")
    try:
        run_approval_demo()
    except KeyboardInterrupt:
        print("\n🛑 System Halted.")
