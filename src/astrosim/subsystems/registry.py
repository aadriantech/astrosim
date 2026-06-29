"""Plugin registry for custom subsystems."""

from __future__ import annotations

from typing import Type

from astrosim.subsystems.base import Subsystem

_REGISTRY: dict[str, Type[Subsystem]] = {}


def register_subsystem(cls: Type[Subsystem]) -> Type[Subsystem]:
    """Decorator to register a subsystem plugin by name."""
    _REGISTRY[cls.name] = cls
    return cls


def unregister_subsystem(name: str) -> None:
    """Remove a registered subsystem (intended for test cleanup)."""
    _REGISTRY.pop(name, None)


def get_subsystem(name: str) -> Subsystem:
    if name not in _REGISTRY:
        raise KeyError(f"Unknown subsystem '{name}'. Registered: {list(_REGISTRY)}")
    return _REGISTRY[name]()


def list_subsystems() -> list[str]:
    return sorted(_REGISTRY)


def build_subsystems(names: list[str] | None = None) -> list[Subsystem]:
    """Instantiate registered subsystems. None returns all registered."""
    if names is None:
        names = list_subsystems()
    return [get_subsystem(name) for name in names]


def _register_builtin() -> None:
    from astrosim.subsystems.compute import ComputeSubsystem
    from astrosim.subsystems.eclss import ECLSSSubsystem
    from astrosim.subsystems.isru import ISRUSubsystem
    from astrosim.subsystems.power import PowerSubsystem
    from astrosim.subsystems.structure import StructureSubsystem
    from astrosim.subsystems.thermal import ThermalSubsystem

    for cls in (
        PowerSubsystem,
        ECLSSSubsystem,
        ThermalSubsystem,
        StructureSubsystem,
        ISRUSubsystem,
        ComputeSubsystem,
    ):
        register_subsystem(cls)


_register_builtin()