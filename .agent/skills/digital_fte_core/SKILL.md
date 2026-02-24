---
name: digital_fte_core
description: Core reasoning and task management for the Digital FTE system.
---

# Digital FTE Core Skill

This skill defines the operational logic for the Digital FTE (Full-Time Equivalent) agent.

## 📋 Operational Workflow
1. **Perception:** Check `/Inbox` and `/Needs_Action` folders for new `.md` files created by Watchers.
2. **Triaging:** Move raw data from `/Inbox` to `/Needs_Action` and categorize it (Finance, Lead, Support, Admin).
3. **Planning:** For each task in `/Needs_Action`, create a `Plan.md` in the same folder with specific steps.
4. **Execution:**
   - Use MCP servers for external actions.
   - For sensitive actions, wait for the user to move the plan to `/Approved`.
5. **Completion:** Move processed tasks to `/Done` and update `Dashboard.md`.

6. **Gold Tier Audit:**
   - Every Monday (or on demand), run `watchers/audit_engine.py`.
   - Analyze `activity_log.md` and `Finance/` to generate `Briefings/CEO_Briefing_DATE.md`.
   - Compare current results against `Campaign_IDs` to track performance goals.

## 🛠 Rules of Engagement
- Always check `Company_Handbook.md` before taking significant actions.
- **Ralph Wiggum Loop:** If a task fails (e.g., Odoo connection), analyze the error, adjust the plan, and retry.
- **Privacy:** Never sync sensitive banking credentials or API tokens (.env files).

## 📂 Expected Folder Structure
- `/Inbox`, `/Needs_Action`, `/Done`
- `/Approved`: Human-cleared plans.
- `/Briefings`: Weekly CEO Audits.
- `/Accounting`: Local & Odoo financial logs.
- `/Templates`: Standardized documentation.
