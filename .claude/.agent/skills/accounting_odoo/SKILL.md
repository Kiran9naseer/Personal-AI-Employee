---
name: accounting_odoo
description: Handles financial operations using Odoo Community JSON-RPC APIs.
---

# 💰 Accounting & Odoo Skill
This skill enables the Digital FTE to manage invoices, tracked payments, and financial reporting.

## 🛠 Capabilities
1. **Invoice Drafting:** Automatically create draft invoices in Odoo when a deal is approved.
2. **Revenue Tracking:** Fetch real-time financial data from Odoo for the `CEO_Briefing`.
3. **Audit Readiness:** Maintain a local Markdown mirror of Odoo transactions in `/Accounting`.

## 📂 Workflow
1. **Trigger:** Human Approves a `PLAN.md` with an invoice step.
2. **Action:** Call `watchers/odoo_integration.py` to create a record in Odoo.
3. **Verification:** Save the Odoo Invoice ID back to the `/Finance` folder.
4. **Report:** Update `Dashboard.md` with the new balance.

## 🛑 Safety Rules
- AI cannot **Post** (Finalize) an invoice without human review.
- High-value payments (> $500) must be flagged for Kiran Naseer.
