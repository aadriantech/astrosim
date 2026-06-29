"""Run canonical scenario suite and aggregate results."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from astrosim.scenario import load_and_build, load_scenario

CANONICAL_SCENARIOS = (
    "lunar_base.yaml",
    "mars_habitat.yaml",
    "orbital_station.yaml",
    "deep_space_transit.yaml",
    "greenhouse_lunar.yaml",
    "greenhouse_mars.yaml",
    "mars_closed_loop.yaml",
    "orbital_greenhouse.yaml",
)


@dataclass
class SuiteRow:
    scenario_name: str
    scenario_path: str
    energy_net_kwh: float | None
    mass_net_import_kg: float | None
    mission_success_probability: float | None
    error: str | None = None


@dataclass
class SuiteResult:
    rows: list[SuiteRow] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _run_one(path: Path) -> SuiteRow:
    try:
        config = load_scenario(path)
        sim_result = load_and_build(path).run()
        energy = sim_result.energy_budget.net_kwh if sim_result.energy_budget else None
        mass = sim_result.mass_budget.net_import_kg if sim_result.mass_budget else None
        reliability = (
            sim_result.reliability_budget.mission_success_probability
            if sim_result.reliability_budget
            else None
        )
        return SuiteRow(
            scenario_name=config.name,
            scenario_path=str(path),
            energy_net_kwh=energy,
            mass_net_import_kg=mass,
            mission_success_probability=reliability,
        )
    except Exception as exc:  # noqa: BLE001
        return SuiteRow(
            scenario_name=path.name,
            scenario_path=str(path),
            energy_net_kwh=None,
            mass_net_import_kg=None,
            mission_success_probability=None,
            error=str(exc),
        )


def run_scenario_suite(
    scenarios_dir: str | Path,
    *,
    names: tuple[str, ...] = CANONICAL_SCENARIOS,
    parallel: bool = False,
    max_workers: int | None = None,
) -> SuiteResult:
    root = Path(scenarios_dir)
    paths = [root / name for name in names]
    result = SuiteResult()

    if parallel and len(paths) > 1:
        workers = max_workers or min(len(paths), 4)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(_run_one, path): path for path in paths}
            for future in as_completed(futures):
                row = future.result()
                if row.error:
                    result.errors.append(f"{row.scenario_path}: {row.error}")
                result.rows.append(row)
    else:
        for path in paths:
            row = _run_one(path)
            if row.error:
                result.errors.append(f"{row.scenario_path}: {row.error}")
            result.rows.append(row)

    return result


def export_suite_json(result: SuiteResult, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "scenarios": [
            {
                "scenario_name": row.scenario_name,
                "scenario_path": row.scenario_path,
                "energy_net_kwh": row.energy_net_kwh,
                "mass_net_import_kg": row.mass_net_import_kg,
                "mission_success_probability": row.mission_success_probability,
                "error": row.error,
            }
            for row in result.rows
        ],
        "errors": result.errors,
    }
    output.write_text(json.dumps(payload, indent=2))
    return output