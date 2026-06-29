"""LLM integration hooks for optimization and insights."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from astrosim.engine.simulator import SimulationResult


class LLMClient(Protocol):
    """Protocol for external LLM providers."""

    def complete(self, prompt: str) -> str: ...


@dataclass
class InsightRequest:
    result: SimulationResult
    question: str = "Summarize key risks and optimization opportunities."


@dataclass
class OptimizationSuggestion:
    parameter: str
    current_value: float
    suggested_value: float
    rationale: str


class AIHooks:
    """Bridge between simulation results and LLM analysis."""

    def __init__(self, client: LLMClient | None = None) -> None:
        self.client = client

    def build_context(self, result: SimulationResult) -> str:
        config = result.config
        energy = result.energy_budget.summary() if result.energy_budget else {}
        mass = result.mass_budget.summary() if result.mass_budget else {}
        reliability = (
            result.reliability_budget.summary() if result.reliability_budget else {}
        )
        final = result.final_state.metrics if result.final_state else {}

        lines = [
            f"Scenario: {config.name} ({config.location})",
            f"Duration: {config.duration_hours} h, Crew: {config.crew_count}",
            f"Energy: {energy}",
            f"Mass: {mass}",
            f"Reliability: {reliability}",
            f"Final metrics: {final}",
        ]
        return "\n".join(lines)

    def generate_insights(self, request: InsightRequest) -> str:
        context = self.build_context(request.result)
        prompt = f"{request.question}\n\nSimulation data:\n{context}"

        if self.client is None:
            return _offline_insights(request.result)

        return self.client.complete(prompt)

    def suggest_optimizations(
        self, result: SimulationResult
    ) -> list[OptimizationSuggestion]:
        suggestions: list[OptimizationSuggestion] = []
        params = result.config.parameters

        if result.energy_budget and result.energy_budget.net_kwh < 0:
            solar = params.get("solar_array_kw", 50.0)
            suggestions.append(
                OptimizationSuggestion(
                    parameter="solar_array_kw",
                    current_value=solar,
                    suggested_value=solar * 1.25,
                    rationale="Energy deficit detected; increase solar capacity.",
                )
            )

        if result.mass_budget and result.mass_budget.net_import_kg > 0:
            recovery = params.get("water_recovery_rate", 0.93)
            suggestions.append(
                OptimizationSuggestion(
                    parameter="water_recovery_rate",
                    current_value=recovery,
                    suggested_value=min(0.99, recovery + 0.03),
                    rationale="Net mass import positive; improve ECLSS recovery.",
                )
            )

        return suggestions


def _offline_insights(result: SimulationResult) -> str:
    parts = [f"Completed {len(result.history)} timesteps for '{result.config.name}'."]
    if result.energy_budget:
        e = result.energy_budget.summary()
        parts.append(
            f"Energy balance: {e['net_kwh']:.1f} kWh net "
            f"({e['generated_kwh']:.1f} generated, {e['consumed_kwh']:.1f} consumed)."
        )
    if result.reliability_budget:
        p = result.reliability_budget.mission_success_probability
        parts.append(f"Estimated mission success probability: {p:.4f}.")
    return " ".join(parts)