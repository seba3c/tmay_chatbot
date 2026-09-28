---
tags: core
signals: Ownership, Scope, Communication, Leadership, Growth
---

# Hedging Engine Multi-Venue Migration
## Solvex Pay - Senior Software Engineer, Money Movement Team

### Context
Our BTC hedging engine was hardcoded against a single venue, Kortex Exchange — a major single point of failure for the business, since any Kortex outage or rate-limit meant Treasury couldn't hedge exposure at all. The Treasury team wanted to route through multiple venues for better liquidity and pricing, and the Crypto team, who owned the hedging engine, was underwater with other priorities. I stepped in to lead the migration as a guest contributor in their codebase.

### Stakeholders
- Treasury Team (wanted multi-venue liquidity and pricing)
- Crypto Team (owned the hedging engine, under-resourced)
- Money Movement Team (my home team)

### Table of content
Led the transition of the BTC hedging engine off a single hardcoded venue into a pluggable, venue-agnostic architecture, working as a guest engineer in another team's mission-critical repo, going heavy on tests because the system handled live treasury funds, and leaving behind a template later adopted for the second venue integration (Meridian OTC).

### Actions
1. Mapped every Kortex-specific dependency in the hedging engine before writing a single line of new code, so I understood the full blast radius of the change.
2. Designed a common venue interface so the core hedging logic didn't care which exchange or OTC desk sat behind it.
3. Since I was a guest in the Crypto team's mission-critical repo, I over-communicated constantly and went heavy on unit tests — the service handled live treasury funds with zero room for error.
4. Rolled out the refactor behind a feature flag, first shadow-running the new abstraction against Kortex before cutting traffic over.
5. Partnered with the Crypto team to onboard Meridian OTC as the second venue, using the new interface as the template.
6. Documented the abstraction and presented it to the Crypto team so they could extend it to future venues without me.

### Result and impact
- The abstraction became the standard template for all future venue integrations, and the Crypto team liked the work enough to request a permanent transfer.
- Removed a major single point of failure for Treasury, who could now route hedges to whichever venue offered better liquidity or pricing at any given moment.
- Zero incidents during the migration itself, despite touching a system handling live treasury funds throughout.

### Learnings
- Design against an interface, not an implementation, whenever the business direction on "which provider" is still likely to change — it turns the next integration into a plug-and-play task instead of another refactor.
- When you're a guest in someone else's mission-critical repo, trust is earned through rigor — tests, documentation, and communication — not through velocity alone.
- Shadow-running a new path against the old one before cutting over is worth the extra step whenever the blast radius involves live funds.

### Signal areas
- **Ownership**: Took full responsibility for a migration in a codebase I didn't own, from design through rollout.
- **Scope**: Removed a company-wide single point of failure and left behind a reusable pattern for future integrations.
- **Communication**: Acted as the main point of contact across Treasury, Crypto, and my own team throughout the migration.
- **Leadership**: Led the technical direction of the migration despite having no formal authority over the codebase.
- **Growth**: Built enough trust and technical credibility to be offered a permanent transfer to the team whose code I was touching.
