# Decisions

Why the project is the way it is. **Append-only**: never edit or delete an
entry's content. The only in-place edit is its **Status** line. To change a
decision, append a new one that supersedes it, and update the old one's status.

Statuses: `Accepted` · `Provisional (Q-NNN)` · `Superseded by D-NNN` ·
`Accepted; part changed by D-NNN` · `Accepted; done YYYY-MM-DD`.

## Index

| ID | Date | Decision | Status |
|---|---|---|---|
| [D-001](#d-001-project-structure) | YYYY-MM-DD | Project structure | Accepted |

---

### D-001 Project structure

- **Date:** YYYY-MM-DD
- **Status:** Accepted
- **Decision:** <The parts set up for this project, in a few lines: docs
  modules, skills, agents, limits, version control.>
- **Why:** <The project profile answers that drove it.>

  <Paste the project profile block from the purpose grill.>
- **Left out:** <Modules not created, and the growth trigger that would add each.>
- **Revisit if:** <The concrete observation that would reopen it, e.g. "an agent
  starts working unattended", "a second person joins", "sessions keep skipping
  the end routine".>

<!--
Entry shape for later decisions:

### D-NNN Title

- **Date:** YYYY-MM-DD
- **Status:** Accepted
- **Decision:** what was chosen
- **Alternatives:** what else was considered, and why not
- **Why:** the reasoning and evidence (verified / owner-stated / inferred)
- **Consequences:** what this forces downstream
- **Revisit if:** the concrete observation that would reopen it
-->
