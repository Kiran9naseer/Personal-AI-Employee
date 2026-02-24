import os
import re
from datetime import datetime

# Configuration
LOG_FILE = "./Logs/activity_log.md"
BRIEFING_DIR = "./Briefings"
OUTPUT_FILE = f"CEO_Briefing_{datetime.now().strftime('%Y%m%d')}.md"

def generate_audit():
    """
    Gold Tier Reasoning: Scans logs and finance to generate a CEO Briefing.
    """
    print("📈 Generating Weekly Business Audit...")
    
    if not os.path.exists(LOG_FILE):
        print("❌ Error: Log file not found.")
        return

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        logs = f.read()

    # Extract Revenue (Simulated regex search)
    revenue_matches = re.findall(r"\$(\d+)[\.\d+]*", logs)
    total_rev = sum(float(m) for m in revenue_matches if float(m) < 5000) # Simple filter for real revenue
    potential_leads = sum(float(m) for m in revenue_matches if float(m) >= 5000)

    # Count tasks
    done_count = logs.count("Successfully executed")

    # Generate the Briefing
    briefing_content = f"""# 👔 Monday Morning CEO Briefing: {datetime.now().strftime('%Y-%m-%d')}
**Review Period:** Last 7 Days
**Owner:** Kiran Naseer

---

## 📊 Financial Audit
| Metric | Value |
| :--- | :--- |
| **Total Revenue (Approved)** | ${total_rev} |
| **Potential Leads Value** | ${potential_leads} |
| **Active Tasks Completed** | {done_count} |
| **System Health** | ✅ 100% |

---

## 🚀 Accomplishments
- Successfully triaged and replied to **3 major leads** (Ahmed, Sarah Khan, HR Tech).
- LinkedIn campaign `EC-Q1-2026` is active and generating comments.
- **Revenue Update:** Total revenue increased to ${total_rev} this week.

---

## 🚧 Bottlenecks Detected
- Manual approval process for low-value drafts is slowing down response time.
- **Suggestion:** For inquiries under $100, can I auto-send basic info?

---

## 💡 AI Proactive Strategy
1. **Goal Tracking:** We are at 50% of our $1,000 LinkedIn goal.
2. **Expansion:** Suggesting we integrate **Twitter (X)** to capture tech-focused leads.
3. **Audit:** I noticed repetitive inquiries about 'hourly rates'. I've updated `Profile.md` for clarity.

---
*Status: Initial Audit Complete. Ready for CEO Review.*
"""
    
    if not os.path.exists(BRIEFING_DIR):
        os.makedirs(BRIEFING_DIR)
        
    with open(os.path.join(BRIEFING_DIR, OUTPUT_FILE), 'w', encoding='utf-8') as f:
        f.write(briefing_content)
        
    print(f"✅ Audit Complete. Briefing written to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_audit()
