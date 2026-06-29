"""Load curated reference benchmarks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def default_benchmarks_path() -> Path:
    """Return path to bundled ``reference/benchmarks.yaml``."""
    return Path(__file__).resolve().parents[3] / "reference" / "benchmarks.yaml"


def load_benchmarks(path: Path | None = None) -> dict[str, Any]:
    """Load benchmarks YAML; raises ``FileNotFoundError`` if missing."""
    benchmarks_path = path or default_benchmarks_path()
    if not benchmarks_path.exists():
        raise FileNotFoundError(
            f"Benchmarks file not found: {benchmarks_path}. "
            "Expected reference/benchmarks.yaml at repo root."
        )
    return yaml.safe_load(benchmarks_path.read_text())