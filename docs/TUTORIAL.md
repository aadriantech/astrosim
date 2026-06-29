# AstroSim Tutorial (15 minutes)

## 1. Install

```bash
git clone https://github.com/aadriantech/astrosim.git
cd astrosim
pip install -e ".[dev,optimize]"
```

## 2. Run a scenario

```bash
python examples/run_lunar_base.py
```

Output lands in `output/lunar_base/` (JSON, CSV, PNG, HTML).

## 3. Use the CLI

```bash
astrosim scenarios/lunar_base.yaml --web --output-dir output/cli_run
```

## 4. Load a scenario in Python

```python
from astrosim.scenario import load_and_build

simulator = load_and_build("scenarios/mars_habitat.yaml")
result = simulator.run()
print(result.energy_budget.net_kwh)
```

## 5. Export and visualize

```python
from astrosim.export.formats import export_json
from astrosim.visualization.dashboard import plot_dashboard

export_json(result, "results.json")
plot_dashboard(result, "dashboard.png")
```

## 6. Sensitivity and optimization

```bash
python examples/run_sensitivity.py
python examples/run_optimize.py   # requires [optimize]
```

## 7. Verify your install

```bash
bash scripts/integrity_check.sh
```