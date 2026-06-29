"""Mass budget tracking."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MassBudget:
    imported_kg: float = 0.0
    produced_kg: float = 0.0
    consumed_kg: float = 0.0
    by_subsystem: dict[str, float] = field(default_factory=dict)

    def accumulate(self, subsystem: str, outputs: dict[str, float]) -> None:
        produced = (
            outputs.get("o2_produced_kg", 0.0)
            + outputs.get("water_produced_kg", 0.0)
        )
        consumed = (
            outputs.get("o2_consumed_kg", 0.0)
            + outputs.get("water_net_kg", 0.0)
            + outputs.get("food_consumed_kg", 0.0)
            + outputs.get("waste_net_kg", 0.0)
        )
        self.produced_kg += produced
        self.consumed_kg += consumed
        net = consumed - produced
        if net != 0:
            self.by_subsystem[subsystem] = self.by_subsystem.get(subsystem, 0.0) + net

    @property
    def net_import_kg(self) -> float:
        return self.consumed_kg - self.produced_kg + self.imported_kg

    def summary(self) -> dict[str, float]:
        return {
            "imported_kg": self.imported_kg,
            "produced_kg": self.produced_kg,
            "consumed_kg": self.consumed_kg,
            "net_import_kg": self.net_import_kg,
        }