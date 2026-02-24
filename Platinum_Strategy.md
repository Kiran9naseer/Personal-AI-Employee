# ☁️ Platinum Tier Strategy: Hybrid Cloud + Local
> **Status:** Planning Phase
> **Goal:** 24/7 Always-On Operation

## 🌍 CLOUD DOMAIN (Cloud VM - 24/7)
**Ownership:** Perception & Drafting
1. **Email Watcher:** High-priority email detection 24/7.
2. **Social Watcher:** LinkedIn/X/FB engagement monitoring.
3. **Auto-Drafting:** Creating initial replies and plans.
4. **Odoo (Mirror):** Mirroring accounting records.

## 🏠 LOCAL DOMAIN (Kiran's PC)
**Ownership:** Action & Privacy
1. **WhatsApp Session:** All WhatsApp messages must go through local instance.
2. **Payments/Banking:** No banking keys on Cloud.
3. **Final Approvals (HITL):** Moving drafted plans to `/Approved`.
4. **Final Sync:** Merging Cloud updates into the local master vault.

## 🔄 THE SYNC RULE (Claim-by-Move)
- Cloud writes to `/Inbox/Cloud/`.
- Local Agent (Claude) reads from Cloud inbox and merges to `/Needs_Action`.
- First agent to move a file to `/In_Progress` owns it.
- **NEVER SYNC:** `.env`, `tokens.json`, `whatsapp_session.db`.

---
*Strategy aligned with 2026 Production Standards.*
