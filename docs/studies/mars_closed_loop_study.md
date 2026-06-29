# Mars Closed-Loop Habitat Study

**AstroSim v1.1+ example study** — integrated food, water, and O₂ loops.

## Objective

Quantify mass import reduction for a Mars habitat using greenhouse food production and ISRU water/O₂ credits versus baseline `mars_habitat`.

## Scenario

- Closed loop: `scenarios/mars_closed_loop.yaml`
- Baseline: `scenarios/mars_habitat.yaml`

## Methods

Deterministic 168 h runs with subsystem order: power → greenhouse → isru → eclss.

## Reproduce

```bash
cd /home/adrianlos/projects/astrosim
pip install -e ".[dev]"
astrosim --compare scenarios/mars_closed_loop.yaml scenarios/mars_habitat.yaml
python examples/run_mars_closed_loop.py
PYTHONPATH=src python3 -m pytest tests/test_closed_loop_audit.py -q
```

## Expected findings

- Lower `eclss.food_net_import_kg` vs mars_habitat
- Lower total `mass.net_import_kg`
- ISRU reduces `eclss.o2_net_import_kg` and `eclss.water_net_kg`

## Citation

See [CITATION.cff](../../CITATION.cff) at repository root.