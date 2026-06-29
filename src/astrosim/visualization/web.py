"""Simple self-contained HTML web dashboard."""

from __future__ import annotations

import json
from pathlib import Path

from astrosim.engine.simulator import SimulationResult
from astrosim.visualization.dashboard import result_to_dataframe


def render_web_dashboard(
    result: SimulationResult,
    output_path: str | Path,
    *,
    study_report_path: str | Path | None = None,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    study_meta: dict | None = None
    if study_report_path is not None:
        sidecar = Path(study_report_path)
        if sidecar.exists():
            study_meta = json.loads(sidecar.read_text())

    df = result_to_dataframe(result)
    energy = result.energy_budget.summary() if result.energy_budget else {}
    mass = result.mass_budget.summary() if result.mass_budget else {}
    reliability = (
        result.reliability_budget.summary() if result.reliability_budget else {}
    )

    def _series(column: str) -> list[float]:
        if column not in df.columns:
            return []
        return [float(v) for v in df[column].tolist()]

    chart_data = {
        "time_hours": _series("time_hours"),
        "power_generated": _series("power.generated_kwh"),
        "power_stored": _series("power.stored_kwh"),
        "eclss_water_net": _series("eclss.water_net_kg"),
        "thermal_heat_load": _series("thermal.heat_load_kw"),
        "greenhouse_food_supplied": _series("greenhouse.food_supplied_kg"),
        "eclss_food_net_import": _series("eclss.food_net_import_kg"),
    }

    repro_block = ""
    if study_meta:
        repro_cmd = study_meta.get("reproducibility_command", "")
        repro_block = f"""
  <div class="card" style="margin-top:1.5rem; grid-column: 1 / -1;">
    <div class="label">Study Report</div>
    <div class="value" style="font-size:1rem;">{study_meta.get('title', result.config.name)}</div>
    <pre style="margin-top:0.75rem; color:#8b95b0; white-space:pre-wrap;">{repro_cmd}</pre>
  </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AstroSim — {result.config.name}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #0b0f1a; color: #e8ecf4; }}
    h1 {{ color: #7eb8ff; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .card {{ background: #151b2e; border-radius: 8px; padding: 1rem; border: 1px solid #2a3555; }}
    .label {{ color: #8b95b0; font-size: 0.85rem; }}
    .value {{ font-size: 1.4rem; font-weight: 600; }}
    canvas {{ background: #151b2e; border-radius: 8px; margin-top: 1.5rem; max-width: 100%; display: block; }}
  </style>
</head>
<body>
  <h1>AstroSim Dashboard</h1>
  <p>{result.config.name} · {result.config.location} · {result.config.duration_hours} h</p>
  <div class="grid">
    <div class="card"><div class="label">Energy Net (kWh)</div><div class="value">{energy.get('net_kwh', 0):.1f}</div></div>
    <div class="card"><div class="label">Mass Net Import (kg)</div><div class="value">{mass.get('net_import_kg', 0):.1f}</div></div>
    <div class="card"><div class="label">Mission Success</div><div class="value">{reliability.get('mission_success_probability', 0):.4f}</div></div>
    <div class="card"><div class="label">Timesteps</div><div class="value">{len(result.history)}</div></div>
    {repro_block}
  </div>
  <canvas id="power-chart" width="900" height="320"></canvas>
  <canvas id="subsystem-chart" width="900" height="320"></canvas>
  <canvas id="food-chart" width="900" height="320"></canvas>
  <script>
    const data = {json.dumps(chart_data)};
    function drawChart(canvasId, title, seriesList) {{
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext('2d');
      const w = canvas.width, h = canvas.height, pad = 40;
      const allValues = seriesList.flatMap(s => s.values);
      const maxY = Math.max(...allValues, 1);
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#8b95b0';
      ctx.fillText(title, pad, 18);
      seriesList.forEach((series, idx) => {{
        if (!series.values.length) return;
        ctx.strokeStyle = series.color;
        ctx.beginPath();
        series.values.forEach((v, i) => {{
          const x = pad + (i / Math.max(series.values.length - 1, 1)) * (w - 2 * pad);
          const y = h - pad - (v / maxY) * (h - 2 * pad);
          i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
        }});
        ctx.stroke();
        ctx.fillStyle = series.color;
        ctx.fillText(series.label, pad + idx * 120, 36);
      }});
    }}
    drawChart('power-chart', 'Power over time', [
      {{ label: 'Generated', color: '#7eb8ff', values: data.power_generated }},
      {{ label: 'Stored', color: '#5fd4a0', values: data.power_stored }},
    ]);
    drawChart('subsystem-chart', 'ECLSS & Thermal', [
      {{ label: 'Water Net (kg)', color: '#f0a060', values: data.eclss_water_net }},
      {{ label: 'Heat Load (kW)', color: '#d47eb8', values: data.thermal_heat_load }},
    ]);
    if (data.greenhouse_food_supplied.length || data.eclss_food_net_import.length) {{
      drawChart('food-chart', 'Food Loop', [
        {{ label: 'Food Supplied (kg)', color: '#8fd47e', values: data.greenhouse_food_supplied }},
        {{ label: 'Food Net Import (kg)', color: '#e8c060', values: data.eclss_food_net_import }},
      ]);
    }}
  </script>
</body>
</html>"""

    output.write_text(html)
    return output