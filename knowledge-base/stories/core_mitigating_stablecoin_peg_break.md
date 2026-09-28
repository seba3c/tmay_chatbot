---
tags: core
signals: Ownership, Scope, Ambiguity, Communication, Leadership, Perseverance
---

# Mitigating a Stablecoin Peg Break
## Solvex Pay - Senior Software Engineer, Money Movement Team

### Context
In 2023, NovaUSD — the stablecoin our settlement flows relied on for cross-border transfers — briefly broke its peg after its issuer, Nova Reserve, disclosed exposure to a failing banking partner. Within hours, the coin dropped several cents below par, and our customers held meaningful balances denominated in it. I was the on-call engineer when the alerts started firing, and I ended up leading our technical response for the following 48 hours.

### Stakeholders
- Customers (holding NovaUSD balances during the peg break)
- Treasury Team (managing exposure and hedging decisions)
- Risk and Compliance (assessing customer-communication obligations)
- Money Movement Team (my team, owning the settlement pipeline)

### Table of content
Led the incident response to a stablecoin de-peg event, building an emergency circuit-breaker to pause new NovaUSD settlements, working with Treasury on a fair internal conversion rate for affected transactions, and driving the post-incident redesign that added a second stablecoin rail as a fallback.

### Actions
1. As soon as the alerts fired, I paged Treasury and Risk and set up a dedicated incident channel to keep everyone synced in real time.
2. I built and shipped an emergency circuit-breaker within the first two hours, pausing new NovaUSD-denominated settlements while keeping withdrawals of existing balances available.
3. I worked with Treasury to define a fair internal conversion rate for in-flight transactions, so customers weren't penalized for a de-peg that happened mid-transfer.
4. I wrote a script to reconcile every affected transaction against the ledger, flagging discrepancies for manual review by Risk and Compliance.
5. Once NovaUSD re-pegged about 30 hours later, I led the phased re-enablement of settlements, starting with a small allow-list of low-risk corridors.
6. In the post-incident review, I proposed and then implemented a second stablecoin rail as a fallback, so a single issuer's problems could never again fully halt settlements.

### Result and impact
- We contained customer impact to a small, clearly identified set of in-flight transactions, all reconciled and made whole within a week.
- The circuit-breaker mechanism became a standing piece of infrastructure, since reused for two smaller incidents unrelated to stablecoins.
- The second settlement rail cut our single-issuer concentration risk in half and became a company-wide talking point in the next board update.

### Learnings
- Speed matters more than perfection in the first hour of an incident; a rough circuit-breaker that stops the bleeding beats a perfect fix that ships too late.
- Incidents involving customer funds need Risk and Compliance in the room from minute one, not after the fact — decisions about conversion rates and communication have to be made jointly.
- Single-vendor dependencies in a payments stack are a standing risk, not just a theoretical one; the fallback rail should have existed before the incident, not after.

### Signal areas
- **Ownership**: Took charge of the incident from the first alert through the post-incident architecture change.
- **Scope**: The fix and the follow-up redesign reduced company-wide concentration risk, not just the immediate symptom.
- **Ambiguity**: Made real-time decisions about conversion rates and rollout scope with incomplete information during a live incident.
- **Communication**: Kept Treasury, Risk, and Compliance aligned in real time during a fast-moving, high-stakes event.
- **Leadership**: Directed the technical response and drove the follow-up architecture change through to implementation.
- **Perseverance**: Stayed engaged through a 48-hour incident window, from firefighting to fair resolution to structural fix.
