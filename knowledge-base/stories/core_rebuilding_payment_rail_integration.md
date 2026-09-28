---
tags: core
signals: Ownership, Scope, Perseverance, Ambiguity, Communication, Leadership, Growth
---

# Payment Rail Integration Rebuild
## Solvex Pay - Senior Software Engineer, Money Movement Team

### Context
We ran into a crisis when one of our third-party providers, Continental Settlement Network, terminated their contract, and we suddenly lost the ability to send or receive cross-border payments through that rail. This was a direct hit to our customers and a major gap in our "premium" payments product. Once we signed a new provider, I led the backend implementation to recover that capability. It was a messy integration from the start: the provider's sandbox was half-broken (we could send orders but never see them finish), the API documentation was outdated and didn't match the actual responses, and we eventually discovered that some countries, like the UAE, required extra "hidden" fields that weren't documented at all.

### Stakeholders
- Customers (lost cross-border payment capability)
- Third-party provider (new integration partner)
- Money Movement Team (my team building the integration)

### Table of content
Led the implementation to restore cross-border payment capabilities after losing our provider. Ramped up fast on the payment-rail domain, built a mock webhook simulator in staging to bypass a broken sandbox, collaborated cross-functionally on UI and API contracts, managed a safe rollout via feature flags, deployed a targeted country-list hotfix in production, and presented the architecture at a company-wide All-Hands.

### Actions
1. Since my background was mostly in consumer fintech, I ramped up on the payment-rail domain incredibly fast by doing a deep dive into the codebase and partnering with the domain experts on the team to get my bearings.
2. I initially started the implementation relying only on unit tests because our provider took some time to provide us access to their sandbox environment.
3. To keep the project moving despite the broken sandbox, I built a custom simulation service in our staging environment so we could mimic webhook events and test the full flow ourselves.
4. I worked closely with the mobile and design teams to nail down the UX and API contracts so the frontend and backend stayed in sync.
5. I implemented the whole thing using feature flags so we could do a gradual rollout and kill it quickly if things go wrong.
6. When that undocumented UAE field issue popped up in production, I used our "allowed countries" list to quickly toggle off the affected regions while I coded a hotfix.
7. During the process, I spotted an opportunity to optimize our internal ledger calls and consolidated two separate API requests into one, and I represented the team by presenting our solution at a company-wide All-Hands.

### Result and impact
- We shipped the feature in just two months, restoring a core capability of our product, and we saw about 200 successful transactions in the first few weeks after launch.
- Beyond just fixing the problem, we delivered a more resilient system that gave the Treasury team exactly what they needed to keep payments running smoothly.
- The ledger-call optimization consolidated two API requests into one, cutting downstream load on every transaction.

### Learnings
- Defensive programming is non-negotiable when you're integrating with third-party APIs; you have to assume they'll fail or miss events, and I learned not to trust webhooks blindly — always build a polling mechanism as a backup, which I've carried into every external integration since.
- Be the "squeaky wheel" — when you're blocked by a partner or a vague API, persistence is the only way to keep a project on schedule, and following up constantly via Slack and weekly meetings became my default for partner-dependent work.
- Cross-functional sync is key; a project like this isn't just code — it's legal, UX, mobile, and security, and success depends entirely on how well you collaborate across those different "languages" to deliver a single product.

### Signal areas
- **Ownership**: Followed up and unblocked issues across the partner and internal teams to keep the integration moving.
- **Scope**: Delivered significant business value by restoring a core product capability and optimizing internal ledger calls.
- **Perseverance**: Built extra tooling (the mock simulator) to work around a broken sandbox rather than waiting for the partner to fix it.
- **Communication**: Collaborated with mobile and design teams and presented the solution to the entire company at an All-Hands.
- **Leadership**: Led the backend integration of the new provider and represented the team at the All-Hands.
- **Ambiguity**: Navigated a half-broken sandbox, outdated documentation, and undocumented production requirements with incomplete information.
- **Growth**: Ramped up quickly on the unfamiliar payment-rail domain from a consumer-fintech background.
