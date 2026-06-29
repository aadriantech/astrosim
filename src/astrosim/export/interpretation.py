"""Rule-based interpretation of simulation results — implications and verdict."""

from __future__ import annotations

from dataclasses import dataclass, field

from astrosim.engine.simulator import SimulationResult


@dataclass
class ResultInterpretation:
    implications: list[str] = field(default_factory=list)
    verdict: str = ""
    energy_status: str = ""
    logistics_status: str = ""
    reliability_status: str = ""


def interpret_result(result: SimulationResult) -> ResultInterpretation:
    """Derive engineering implications and an overall verdict from budgets and metrics."""
    out = ResultInterpretation()
    final = result.final_state
    metrics = final.metrics if final else {}

    energy_net = result.energy_budget.net_kwh if result.energy_budget else None
    mass_net = result.mass_budget.net_import_kg if result.mass_budget else None
    success = (
        result.reliability_budget.mission_success_probability
        if result.reliability_budget
        else None
    )
    food_net = metrics.get("eclss.food_net_import_kg")
    water_net = metrics.get("eclss.water_net_kg")
    o2_net = metrics.get("eclss.o2_net_import_kg")
    food_supplied = metrics.get("greenhouse.food_supplied_kg", 0.0)
    water_supplied = metrics.get("eclss.water_supplied_kg", 0.0)
    o2_supplied = metrics.get("eclss.o2_supplied_kg", 0.0)

    # Energy
    if energy_net is not None:
        if energy_net < -500:
            out.energy_status = "critical_deficit"
            out.implications.append(
                f"Energy deficit is large ({energy_net:.0f} kWh net). "
                "Solar capacity or battery storage is insufficient for the configured load; "
                "mission timelines risk brownouts without resupply or load shedding."
            )
        elif energy_net < 0:
            out.energy_status = "marginal_deficit"
            out.implications.append(
                f"Energy runs slightly negative ({energy_net:.1f} kWh net). "
                "The habitat is close to balance; small increases in crew or ISRU load may tip into deficit."
            )
        else:
            out.energy_status = "surplus"
            out.implications.append(
                f"Energy is in surplus ({energy_net:.1f} kWh net). "
                "Additional subsystems (greenhouse, ISRU) can be supported without immediate power upgrades."
            )

    # Logistics / mass
    if mass_net is not None:
        if mass_net > 100:
            out.logistics_status = "high_import"
            out.implications.append(
                f"Net mass import is high ({mass_net:.0f} kg). "
                "Logistics chain must deliver consumables; closed-loop production is not offsetting demand."
            )
        elif mass_net > 0:
            out.logistics_status = "moderate_import"
            out.implications.append(
                f"Net mass import is positive ({mass_net:.1f} kg). "
                "Some consumables still require external supply over the simulated period."
            )
        else:
            out.logistics_status = "production_offset"
            out.implications.append(
                f"Net mass import is negative ({mass_net:.1f} kg). "
                "ISRU or recycling produces more than is consumed — local resource loop is reducing logistics burden."
            )

    if food_net is not None:
        if food_supplied and food_supplied > 0:
            pct = 100.0 * (1.0 - food_net / max(metrics.get("eclss.food_consumed_kg", 1), 0.001))
            out.implications.append(
                f"Greenhouse supplies ~{food_supplied:.2f} kg food per final step; "
                f"~{pct:.0f}% of crew food demand met locally (food net import {food_net:.2f} kg/step)."
            )
        elif food_net >= 1.5:
            out.implications.append(
                f"Food net import is high ({food_net:.2f} kg/step). "
                "No meaningful local food production — full food logistics required."
            )

    if water_net is not None and water_supplied and water_supplied > 0:
        out.implications.append(
            f"ISRU water credit reduces ECLSS net water import to {water_net:.2f} kg/step "
            f"({water_supplied:.2f} kg supplied from ISRU on final step)."
        )
    elif water_net is not None and water_net > 0.3:
        out.implications.append(
            f"Water net import remains {water_net:.2f} kg/step after recovery — "
            "consider higher recovery rate or ISRU water production."
        )

    if o2_net is not None and o2_supplied and o2_supplied > 0:
        out.implications.append(
            f"ISRU O₂ credit: net import {o2_net:.2f} kg/step with {o2_supplied:.2f} kg supplied."
        )

    # Reliability
    if success is not None:
        if success < 0.99:
            out.reliability_status = "elevated_risk"
            out.implications.append(
                f"Mission success probability is {success:.4f} — "
                "structure/micrometeoroid risk is non-negligible over this duration."
            )
        else:
            out.reliability_status = "acceptable"
            out.implications.append(
                f"Reliability estimate is high ({success:.5f}) for the simulated period."
            )

    # Overall verdict
    verdict_parts: list[str] = []
    if out.energy_status in ("critical_deficit", "marginal_deficit"):
        verdict_parts.append("Power system needs upgrade before scaling crew or duration.")
    elif out.energy_status == "surplus":
        verdict_parts.append("Power system is adequate for current configuration.")

    if out.logistics_status == "production_offset":
        verdict_parts.append("Mass loop is favorable — ISRU/recycling reduces resupply.")
    elif out.logistics_status in ("moderate_import", "high_import"):
        if food_supplied and food_supplied > 0:
            verdict_parts.append("Greenhouse helps but logistics remain net-positive.")
        else:
            verdict_parts.append("Logistics remain import-dependent for this scenario.")

    if out.reliability_status == "elevated_risk":
        verdict_parts.append("Review shielding or reduce exposure duration.")

    if not verdict_parts:
        out.verdict = "Configuration is balanced for the simulated period; continue trade studies before committing to hardware."
    else:
        out.verdict = " ".join(verdict_parts)

    return out