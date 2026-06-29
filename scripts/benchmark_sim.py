#!/usr/bin/env python3
"""Benchmark one-year lunar simulation wall time (report-only)."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

os.environ.setdefault("MPLBACKEND", "Agg")

from astrosim.engine.state import SimulationConfig  # noqa: E402
from astrosim.engine.simulator import Simulator  # noqa: E402
from astrosim.scenario import load_scenario  # noqa: E402
from astrosim.subsystems import DEFAULT_SUBSYSTEMS  # noqa: E402

WARN_SECONDS = 30.0


def main() -> None:
    config = load_scenario(ROOT / "scenarios" / "lunar_base.yaml")
    year_config = SimulationConfig(
        name=config.name,
        duration_hours=8760,
        timestep_hours=config.timestep_hours,
        crew_count=config.crew_count,
        location=config.location,
        parameters=dict(config.parameters),
        events=config.events,
        subsystems=config.subsystems,
    )

    start = time.perf_counter()
    result = Simulator(year_config, DEFAULT_SUBSYSTEMS).run()
    elapsed = time.perf_counter() - start

    print(f"Benchmark: {len(result.history)} steps in {elapsed:.2f}s")
    if elapsed > WARN_SECONDS:
        print(f"WARN: exceeded soft threshold of {WARN_SECONDS}s")
        sys.exit(0)
    print("OK: within soft threshold")
    sys.exit(0)


if __name__ == "__main__":
    main()