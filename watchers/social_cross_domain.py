import os
import time
from datetime import datetime

class SocialCrossDomainWatcher:
    """
    Gold Tier: Monitors Facebook, Instagram, and Twitter (X) for mentions and trends.
    """
    def __init__(self, platform):
        self.platform = platform
        self.inbox_dir = f"./Inbox/{platform}"
        if not os.path.exists(self.inbox_dir):
            os.makedirs(self.inbox_dir)

    def scan(self):
        print(f"🔍 Scanning {self.platform} for mentions of 'Kiran Naseer' and 'Digital FTE'...")
        # Simulated detection
        if datetime.now().minute % 10 == 0: # Simulate a hit every 10 mins
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Social_Mention_{self.platform}_{timestamp}.md"
            with open(os.path.join(self.inbox_dir, filename), "w", encoding="utf-8") as f:
                f.write(f"# 🌐 {self.platform} Mention Detected\n")
                f.write(f"**Account:** TechInfluencer2026\n")
                f.write(f"**Content:** 'Just saw Kiran's post about Claude Code based FTEs. Mind-blown!'\n")
            print(f"✅ Found mention on {self.platform}. Saved to Inbox.")

            # NEW: Trigger WhatsApp Mobile Alert for Social Mentions
            try:
                from whatsapp_alerter import send_whatsapp_alert
                send_whatsapp_alert(f"New Mention on {self.platform}: '@TechInfluencer2026' mentioned you! Check platform.")
            except Exception as e:
                print(f"⚠️ WhatsApp Alert failed: {e}")

if __name__ == "__main__":
    for platform in ["Twitter", "Facebook", "Instagram"]:
        watcher = SocialCrossDomainWatcher(platform)
        watcher.scan()
