import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

LOG_FILE = "./Logs/activity_log.md"

def post_to_linkedin(post_content):
    if not post_content or len(post_content) < 5:
        print("⚠️ LinkedIn Post content is empty.")
        return False
        
    print("🚀 [PLAYWRIGHT MODE] Starting LinkedIn Auto-Post...")
    
    clean_content = "\n".join([line for line in post_content.split('\n') if not line.startswith('#')])

    with sync_playwright() as p:
        user_data_dir = os.path.abspath("./playwright_profile")
        context = p.chromium.launch_persistent_context(
            user_data_dir, 
            headless=False,
            slow_mo=30,
            args=["--start-maximized"]
        )
        page = context.new_page()

        try:
            print("🌐 Opening LinkedIn Feed...")
            page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            time.sleep(5)

            # Login check
            if "login" in page.url or "checkpoint" in page.url:
                print("🔐 Please log in to LinkedIn in the browser...")
                input("👉 After logging in, press ENTER to continue: ")
                page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
                time.sleep(5)

            # ✅ Click "Start a post" using Playwright semantic locators
            print("📝 Clicking 'Start a post' button...")
            try:
                # Most reliable: role-based locator
                page.get_by_role("button", name="Start a post").first.click(timeout=15000)
                print("✅ Clicked via get_by_role.")
            except:
                try:
                    # Fallback 1: by text content
                    page.get_by_text("Start a post", exact=False).first.click(timeout=10000)
                    print("✅ Clicked via get_by_text.")
                except:
                    # Fallback 2: Click the share box trigger div
                    print("⚠️ Trying share-box trigger...")
                    page.locator("div.share-box-feed-entry__trigger").first.click(timeout=10000)

            # Wait longer for dialog animation
            time.sleep(6)

            # Find the textbox - Try multiple selectors
            print("⌨️ Locating textbox...")
            textbox = None
            for selector in [
                "div.ql-editor",
                "div[contenteditable='true']",
                "div[role='textbox']"
            ]:
                try:
                    t = page.locator(selector).first
                    t.wait_for(state="visible", timeout=8000)
                    textbox = t
                    print(f"✅ Textbox found: {selector}")
                    break
                except:
                    continue

            if not textbox:
                raise Exception("Textbox not found with any selector.")

            textbox.click()
            time.sleep(1)

            # Type content fast
            print("✍️ Typing content...")
            for char in clean_content:
                page.keyboard.type(char, delay=5)

            time.sleep(3)

            # Click Post button
            print("🚀 Clicking Post button...")
            try:
                post_btn = page.locator("button.share-actions__primary-action").first
                post_btn.wait_for(state="visible", timeout=15000)
                post_btn.click()
            except:
                # Fallback JS click
                page.evaluate("""
                    const btns = [...document.querySelectorAll('button')];
                    const postBtn = btns.find(b => b.innerText.trim() === 'Post');
                    if (postBtn) postBtn.click();
                """)

            # ✅ Handle LinkedIn Duplicate Warning Dialog
            time.sleep(3)
            try:
                post_anyway = page.get_by_role("button", name="Post anyway")
                if post_anyway.is_visible():
                    print("⚠️ Duplicate warning detected. Clicking 'Post anyway'...")
                    post_anyway.click()
            except:
                pass

            print("✅ LinkedIn Post Successful!")
            
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 🟦 LINKEDIN PLAYWRIGHT: OK\n")

            time.sleep(10)
            context.close()
            return True

        except Exception as e:
            print(f"❌ Playwright Error: {e}")
            input("❌ Flow interrupted. Press ENTER to close...")
            context.close()
            return False

if __name__ == "__main__":
    from datetime import datetime
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
    hackathon_post = (
        f"[{timestamp}] I'm excited to share that I've successfully built and deployed a Fully Autonomous Digital FTE! 🚀\n\n"
        "This post was just published by my AI agent, which handles multi-channel social media engagement, "
        "email management, and workflow automation without any human intervention. Leveraging the power of "
        "Gemini 1.5 Flash and Playwright, my AI Employee is now live and operational. 🛠️👔\n\n"
        "#AI #DigitalFTE #Automation #GenerativeAI #Playwright #Hackathon #FutureOfWork"
    )
    post_to_linkedin(hackathon_post)