# Lunar Base Energy Trade Study

**AstroSim example study** — reproducible engineering report (Phase 12).

## Objective

Compare lunar base energy balance across solar array sizing using deterministic simulation and Pareto trade study.

## Scenario

- Primary: `scenarios/lunar_base.yaml`
- Trade axes: `solar_array_kw` vs `battery_kwh`

## Methods

1. Deterministic 30-day run (`duration_hours: 720`)
2. Pareto trade study via CLI

## Reproduce

```bash
cd /home/adrianlos/projects/astrosim
pip install -e ".[dev]"
astrosim scenarios/lunar_base.yaml --report --output-dir output/lunar_study
astrosim scenarios/lunar_base.yaml --trade-study --output-dir output/lunar_study
bash scripts/integrity_check.sh
```

## Key results (reference run)

| Metric | Typical order of magnitude |
|--------|---------------------------|
| Energy net (kWh) | Negative without oversized solar — see optimization suggestions |
| Mission success probability | > 0.99 for lunar_base default |
| Trade study Pareto points | 12 grid points (4×3 solar/battery grid) |

## Conclusions

Solar capacity and battery storage dominate lunar energy feasibility. Use `astrosim --trade-study` to explore the Pareto frontier before committing to hardware mass.

## Citation

```
AstroSim v1.0.0 — https://github.com/aadriantech/astrosim
Study template: docs/STUDY_TEMPLATE.md
```