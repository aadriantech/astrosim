"""Time-stepped simulation engine."""

from __future__ import annotations

from dataclasses import dataclass, field

from astrosim.budgeting.energy import EnergyBudget
from astrosim.budgeting.mass import MassBudget
from astrosim.budgeting.reliability import ReliabilityBudget
from astrosim.engine.events import EventQueue, apply_event_payload, tick_event_recovery
from astrosim.engine.state import SimulationConfig, SimulationState
from astrosim.subsystems.base import Subsystem


@dataclass
class SimulationResult:
    config: SimulationConfig
    history: list[SimulationState] = field(default_factory=list)
    energy_budget: EnergyBudget | None = None
    mass_budget: MassBudget | None = None
    reliability_budget: ReliabilityBudget | None = None

    @property
    def final_state(self) -> SimulationState | None:
        return self.history[-1] if self.history else None


class Simulator:
    """Orchestrates subsystem updates over discrete timesteps."""

    def __init__(
        self,
        config: SimulationConfig,
        subsystems: list[Subsystem],
    ) -> None:
        self.config = config
        self.subsystems = subsystems
        self.energy_budget = EnergyBudget()
        self.mass_budget = MassBudget()
        self.reliability_budget = ReliabilityBudget(
            mission_hours=config.duration_hours
        )
        self.event_queue = EventQueue(config.events)

    def run(self) -> SimulationResult:
        state = SimulationState(crew_count=self.config.crew_count)
        history: list[SimulationState] = []

        for step in range(self.config.num_steps):
            state.step = step
            state.time_hours = step * self.config.timestep_hours
            dt = self.config.timestep_hours

            tick_event_recovery(self.config, state.time_hours)
            self._process_events(state)

            for subsystem in self.subsystems:
                outputs = subsystem.update(state, dt, self.config.parameters)
                subsystem._local_state.update(outputs)
                state.record_subsystem(subsystem.name, outputs)
                self.energy_budget.accumulate(subsystem.name, outputs)
                self.mass_budget.accumulate(subsystem.name, outputs)
                self.reliability_budget.record_step(subsystem.name, outputs)

            history.append(_snapshot(state))

        return SimulationResult(
            config=self.config,
            history=history,
            energy_budget=self.energy_budget,
            mass_budget=self.mass_budget,
            reliability_budget=self.reliability_budget,
        )

    def _process_events(self, state: SimulationState) -> None:
        for event in self.event_queue.due_at(state.time_hours):
            state.events_fired.append(event.name)
            apply_event_payload(self.config, event, state.time_hours)
            if event.payload:
                state.flags.update({f"event.{k}": bool(v) for k, v in event.payload.items()})
            if event.handler:
                event.handler()


def _snapshot(state: SimulationState) -> SimulationState:
    return SimulationState(
        time_hours=state.time_hours,
        step=state.step,
        energy_kwh=state.energy_kwh,
        mass_kg=state.mass_kg,
        crew_count=state.crew_count,
        subsystem_outputs=dict(state.subsystem_outputs),
        metrics=dict(state.metrics),
        flags=dict(state.flags),
        events_fired=list(state.events_fired),
    )