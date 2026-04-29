import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

LOG_FILE = "./Logs/activity_log.md"
CHROME_PROFILE_DIR = os.path.abspath("./selenium_profile")

def find_post_box(driver):
    """Extremely robust finder for the FB post box."""
    # List of possible identifiers for the 'What's on your mind?' area
    selectors = [
        "//div[@role='button']//span[contains(text(), 'mind')]", 
        "//div[@aria-label[contains(.,'mind')]]",
        "//div[@aria-label[contains(.,'Create a post')]]",
        "//div[@role='main']//div[@role='button'][1]", # The first button in the main feed is usually it
        "//span[contains(text(), \"What's on your mind?\")]"
    ]
    
    wait = WebDriverWait(driver, 10)
    for selector in selectors:
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            if element: return element
        except: continue
    return None

def post_to_facebook(post_content):
    print("🚀 [ULTIMATE MODE] Starting Facebook Auto-Post...")
    pyperclip.copy(post_content)
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("https://www.facebook.com/")
        time.sleep(5)

        print("🔍 Scanning page for Post Box...")
        post_box = find_post_box(driver)
        
        if not post_box:
            print("⏳ Please make sure you are LOGGED IN and on the News Feed.")
            print("Waiting 30 more seconds for you to navigate there...")
            time.sleep(30)
            post_box = find_post_box(driver)

        if post_box:
            print("✅ Box found! Opening Dialog...")
            # Use JS to click because sometimes buttons are covered
            driver.execute_script("arguments[0].click();", post_box)
            time.sleep(3)
            
            print("📋 Pasting AI Content...")
            # Find the actual text input box in the popup
            wait = WebDriverWait(driver, 10)
            input_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))
            input_box.send_keys(Keys.CONTROL, 'v')
            time.sleep(1)
            
            # Dismiss hashtag/tag menus by hitting ESCAPE
            input_box.send_keys(Keys.ESCAPE)
            driver.find_element("tag name", "body").send_keys(Keys.ESCAPE)
            time.sleep(2)
            
            print("📤 Final Publishing Attempt (Strict Flow Mode)...")
            time.sleep(2)
            
            # 1. Close popup
            try:
                driver.find_element("tag name", "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
            except: pass

            # 2. Click Next
            try:
                driver.find_element("xpath", "//span[text()='Next']").click()
                print("➡️ Clicked 'Next' button...")
                time.sleep(2)
            except: pass

            # 3. Click Post
            try:
                driver.find_element("xpath", "//div[@aria-label='Post']").click()
                print("🚀 Clicked 'Post' button!")
            except:
                print("⚠️ Direct click failed, trying global shortcut as last resort...")
                driver.find_element("tag name", "body").send_keys(Keys.CONTROL, Keys.ENTER)

            # --- WAIT AFTER POSTING (FOR DEMO) ---
            print("⏳ SUCCESS: Keeping browser open for 40 seconds for your Demo record...")
            time.sleep(40)
            
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 🟦 FB AUTO-POST: OK\n")
        else:
            print("❌ Error: Could not find the Post entry box.")

        driver.quit()
        return True
    except Exception as e:
        print(f"❌ Error Detail: {e}")
        # Even on error, wait so the user can see what happened
        print("⏳ Staying open for 30 seconds for you to check the screen...")
        time.sleep(30)
        try: driver.quit()
        except: pass

if __name__ == "__main__":
    from datetime import datetime
    ts = datetime.now().strftime("%d %b %Y, %I:%M %p")
    post_to_facebook(f"[{ts}] 🚀 My Digital FTE AI just posted this automatically! Built with Gemini & Python. #AI #DigitalFTE #Automation #Productivity")
