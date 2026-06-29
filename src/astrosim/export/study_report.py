"""Markdown study report generation from simulation results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from astrosim.engine.simulator import SimulationResult
from astrosim.export.interpretation import interpret_result

if TYPE_CHECKING:
    from astrosim.validation.validate import ValidationReport


def _metric_row(label: str, value: float | None, unit: str = "") -> str:
    if value is None:
        return f"| {label} | N/A |"
    suffix = f" {unit}".rstrip()
    return f"| {label} | {value:.4g}{suffix} |"


def _validation_payload(validation: ValidationReport) -> dict:
    return {
        "overall_status": validation.overall_status,
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
            for c in validation.checks
        ],
    }


def render_study_report(
    result: SimulationResult,
    *,
    output_path: str | Path,
    method: str = "deterministic",
    scenario_path: str | Path | None = None,
    validation: ValidationReport | None = None,
) -> Path:
    """Write markdown study report and JSON metadata sidecar."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    config = result.config
    energy = result.energy_budget.summary() if result.energy_budget else {}
    mass = result.mass_budget.summary() if result.mass_budget else {}
    reliability = result.reliability_budget.summary() if result.reliability_budget else {}

    metrics = {
        "energy_net_kwh": energy.get("net_kwh"),
        "mass_net_import_kg": mass.get("net_import_kg"),
        "mission_success_probability": reliability.get("mission_success_probability"),
    }

    scenario_file = str(scenario_path) if scenario_path else "scenarios/<file>.yaml"
    repro_cmd = f"astrosim {scenario_file} --output-dir output/study_run"
    interpretation = interpret_result(result)

    lines = [
        "# AstroSim Study Report",
        "",
        "## Title",
        "",
        config.name,
        "",
        "## Objective",
        "",
        "Engineering assessment of habitat scenario performance.",
        "",
        "## Scenario",
        "",
        f"- File: `{scenario_file}`",
        f"- Duration: {config.duration_hours} h",
        f"- Crew: {config.crew_count}",
        f"- Location: {config.location}",
        "",
        "## Methods",
        "",
        f"- Method: {method}",
        f"- Timestep: {config.timestep_hours} h",
        "",
        "## Key Results",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        _metric_row("Energy net", metrics["energy_net_kwh"], "kWh"),
        _metric_row("Mass net import", metrics["mass_net_import_kg"], "kg"),
        _metric_row("Mission success probability", metrics["mission_success_probability"], ""),
        "",
        "## Figures",
        "",
        "- Dashboard: see output directory `*_dashboard.png`",
        "",
        "## Implications",
        "",
    ]
    for item in interpretation.implications:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            interpretation.verdict,
            "",
            "## References",
            "",
        ]
    )
    for ref in interpretation.references:
        lines.append(f"- {ref}")
    lines.extend(["", "## Recommended Actions", ""])
    if interpretation.actions:
        for action in interpretation.actions:
            lines.append(
                f"- `{action.parameter}`: {action.current_value} → {action.suggested_value} "
                f"— {action.rationale}"
            )
    else:
        lines.append("- No parameter changes suggested for current configuration.")
    if validation is not None:
        lines.extend(
            [
                "",
                "## Validation",
                "",
                f"Overall status: **{validation.overall_status.upper()}**",
                "",
                "| Check | Simulated | Reference | Status |",
                "|-------|-----------|-----------|--------|",
            ]
        )
        for check in validation.checks:
            sim = "n/a" if check.simulated is None else f"{check.simulated:.4g}"
            if isinstance(check.simulated, str):
                sim = check.simulated
            lines.append(
                f"| {check.name} | {sim} | {check.reference} | {check.status.upper()} |"
            )
    lines.extend(
        [
            "",
            "## Reproducibility",
            "",
            "```bash",
            repro_cmd,
            "bash scripts/integrity_check.sh",
            "```",
            "",
        ]
    )

    output.write_text("\n".join(lines))

    sidecar = {
        "title": config.name,
        "scenario_path": scenario_file,
        "method": method,
        "duration_hours": config.duration_hours,
        "crew_count": config.crew_count,
        "location": config.location,
        "metrics": metrics,
        "implications": interpretation.implications,
        "verdict": interpretation.verdict,
        "status": {
            "energy": interpretation.energy_status,
            "logistics": interpretation.logistics_status,
            "reliability": interpretation.reliability_status,
        },
        "references": interpretation.references,
        "actions": [
            {
                "parameter": a.parameter,
                "current_value": a.current_value,
                "suggested_value": a.suggested_value,
                "rationale": a.rationale,
            }
            for a in interpretation.actions
        ],
        "reproducibility_command": repro_cmd,
    }
    if validation is not None:
        sidecar["validation"] = _validation_payload(validation)

    json_path = output.with_suffix(".json")
    json_path.write_text(json.dumps(sidecar, indent=2))

    return output