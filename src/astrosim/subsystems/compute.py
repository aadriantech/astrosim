"""Compute and AI workload subsystem."""

from __future__ import annotations

from typing import Any

from astrosim.engine.state import SimulationState
from astrosim.subsystems.base import Subsystem


class ComputeSubsystem(Subsystem):
    name = "compute"

    def update(
        self,
        state: SimulationState,
        dt_hours: float,
        params: dict[str, Any],
    ) -> dict[str, float]:
        compute_nodes = params.get("compute_nodes", 4)
        watts_per_node = params.get("watts_per_node", 150.0)
        ai_utilization = params.get("ai_utilization", 0.6)
        inference_jobs_per_hour = params.get("inference_jobs_per_hour", 120.0)
        radiation_sv_per_year = params.get("radiation_sv_per_year", 0.4)
        shielding_factor = params.get("compute_shielding_factor", 0.7)

        power_kw = (compute_nodes * watts_per_node / 1000.0) * ai_utilization
        jobs_completed = inference_jobs_per_hour * ai_utilization * dt_hours

        annual_hours = 8760.0
        dose_sv = (
            radiation_sv_per_year
            * (1.0 - shielding_factor)
            * (dt_hours / annual_hours)
        )
        cumulative_dose = self._local_state.get("cumulative_dose_sv", 0.0) + dose_sv
        bit_error_rate = dose_sv * params.get("radiation_ber_factor", 1e-6)

        return {
            "power_kw": power_kw,
            "jobs_completed": jobs_completed,
            "active_nodes": compute_nodes,
            "ai_utilization": ai_utilization,
            "dose_sv_step": dose_sv,
            "cumulative_dose_sv": cumulative_dose,
            "bit_error_rate": bit_error_rate,
        }