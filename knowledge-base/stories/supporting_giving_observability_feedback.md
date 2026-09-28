---
tags: supporting
signals: Communication, Growth, Leadership
---

# Give feedback: observability instead of print statements
## Solvex Pay - Senior Software Engineer, Money Movement Team

### Context
I saw a junior teammate visibly struggling, drowning in scattered `print` statements trying to track down a production bug. He didn't have structured logging habits yet, and the debugging session was dragging on far longer than it needed to.

### Stakeholders
- Junior teammate (being coached)
- Money Movement Team (benefited from better debugging practices spreading)

### Table of content
Coached a junior teammate out of print-statement debugging and into structured logging with LogFerry, explaining the reasoning rather than just the command, then followed up weeks later to confirm the habit stuck.

### Actions
1. Pulled up a chair instead of just telling him to "use logging" — I wanted to understand what he was actually trying to track down first.
2. Walked him through log levels (debug, info, warning, error) and message formatting, explaining why each mattered for someone reading the logs later, not just for him in the moment.
3. Showed him how to search and filter structured logs in LogFerry so he could see the payoff immediately, compared to scrolling through print output in a terminal.
4. Left him to apply it himself on the rest of the bug rather than finishing it for him.
5. Checked back in a few weeks later, casually, to see if the habit had stuck.

### Result and impact
- He told me he'd dropped print-statement debugging entirely and was using structured logging by default.
- The specific log-level convention we used became something he later taught to the next new hire.

### Learnings
- Explaining the "why" behind a practice makes it generalize; handing someone a command ("don't use print") only fixes the one instance.
- A short follow-up weeks later is what turns a one-off correction into a habit — and it shows the person you were genuinely invested, not just correcting them in the moment.

### Signal areas
- **Communication**: Coached through explanation and reasoning rather than instruction.
- **Growth**: Focused on making the lesson generalize beyond the one bug.
- **Leadership**: Took the informal coaching initiative without being asked.
