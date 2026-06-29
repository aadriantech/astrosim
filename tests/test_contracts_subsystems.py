"""Contract tests: built-in subsystems emit required output keys."""

from __future__ import annotations

from pathlib import Path

import yaml

from astrosim.engine.state import SimulationState
from astrosim.subsystems.compute import ComputeSubsystem
from astrosim.subsystems.eclss import ECLSSSubsystem
from astrosim.subsystems.greenhouse import GreenhouseSubsystem
from astrosim.subsystems.isru import ISRUSubsystem
from astrosim.subsystems.power import PowerSubsystem
from astrosim.subsystems.structure import StructureSubsystem
from astrosim.subsystems.thermal import ThermalSubsystem

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "contracts" / "subsystem_outputs.yaml"

SUBSYSTEMS = {
    "power": PowerSubsystem,
    "eclss": ECLSSSubsystem,
    "thermal": ThermalSubsystem,
    "structure": StructureSubsystem,
    "isru": ISRUSubsystem,
    "compute": ComputeSubsystem,
    "greenhouse": GreenhouseSubsystem,
}


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())


def test_manifest_covers_all_builtins():
    manifest = _load_manifest()
    assert set(manifest) == set(SUBSYSTEMS)


def test_each_subsystem_produces_required_output_keys():
    manifest = _load_manifest()
    state = SimulationState(crew_count=2, energy_kwh=10.0)
    params: dict = {}

    for name, cls in SUBSYSTEMS.items():
        outputs = cls().step(state, 6.0, params)
        required = manifest[name]["required_keys"]
        missing = [key for key in required if key not in outputs]
        assert not missing, f"{name} missing keys: {missing}"