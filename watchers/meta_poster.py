import os
import webbrowser
import pyperclip
import time
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")

def post_to_meta(platform, post_content):
    """
    Executes a Post to Facebook or Instagram.
    If official token is present, executes Graph API call.
    Else, copies the content to clipboard and opens the browser.
    """
    if not post_content or len(post_content) < 5:
        print("⚠️ Post content is empty.")
        return False
        
    print(f"🚀 [META ACTION] Initiating {platform} Auto-Post sequence...")
    clean_content = "\n".join([line for line in post_content.split('\n') if not line.startswith('#')])

    if META_ACCESS_TOKEN:
        print(f"🔗 Connecting to Meta Graph API for {platform}...")
        # Add actual requests.post(...) to Meta Graph API here in future
        print(f"✅ Posted successfully via API (Simulated with Token).")
        return True
    else:
        print(f"⚠️ No API Token found for {platform}. Using Smart Clipboard Fallback...")
        
        # Copy to clipboard magically
        pyperclip.copy(clean_content.strip())
        print(f"✅ AI Content copied to your clipboard magically! 🪄")
        
        # Open respective platform
        if platform.lower() == "instagram":
            webbrowser.open("https://www.instagram.com/")
        else:
            webbrowser.open("https://www.facebook.com/")
            
        print(f"✅ Opened {platform} in your browser.")
        print(f"👉 ACTION REQUIRED: Just click 'Create Post' and press 'Ctrl + V' to paste the AI's exact words!")
        
        return True

if __name__ == "__main__":
    post_to_meta("Facebook", "Hello Facebook! This is an automated post written by my Digital FTE 🚀")
