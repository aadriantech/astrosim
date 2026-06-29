---
name: aysu-verify
description: >
  AYSU ("Are You Sure?") verification gate for AstroSim. Mandatory before declaring
  any task done. Triggers: "/aysu-verify", "are you sure", "mark complete".
metadata:
  short-description: "AYSU — self-verify before ship"
---

# AYSU Verify Skill

## Preconditions

- T2+: `reviews/<task-id>.md` with `recommendation: approve`
- `pytest tests/ -q` green

## Steps

1. Re-read plan acceptance criteria line by line.
2. Confirm each criterion has evidence (test name or doc).
3. Fill mandatory block:

```
AYSU:
  confidence: high | medium | low
  task_class: T0 | T1 | T2 | T3
  verified:
    - [ ] Plan acceptance criteria met
    - [ ] pytest green
    - [ ] Critic approve (if T2+)
    - [ ] Section AGENT.md synced (if behavior changed)
  residual_risks: <list or none>
  loop_back: yes | no
```

4. **confidence: high** only if all verified boxes checked and no known doubts.
5. If medium/low or `loop_back: yes` → return to implementer; do not declare done.

## Must not

- Declare done without printing AYSU block
- Set high confidence with failing tests or open critic findings

## Output

AYSU block + ship/no-ship decision.