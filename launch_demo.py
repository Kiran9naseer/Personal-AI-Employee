import subprocess
import time
import os

# ============================================================
# 🚀 DIGITAL FTE - MASTER DEMO LAUNCHER (AUTO-POSITIONED)
# Opens each script in its own window at a screen quadrant
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Each script with its screen position (x, y, width, height)
# Assumes 1920x1080 screen - adjust if needed
SCRIPTS = [
    ("Approval Bridge",        "watchers/approval_bridge.py",            0,    0,   960, 540),
    ("LinkedIn Poster",        "watchers/linkedin_poster.py",            960,  0,   960, 540),
    ("Gmail AI Agent",         "watchers/gmail/gmail_oauth_agent.py",    0,    540, 960, 540),
    ("Facebook Poster",        "watchers/facebook_selenium_poster.py",   960,  540, 960, 540),
]

DELAY = 10  # seconds between each launch

def launch_positioned(title, script, x, y, w, h):
    full_path = os.path.join(BASE_DIR, script)
    # Open in new CMD window, then PowerShell will reposition it
    cmd = f'start "{title}" cmd /k "cd /d {BASE_DIR} && python "{full_path}""'
    subprocess.Popen(cmd, shell=True, cwd=BASE_DIR)
    time.sleep(2) # Give window time to open
    
    # PowerShell to find and move the window by title
    ps_cmd = f"""
    Add-Type @"
    using System; using System.Runtime.InteropServices;
    public class Win {{
        [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int h, bool r);
        [DllImport("user32.dll")] public static extern IntPtr FindWindow(string c, string t);
    }}
"@
    $hwnd = [Win]::FindWindow($null, "{title}")
    [Win]::MoveWindow($hwnd, {x}, {y}, {w}, {h}, $true)
    """
    subprocess.Popen(["powershell", "-Command", ps_cmd], shell=False)
    print(f"✅ Launched & Positioned: {title}")

if __name__ == "__main__":
    print("=" * 52)
    print("🤖 DIGITAL FTE - MASTER DEMO LAUNCHER")
    print("=" * 52)
    print(f"📋 {len(SCRIPTS)} scripts → 4 screen quadrants\n")

    for title, script, x, y, w, h in SCRIPTS:
        launch_positioned(title, script, x, y, w, h)
        if (title, script, x, y, w, h) != SCRIPTS[-1]:
            print(f"⏳ Next script in {DELAY}s...")
            time.sleep(DELAY)

    print("\n🎉 All 4 watchers launched in their quadrants!")
    print("📽️  Arrange & Start your screen recording now.")
