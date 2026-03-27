# 🎥 Kiran's Hackathon Demo Script
**Project:** Digital FTE (Full-Time AI Employee) - Platinum Tier
**Goal Length:** 3-5 Minutes

---

### **Step 1: Introduction (30 seconds)**
- **Screen:** Open VS Code showing your `README.md` or Open Obsidian `Dashboard.md`.
- **Speak:** "Hi everyone, my name is Kiran Naseer, and this is my Digital FTE. It is a Platinum-Tier, fully autonomous, local-first AI Employee. It monitors my Gmail, Upwork, and social media without me ever touching the browser, and stores all its memory locally in Obsidian using Markdown files."

### **Step 2: Architecture & Security (30 seconds)**
- **Screen:** Show the `.claude/skills` folder and `.env.example`.
- **Speak:** "I designed this with strict B2B security in mind. As you can see in my `.gitignore` and `.env.example`, no API keys, Gemini tokens, or WhatsApp numbers are ever pushed to GitHub. The AI's reasoning is separated into specific 'Skills' in the `.claude` directory, like accounting and social media."

### **Step 3: Live Demo 1 - The Autonomous Gmail Agent (1.5 Minutes)** 
- **Screen:** Split your screen. Keep your Email Inbox on one side, and the VS Code Terminal on the other side.
- **Action:** Run the command `python watchers/gmail/gmail_oauth_agent.py`
- **Speak:** "First, let's see the Perception layer working. My Gmail agent uses Google OAuth 2.0 to securely read emails. I'm going to send a test inquiry to my email right now..."
- **Action:** Send an email from your phone to your project email. Watch the terminal catch the email, say "AI Processor Initialized," and send a fully autonomous reply back without you clicking anything.
- **Speak:** "As you can see, the AI used Gemini to triage the email, decided it was a real inquiry (not spam), and auto-replied directly via the Gmail API, all while logging it to my Obsidian `/Needs_Action` folder."

### **Step 4: Live Demo 2 - The Freelance WhatsApp Bridge (1 Minute)**
- **Screen:** Show the terminal and prepare your WhatsApp Web tab.
- **Action:** Press `Ctrl+C` to stop the Gmail agent, then run `python watchers/freelance_watcher.py`
- **Speak:** "Next, my employee also hunts for clients. The Freelance Watcher constantly monitors RSS feeds for high-value jobs. Let's see it in action."
- **Action:** Let the script run. It will instantly detect the simulated $1,500 job and pop open your WhatsApp Web to send you a real-time mobile alert.
- **Speak:** "This means even if I am away from my laptop, my AI employee finds a job, drafts a proposal in Obsidian, and buzzes my phone via WhatsApp."

### **Step 5: Live Demo 3 - LinkedIn Auto Poster & Conclusion (30 seconds)**
- **Screen:** Show the terminal.
- **Action:** Run `python watchers/linkedin_poster.py`. DON'T touch the mouse!
- **Speak:** "Finally, for the execution layer, my AI can post to social media. Running the LinkedIn poster acts as our fallback automation to pre-fill and publish posts generated from my AI Plans."
- **Speak (Final):** "In conclusion, this Digital FTE seamlessly connects Perception (Watchers), Reasoning (Gemini/Claude), and Action (WhatsApp/Emails), fully protecting my data locally. Thank you!"

---
**Tips before recording:**
- Keep WhatsApp Web strictly logged in on your default browser.
- Have a second device (like your phone) ready to send an email to yourself during the Gmail test.
- Speak confidently! You've built an incredible system.
