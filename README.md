# 🤖 Project: Digital FTE (The Autonomous AI Employee)
> **Tier:** Platinum (Hybrid Cloud + Local) | **Project ID:** AF-2026-FTE

Welcome to the future of work. This project transforms **Claude Code** into a proactive, autonomous business manager that handles leads, social media, finance, and strategy with **Human-in-the-Loop (HITL)** safety.

---

## 🏗 System Architecture
The system follows a **Perception-Reasoning-Action** loop, split across two domains:

### 1. ☁️ Perception & Reasoning (The Cloud Brain)
- **Watchers:** 24/7 scripts monitoring Gmail, LinkedIn, and X (Twitter) for sales keywords (e.g., "AUTOPILOT").
- **Triage:** Automatically categorizes leads by potential value ($).
- **Drafting:** Uses `Profile.md` and `Strategic_Rules.md` to draft personalized replies in `Needs_Action`.

### 2. 🏠 Action & Safety (The Local Hands)
- **Execution Engine:** Monitors the `/Approved` folder. Once a human moves a draft to this folder, the engine executes the action (Email/LinkedIn Post/Odoo Billing).
- **Privacy Shield:** Sensitive tokens (WhatsApp sessions, Bank APIs) stay on the local PC and are NEVER synced to the cloud via `.gitignore` policies.

### 3. 🧠 The "Managing Director" Layer (Gold/Platinum)
- **Audit Engine:** Generates weekly "Monday Morning CEO Briefings" analyzing revenue, bottlenecks, and efficiency velocity.
- **Strategic MD:** Automatically detects "Ghosting" (clients not replying) and drafts follow-ups autonomously.

---

## 🥈 Tier Breakdown
- **Bronze:** Essential Vault setup, Identity definition, and Templates.
- **Silver:** LinkedIn Auto-Post, Gmail Priority Watchers, and the Execution Engine.
- **Gold:** Odoo Accounting Integration, CEO Briefing Engine, and Profitability Analysis.
- **Platinum:** 24/7 Hybrid Sync (Cloud perception vs Local execution).

---

## 🛠 Tech Stack
- **Engine:** Claude Code
- **Interface:** Obsidian (Markdown-based Local-First Data)
- **Automation:** Python Watchers & JSON-RPC (Odoo)
- **Sync:** Git Hybrid Model

---
*Created with ❤️ for the Personal AI Employee Hackathon 2026.*
