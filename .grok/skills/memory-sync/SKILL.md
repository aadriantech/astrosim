---
name: memory-sync
description: >
  Sync section AGENT.md files and AGENT_INDEX after behavior or API changes.
  Triggers: "/memory-sync", end of T2+ task, before release tag.
metadata:
  short-description: "Sync distributed agent memory"
---

# Memory Sync Skill

## When

- Public interface or gotcha changed in `src/`
- New domain directory added
- Release tag

## Steps

1. Identify affected AGENT_INDEX ID(s).
2. Update section AGENT.md: §Gotchas, §Verification status, `Last verified` + commit sha.
3. Do **not** duplicate contracts — link `contracts/` instead.
4. Update AGENT_INDEX `Last synced` date if domains added/removed.
5. Run `scripts/check_agent_sync.sh`.

## Rules

- Mark unconfirmed claims `UNVERIFIED`
- Keep each section file ≤80 lines; overflow → docs/ARCHITECTURE.md