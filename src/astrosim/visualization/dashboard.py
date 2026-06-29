"""Dashboard and plot generation."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from astrosim.engine.simulator import SimulationResult


def result_to_dataframe(result: SimulationResult) -> pd.DataFrame:
    rows = []
    cumulative_risk = 0.0
    for state in result.history:
        row = {
            "time_hours": state.time_hours,
            "step": state.step,
            "mass_kg": state.mass_kg,
        }
        row.update(state.metrics)
        step_risk = row.get("structure.micrometeoroid_step_risk", 0.0)
        cumulative_risk += step_risk
        row["reliability.cumulative_risk"] = cumulative_risk
        row["reliability.success_probability"] = float(math.exp(-cumulative_risk))
        rows.append(row)
    return pd.DataFrame(rows)


def plot_dashboard(result: SimulationResult, output_path: str | Path) -> Path:
    df = result_to_dataframe(result)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle(f"AstroSim — {result.config.name}")

    _plot_series(axes[0, 0], df, "power.generated_kwh", "Power Generated (kWh/step)")
    _plot_series(axes[0, 1], df, "power.stored_kwh", "Energy Stored (kWh)")
    _plot_series(axes[0, 2], df, "mass_kg", "Net Mass Balance (kg)")
    _plot_series(axes[1, 0], df, "eclss.water_net_kg", "ECLSS Water Net (kg/step)")
    _plot_series(axes[1, 1], df, "isru.o2_produced_kg", "ISRU O₂ Produced (kg/step)")
    _plot_series(
        axes[1, 2],
        df,
        "reliability.success_probability",
        "Mission Success Probability",
    )

    plt.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output


def _plot_series(ax, df: pd.DataFrame, column: str, title: str) -> None:
    if column in df.columns:
        ax.plot(df["time_hours"], df[column])
    ax.set_title(title)
    ax.set_xlabel("Time (hours)")
    ax.grid(True, alpha=0.3)