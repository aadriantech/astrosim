# AstroSim Study Report Template

## Title

*Mission / scenario name*

## Objective

What engineering question does this study answer?

## Scenario

- File: `scenarios/...`
- Duration, crew, location

## Methods

- Deterministic run / Monte Carlo / trade study / optimization

## Key Results

| Metric | Value |
|--------|-------|
| Energy net (kWh) | |
| Mass net import (kg) | |
| Mission success probability | |

## Figures

- Dashboard PNG / trade study CSV path

## Conclusions

## Reproducibility

```bash
astrosim scenarios/<file>.yaml --output-dir output/study_run
bash scripts/integrity_check.sh
```