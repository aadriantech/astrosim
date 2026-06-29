# Performance Baseline

Run on the project host after changes to engine or subsystems:

```bash
PYTHONPATH=src python3 scripts/benchmark_sim.py
```

## Reference (soft threshold)

| Workload | Steps | Soft limit |
|----------|-------|------------|
| 1-year lunar (`8760h`, Δt=6h) | 1460 | 30s wall time |

The benchmark prints `WARN` above 30s but exits 0 (report-only, not a CI gate).