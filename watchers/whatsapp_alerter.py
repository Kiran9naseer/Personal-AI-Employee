import os
import time
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

MY_WHATSAPP_NUMBER = os.getenv("MY_WHATSAPP_NUMBER")
LOG_FILE = "./Logs/activity_log.md"

def send_whatsapp_alert(message_body):
    if not MY_WHATSAPP_NUMBER or "000000000" in MY_WHATSAPP_NUMBER:
        print("⚠️ [WHATSAPP] Set MY_WHATSAPP_NUMBER in .env file.")
        return

    print(f"📲 [WHATSAPP] Sending alert to {MY_WHATSAPP_NUMBER}...")

    full_message = f"🤖 *DIGITAL FTE ALERT:*\n\n{message_body}\n\nCheck your computer for details."
    encoded_message = urllib.parse.quote(full_message)
    whatsapp_url = f"https://web.whatsapp.com/send?phone={MY_WHATSAPP_NUMBER}&text={encoded_message}"

    # Use a dedicated WhatsApp profile so it stays logged in
    wa_profile = os.path.abspath("./whatsapp_profile")
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument(f"--user-data-dir={wa_profile}")

    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        print("🌐 Opening WhatsApp Web...")
        driver.get(whatsapp_url)

        print("⏳ Starting WhatsApp synchronization...")
        
        # Try multiple XPaths for different WhatsApp Web versions
        # This will wait ONLY as long as needed (up to 60s), not unconditionally.
        wait = WebDriverWait(driver, 60)
        msg_box = None
        for xpath in [
            "//div[@contenteditable='true'][@data-tab='10']",
            "//div[@title='Type a message']",
            "//footer//div[@contenteditable='true']",
            "//div[@role='textbox']"
        ]:
            try:
                msg_box = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                print("✅ Input box found!")
                break
            except:
                continue

        if not msg_box:
            raise Exception("WhatsApp input box not found. Please scan QR code and retry.")

        # Click input box to ensure focus
        time.sleep(0.5)
        msg_box.click()
        time.sleep(0.5)

        # Click the Send button directly
        send_btn = None
        for xpath in [
            "//button[@aria-label='Send']",
            "//span[@data-icon='send']",
            "//button[@data-testid='compose-btn-send']",
            "//div[@role='button'][@aria-label='Send']"
        ]:
            try:
                send_btn = driver.find_element(By.XPATH, xpath)
                if send_btn:
                    print("✅ Send button found!")
                    break
            except:
                continue

        if send_btn:
            driver.execute_script("arguments[0].click();", send_btn)
        else:
            # Last resort: press Enter
            msg_box.send_keys(Keys.ENTER)

        print(f"✅ [WHATSAPP SENT] to {MY_WHATSAPP_NUMBER}")
        time.sleep(8)
        driver.quit()

    except Exception as e:
        print(f"❌ [WHATSAPP ERROR] {e}")
        if driver:
            try: driver.quit()
            except: pass

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"- [{datetime.now().strftime('%H:%M:%S')}] 📲 WHATSAPP SENT: {message_body[:40]}...\n")

if __name__ == "__main__":
    send_whatsapp_alert("✅ System Integration Test: Live WhatsApp Alert Working!")
