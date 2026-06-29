"""AstroSim — space habitat simulation framework."""

import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def _pyproject_version() -> str | None:
    root = Path(__file__).resolve().parents[2]
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None
    match = re.search(r'^version = "([^"]+)"', pyproject.read_text(), re.M)
    return match.group(1) if match else None


def _is_source_tree() -> bool:
    root = Path(__file__).resolve().parents[2]
    return (root / "pyproject.toml").exists() and (root / "src" / "astrosim").is_dir()


if _is_source_tree():
    __version__ = _pyproject_version() or "0.0.0+dev"
else:
    try:
        __version__ = version("astrosim")
    except PackageNotFoundError:
        __version__ = _pyproject_version() or "0.0.0+dev"