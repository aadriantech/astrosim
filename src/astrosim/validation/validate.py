"""Validate simulation results against reference benchmarks."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from astrosim.engine.simulator import SimulationResult
from astrosim.validation.benchmarks import default_benchmarks_path, load_benchmarks


@dataclass
class ValidationCheck:
    name: str
    category: str
    simulated: float | str | None
    reference: str
    status: str
    message: str
    source: str


@dataclass
class ValidationReport:
    scenario_name: str
    checks: list[ValidationCheck]

    @property
    def overall_status(self) -> str:
        statuses = {c.status for c in self.checks}
        if "fail" in statuses:
            return "fail"
        if "warn" in statuses:
            return "warn"
        return "pass"


def _within_tolerance(value: float, target: float, tolerance_pct: float) -> bool:
    if target == 0:
        return value == 0
    return abs(value - target) / abs(target) <= tolerance_pct / 100.0


def _check_parameter_fidelity(
    parameters: dict[str, Any],
    benchmarks: dict[str, Any],
) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []
    consumables = benchmarks.get("eclss_consumables", {})
    source = consumables.get("source", "reference/benchmarks.yaml")
    for name, spec in consumables.get("parameters", {}).items():
        target = float(spec["value"])
        tolerance = float(spec.get("tolerance_pct", 5))
        actual = parameters.get(name)
        if actual is None:
            checks.append(
                ValidationCheck(
                    name=name,
                    category="parameter_fidelity",
                    simulated=None,
                    reference=f"{target} ±{tolerance}%",
                    status="warn",
                    message=f"Parameter '{name}' not set; default may apply at runtime.",
                    source=source,
                )
            )
            continue
        actual_f = float(actual)
        ok = _within_tolerance(actual_f, target, tolerance)
        checks.append(
            ValidationCheck(
                name=name,
                category="parameter_fidelity",
                simulated=actual_f,
                reference=f"{target} ±{tolerance}%",
                status="pass" if ok else "warn",
                message=(
                    f"Scenario parameter matches reference within {tolerance}%."
                    if ok
                    else (
                        f"Parameter {actual_f} differs from BVAD default {target} "
                        f"(±{tolerance}%); scenario may be intentionally tuned."
                    )
                ),
                source=source,
            )
        )
    return checks


def _derived_rate(
    result: SimulationResult,
    metric_key: str,
    param_name: str,
) -> float | None:
    final = result.final_state
    if final is None or result.config.crew_count < 1:
        return None
    consumed = final.metrics.get(metric_key)
    if consumed is None:
        return None
    days = result.config.timestep_hours / 24.0
    if days <= 0:
        return None
    return consumed / result.config.crew_count / days


def _check_derived_rates(result: SimulationResult) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []
    params = result.config.parameters
    mappings = [
        ("derived_o2_kg_per_person_day", "eclss.o2_consumed_kg", "o2_kg_per_person_day"),
        ("derived_water_kg_per_person_day", "eclss.water_consumed_kg", "water_kg_per_person_day"),
        ("derived_food_kg_per_person_day", "eclss.food_consumed_kg", "food_kg_per_person_day"),
    ]
    for check_name, metric_key, param_name in mappings:
        derived = _derived_rate(result, metric_key, param_name)
        expected = params.get(param_name)
        if derived is None or expected is None:
            checks.append(
                ValidationCheck(
                    name=check_name,
                    category="derived_rate",
                    simulated=derived,
                    reference=str(expected) if expected is not None else "n/a",
                    status="warn",
                    message="Could not compute derived consumable rate.",
                    source="AstroSim ECLSS model",
                )
            )
            continue
        expected_f = float(expected)
        ok = _within_tolerance(derived, expected_f, 1.0)
        checks.append(
            ValidationCheck(
                name=check_name,
                category="derived_rate",
                simulated=round(derived, 4),
                reference=str(expected_f),
                status="pass" if ok else "fail",
                message=(
                    "Simulated per-person-day rate matches scenario parameter."
                    if ok
                    else f"Derived {derived:.4f} differs from parameter {expected_f}."
                ),
                source="AstroSim ECLSS model",
            )
        )
    return checks


def _scale_per_year(value: float, duration_hours: float) -> float | None:
    if duration_hours <= 0:
        return None
    return value * (8760.0 / duration_hours)


def _scale_per_crew_year(value: float, duration_hours: float, crew: int) -> float | None:
    if duration_hours <= 0 or crew < 1:
        return None
    return value / crew * (8760.0 / duration_hours)


def _envelope_status(value: float, spec: dict[str, Any]) -> str:
    if "value" in spec:
        target = float(spec["value"])
        tol = float(spec.get("tolerance_pct", 5))
        return "pass" if _within_tolerance(value, target, tol) else "warn"
    low = float(spec.get("min", float("-inf")))
    high = float(spec.get("max", float("inf")))
    if value < low or value > high:
        return "warn"
    return "pass"


def _check_envelope(
    result: SimulationResult,
    envelope: dict[str, Any],
    *,
    scenario_path: str,
) -> list[ValidationCheck]:
    checks: list[ValidationCheck] = []
    source = envelope.get("source", "reference/benchmarks.yaml")
    metrics_spec = envelope.get("metrics", {})
    params = result.config.parameters
    duration = result.config.duration_hours
    crew = result.config.crew_count

    for name, spec in metrics_spec.items():
        if name.endswith("_rate") or name in (
            "o2_kg_per_person_day",
            "water_kg_per_person_day",
            "food_kg_per_person_day",
        ):
            if name.startswith("derived_"):
                continue
            if name in ("o2_kg_per_person_day", "water_kg_per_person_day", "food_kg_per_person_day"):
                metric_map = {
                    "o2_kg_per_person_day": "eclss.o2_consumed_kg",
                    "water_kg_per_person_day": "eclss.water_consumed_kg",
                    "food_kg_per_person_day": "eclss.food_consumed_kg",
                }
                simulated = _derived_rate(result, metric_map[name], name)
            else:
                simulated = float(params.get(name, 0))
        elif name == "mass_net_import_kg_per_crew_year":
            mass = result.mass_budget.net_import_kg if result.mass_budget else 0.0
            simulated = _scale_per_crew_year(mass, duration, crew)
        elif name == "energy_net_kwh_per_year":
            energy = result.energy_budget.net_kwh if result.energy_budget else 0.0
            simulated = _scale_per_year(energy, duration)
        else:
            continue

        if simulated is None:
            checks.append(
                ValidationCheck(
                    name=name,
                    category="envelope",
                    simulated=None,
                    reference=json.dumps(spec),
                    status="warn",
                    message=f"Could not evaluate envelope metric '{name}'.",
                    source=source,
                )
            )
            continue

        status = _envelope_status(simulated, spec)
        ref_str = (
            f"{spec['value']} ±{spec.get('tolerance_pct', 5)}%"
            if "value" in spec
            else f"{spec.get('min', '-inf')}–{spec.get('max', 'inf')}"
        )
        checks.append(
            ValidationCheck(
                name=name,
                category="envelope",
                simulated=round(simulated, 2),
                reference=ref_str,
                status=status,
                message=(
                    f"Within reference envelope for {scenario_path}."
                    if status == "pass"
                    else f"Outside soft envelope for {name} ({simulated:.2f} vs {ref_str})."
                ),
                source=source,
            )
        )
    return checks


def _resolve_envelope(
    benchmarks: dict[str, Any],
    scenario_path: str | None,
    config_name: str,
) -> dict[str, Any] | None:
    envelopes = benchmarks.get("scenario_envelopes", {})
    if scenario_path:
        stem = Path(scenario_path).name
        for envelope in envelopes.values():
            if Path(envelope.get("scenario", "")).name == stem:
                return envelope
    key = config_name.replace(" ", "_").lower()
    if key in envelopes:
        return envelopes[key]
    for envelope in envelopes.values():
        if Path(envelope.get("scenario", "")).stem.replace("_", " ") in config_name.lower():
            return envelope
    if "orbital_station" in key or "orbital station" in config_name.lower():
        return envelopes.get("orbital_station")
    return None


def validate_result(
    result: SimulationResult,
    *,
    benchmarks_path: Path | None = None,
    scenario_path: str | None = None,
) -> ValidationReport:
    """Compare result against bundled reference benchmarks."""
    benchmarks = load_benchmarks(benchmarks_path or default_benchmarks_path())
    checks: list[ValidationCheck] = []
    checks.extend(_check_parameter_fidelity(result.config.parameters, benchmarks))

    envelope = _resolve_envelope(
        benchmarks,
        scenario_path,
        result.config.name,
    )
    if envelope is None and scenario_path:
        stem = Path(scenario_path).stem
        envelope = benchmarks.get("scenario_envelopes", {}).get(stem)

    checks.extend(_check_derived_rates(result))
    if envelope:
        checks.extend(
            _check_envelope(
                result,
                envelope,
                scenario_path=scenario_path or envelope.get("scenario", ""),
            )
        )

    return ValidationReport(scenario_name=result.config.name, checks=checks)


def format_validation_table(report: ValidationReport) -> str:
    """Render a fixed-width validation summary for CLI output."""
    lines = [
        "Validation:",
        f"  Overall: {report.overall_status.upper()}",
        "",
        f"{'Check':<40} {'Simulated':>12} {'Reference':>18} {'Status':>8}",
        "-" * 82,
    ]
    for check in report.checks:
        sim = "n/a" if check.simulated is None else f"{check.simulated}"
        if isinstance(check.simulated, float):
            sim = f"{check.simulated:.4g}"
        lines.append(
            f"{check.name:<40} {sim:>12} {check.reference:>18} "
            f"{check.status.upper():>8}"
        )
    return "\n".join(lines)


def export_validation_json(report: ValidationReport, path: Path) -> Path:
    """Write validation report JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "scenario_name": report.scenario_name,
        "overall_status": report.overall_status,
        "checks": [
            {
                "name": c.name,
                "category": c.category,
                "simulated": c.simulated,
                "reference": c.reference,
                "status": c.status,
                "message": c.message,
                "source": c.source,
            }
            for c in report.checks
        ],
    }
    path.write_text(json.dumps(payload, indent=2))
    return path