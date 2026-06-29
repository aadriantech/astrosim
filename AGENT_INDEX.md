# AGENT_INDEX

> **Read this first** to route context. Load only listed section files.

**Last synced:** 2026-06-28 (Phase 5 complete — all TASKS.md items green)  
**Sync policy:** See [AGENTS.md](AGENTS.md) · run `scripts/check_agent_sync.sh`

| ID | Domain | Path | Load when… |
|----|--------|------|------------|
| ROOT | Operating rules | [AGENTS.md](AGENTS.md) | Every new session |
| PKG | Package surface | [src/astrosim/AGENT.md](src/astrosim/AGENT.md) | Public API, cross-module |
| ENG | Simulation engine | [src/astrosim/engine/AGENT.md](src/astrosim/engine/AGENT.md) | Simulator, state, events, MC |
| SUB | Subsystems | [src/astrosim/subsystems/AGENT.md](src/astrosim/subsystems/AGENT.md) | Power, ECLSS, plugins |
| BUD | Budgeting | [src/astrosim/budgeting/AGENT.md](src/astrosim/budgeting/AGENT.md) | Energy, mass, reliability |
| AI | AI hooks | [src/astrosim/ai/AGENT.md](src/astrosim/ai/AGENT.md) | LLM adapters, insights |
| ANA | Analysis | [src/astrosim/analysis/AGENT.md](src/astrosim/analysis/AGENT.md) | Sensitivity, optimization |
| EXP | Export | [src/astrosim/export/AGENT.md](src/astrosim/export/AGENT.md) | JSON, CSV |
| VIS | Visualization | [src/astrosim/visualization/AGENT.md](src/astrosim/visualization/AGENT.md) | Plots, HTML dashboard |
| SCE | Scenarios | [scenarios/AGENT.md](scenarios/AGENT.md) | YAML/JSON configs |
| TST | Tests | [tests/AGENT.md](tests/AGENT.md) | TDD, coverage, fixtures |
| EXM | Examples | [examples/AGENT.md](examples/AGENT.md) | Demo scripts |
| CIC | CI/CD | [.github/AGENT.md](.github/AGENT.md) | Workflows, PR gates |
| CON | Contracts | [contracts/README.md](contracts/README.md) | Schemas, CDD (secondary) |

## Load combinations

| Work type | Primary | Secondary (max 2) |
|-----------|---------|-------------------|
| Engine change | ENG | TST, CON |
| New subsystem | SUB | TST, CON, BUD |
| Scenario/schema | SCE | CON, TST |
| CLI / entrypoint | PKG | SCE, TST, CIC |
| AI / LLM | AI | TST, CON |
| Release / CI | CIC | TST, ROOT |
| Docs only | ROOT | (section if domain-specific) |