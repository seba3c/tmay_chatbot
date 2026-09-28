---
tags: core
signals: Ownership, Leadership, Communication, Perseverance
---

# Leading the Security Alert Remediation
## Solvex Pay - Senior Software Engineer, Money Movement Team

### Context
Our team had a growing backlog of dependency-vulnerability alerts from ShieldScan, our security scanning tool, and we were under SLA pressure from the security org to close them out. The backlog kept losing to feature work every sprint — nobody had explicitly taken ownership of it, and it was becoming a compliance risk. I took charge of clearing it.

### Stakeholders
- Security Team (set the SLA and tracked company-wide compliance)
- Product Owner and Tech Lead (owned sprint capacity)
- Money Movement Team (my team, doing the remediation work)

### Table of content
Took ownership of an unowned security vulnerability backlog, baked remediation into the sprint cadence with dedicated capacity, used a data-backed nudge to rally the team when fixes stalled mid-sprint, and drove the backlog to zero while ranking top 3 company-wide.

### Actions
1. Partnered with the product owner and tech lead during sprint planning to allocate dedicated tech-debt capacity each sprint, so remediation stopped competing directly with feature work.
2. Before each sprint, I checked the ShieldScan dashboard and sorted alerts by severity and SLA proximity, turning the backlog into an ordered list of sprint tickets.
3. When fixes stalled mid-sprint behind feature work, instead of nagging I posted in Slack that we were top 3 in the company for remediation speed and dared the team to keep the streak.
4. Periodically cleaned the backlog together with the security team, dropping alerts that were already fixed elsewhere or misassigned to us, so the visible number reflected real outstanding work.
5. Reported our SLA compliance and ranking back to the team and to leadership, reinforcing the behavior and securing continued sprint capacity for it.

### Result and impact
- Cleared the entire backlog and held a zero SLA-breach rate for the rest of the year, ranking top 3 company-wide in remediation speed.
- The dedicated-capacity pattern was adopted by two other teams after our tech lead presented it at a leads sync.
- Freed up the security team to focus on proactive work instead of chasing teams for overdue fixes.

### Learnings
- Ongoing, structural work like security debt needs a permanent slot in the team's cadence, not a one-time cleanup — otherwise it just refills.
- A data-backed nudge (a ranking, a streak) motivates a team more effectively than repeated reminders, especially for unglamorous work nobody owns.
- Periodically pruning a backlog against reality (not just closing tickets) keeps the visible number honest and the team's morale intact.

### Signal areas
- **Ownership**: Took charge of a backlog nobody had explicitly owned and drove it to zero.
- **Leadership**: Led without formal authority, by baking the behavior into process and motivating the team with data rather than mandates.
- **Communication**: Reported progress and ranking to the team and leadership, and helped the pattern spread to other teams.
- **Perseverance**: Sustained the cadence over multiple sprints until the backlog was fully cleared, not just reduced.
