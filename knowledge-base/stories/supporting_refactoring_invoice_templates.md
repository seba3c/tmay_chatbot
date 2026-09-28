---
tags: supporting
signals: Ownership, Scope, Communication
---

# Implementing a new invoice design for corporate transactions
## Solvex Pay - Senior Software Engineer, Money Movement Team

### Context
We had a steady stream of customer complaints about transaction invoices, and the EUR withdrawal invoice kept coming back with formatting issues. The easy fix was patching the missing data, but the real problem was structural: every invoice type shared one template stuffed with conditional logic, rendered through PageForge, so touching one flow risked breaking another.

### Stakeholders
- Customers (receiving broken or confusing invoices)
- Support Team (fielding the complaints)
- Money Movement Team (owned the invoice pipeline)

### Table of content
Rebuilt transaction invoices from one tangled shared template into a per-transaction-type design, upgrading the rendering library and rolling out incrementally behind a fallback so no flow was frozen during the migration.

### Actions
1. Diagnosed the root cause first instead of just patching the reported bug — every invoice type shared one template with nested conditionals, so a fix for one type risked regressing another.
2. Designed a per-transaction-type template architecture, so each invoice type owned its own layout instead of sharing conditional logic.
3. Upgraded the PageForge rendering version as part of the migration, since the old version had known layout bugs under certain locales.
4. Added a fallback branch that checked the transaction type — if the new template was ready, it used it; otherwise it fell back to the old shared template.
5. Rolled out the new design one transaction type at a time, starting with the highest-complaint type (EUR withdrawals), without freezing the rest of the invoice types.
6. Stayed in sync with the designer throughout so the new templates matched the updated visual language.

### Result and impact
- Complaints on the migrated invoice types dropped sharply after each rollout stage.
- Other teams could now update their own invoice types independently on the same framework, without touching the shared conditional mess.
- The design was later adopted as the base template for a new corporate-client product.

### Learnings
- The reported bug is often a symptom; when every fix risks a regression elsewhere, the shared structure itself is usually the real problem.
- Incremental, type-by-type rollout behind a fallback lets you ship real value without freezing everything else in flight.

### Signal areas
- **Ownership**: Diagnosed and fixed the structural root cause instead of just patching the reported symptom.
- **Scope**: Delivered a reusable framework that unblocked other teams, not just a fix for the original complaint.
- **Communication**: Stayed in sync with the designer and rolled out incrementally to avoid disrupting other flows.
