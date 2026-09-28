---
tags: supporting
signals: Ownership, Perseverance, Communication
---

# Recovering payments flow delivery
## Solvex Pay - Senior Software Engineer, Money Movement Team

### Context
A corporate payments flow I was responsible for fell about three weeks behind schedule after an upstream dependency changed its API contract without notice, breaking a chunk of our integration tests right before a planned release. The delay put a customer-facing launch date at risk.

### Stakeholders
- Product Team (owned the launch date and customer commitment)
- Upstream Team (owned the API that changed)
- Money Movement Team (delivering the flow)

### Table of content
Recovered a delayed payments flow delivery after an unannounced upstream API change, by triaging the actual blast radius first, negotiating a scoped interim fix with the upstream team, and communicating a revised, credible timeline to Product early rather than late.

### Actions
1. Triaged the breakage first to understand the actual blast radius — only two of the flow's six steps were affected, not the whole feature as it first appeared.
2. Reached out directly to the upstream team's tech lead instead of just filing a ticket, and negotiated a temporary compatibility shim on their side while we adapted our integration properly.
3. Re-scoped the remaining work into a smaller, shippable core plus a fast-follow, instead of trying to deliver the original full scope on the original date.
4. Communicated the revised timeline and scope to Product as soon as I had a credible estimate, rather than waiting until the original deadline had already passed.
5. Added a contract test against the upstream API so a future silent change would fail fast in CI instead of surfacing right before a release.

### Result and impact
- Shipped the re-scoped core flow only one week late instead of the three weeks it looked like initially, with the fast-follow landing two weeks after that.
- Product was able to communicate a single, credible revised date to the customer instead of repeated slips.
- The new contract test caught a second silent upstream change months later before it reached production.

### Learnings
- The first triage after a delay-causing surprise should be about actual blast radius, not the worst-case assumption — it usually opens up options you didn't see at first.
- Surfacing a revised timeline early, even when it's bad news, is always better received than a deadline that quietly slips.
- A contract test against an external dependency is cheap insurance against exactly this kind of surprise happening twice.

### Signal areas
- **Ownership**: Took charge of the recovery plan and the customer-facing timeline commitment.
- **Perseverance**: Worked through an unexpected external blocker to still deliver close to the original date.
- **Communication**: Negotiated directly with the upstream team and gave Product an early, credible revised estimate instead of a late surprise.
