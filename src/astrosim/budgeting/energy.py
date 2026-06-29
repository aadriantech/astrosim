"""Energy budget tracking."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EnergyBudget:
    generated_kwh: float = 0.0
    consumed_kwh: float = 0.0
    by_subsystem: dict[str, float] = field(default_factory=dict)

    def accumulate(self, subsystem: str, outputs: dict[str, float]) -> None:
        if "generated_kwh" in outputs:
            self.generated_kwh += outputs["generated_kwh"]
        if "consumed_kwh" in outputs:
            self.consumed_kwh += outputs["consumed_kwh"]
        power_kw = outputs.get("power_kw", 0.0)
        if power_kw:
            dt_proxy = outputs.get("consumed_kwh", 0.0) / max(outputs.get("load_kw", 1.0), 0.001)
            if dt_proxy == 0:
                dt_proxy = 1.0
            self.by_subsystem[subsystem] = self.by_subsystem.get(subsystem, 0.0) + power_kw * dt_proxy
            self.consumed_kwh += power_kw * dt_proxy

    @property
    def net_kwh(self) -> float:
        return self.generated_kwh - self.consumed_kwh

    def summary(self) -> dict[str, float]:
        return {
            "generated_kwh": self.generated_kwh,
            "consumed_kwh": self.consumed_kwh,
            "net_kwh": self.net_kwh,
        }