## The Big Three

### Tell me about yourself
Structure the answer around the arc already laid out in `tmay/tmay.md`: **Present → Past → Present → Future**.

- **Open with the Personal Summary** — senior software engineer, 10+ years building backend systems in Python across FinTech and payments platforms serving thousands of customers, comfortable owning messy, high-level problems end-to-end, and these days leaning heavily on AI coding tools like Claude Code as part of that process.
- **Ground it with the Accomplishments** — led the backend rebuild of Solvex Pay's payment-rail integration after suddenly losing the provider overnight, shipping it in two months and restoring cross-border transfers (200+ successful transactions in the first weeks); also led the refactor of the BTC hedging engine from a single hardcoded venue into a pluggable multi-venue architecture, protecting live treasury funds and removing a major single point of failure.
- **Bring it to today with Current Focus** — between roles after Solvex Pay went through a reorganization, and used the time deliberately: completed the AWS Solutions Architect Associate certification, finished a Staff Engineer bootcamp, and moved deeper into AI engineering — following Udemy's "AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents" course and putting it into practice with several labs and demo projects, including this RAG-based chatbot.
- **Close with the Forward-Looking Statement** — excited to bring that FinTech/payments background into an AI-powered platform for sophisticated investors, while continuing to grow toward a technical leadership role.

Optional personal opener, from `tmay/bio.md`: originally from Brazil, currently based in Lisbon, Portugal — a light rapport-building line for a more casual first round.

### Tell me about your favorite project/most impactful project or otherwise a chance to tell one large core story
Top core stories where Scope and Ownership (impact, contribution, scope) are the leading signals:

**Option 1 — Payment Rail Integration Rebuild**
Led the backend recovery of payment-rail capability after Solvex Pay's third-party provider terminated their contract overnight, cutting off the ability to send or receive cross-border transfers. Worked through a half-broken sandbox, outdated documentation, and undocumented country-specific requirements (a hidden UAE field surfaced in production) to ship the integration in two months — restoring a core "premium" product capability with about 200 successful transactions in the first few weeks, plus a ledger-call optimization that cut downstream load on every transaction.

**Option 2 — Hedging Engine Multi-Venue Migration**
Stepped in to lead the transition of Solvex Pay's BTC hedging engine off a single hardcoded venue (Kortex Exchange) — a major single point of failure for the business — into a pluggable, venue-agnostic architecture. Mapped every Kortex-specific dependency, designed a common interface for future venues, and went heavy on unit tests since the service handled live treasury funds with zero room for error. The abstraction became the standard template for all future integrations, and the Crypto team liked the work enough to request a permanent transfer.

### Tell me about a conflict you resolved
Stories whose main topic is conflict resolution:

**Option 1 — Disagreeing on our app release testing approach**
Disagreed with how the team handled post-release app verification — the scope was unclear, the time budget wasn't realistic, and the random task assignment kept disrupting whoever got picked mid-sprint. Raised it once and got no traction; raised it a second time with more emphasis and concrete examples of the inconsistency, which finally got the team to discuss it properly. The team aligned on a clear testing scope and switched to a round-robin assignment so no one was blindsided mid-sprint again.

**Option 2 — Team reassignment**
Disagreed with being reassigned off the Money Movement team during a company reorganization, and was frustrated that no one had asked for input beforehand. Voiced the disagreement and the reasoning directly to the leader, listened to the reasoning behind the decision (best fit given prior experience), and chose to disagree and commit rather than resist. Took extra time to properly close out and hand off work in progress on the old team, then ramped up fast on the new team — delivering features independently within about two weeks.
