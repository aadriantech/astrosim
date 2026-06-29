from astrosim.subsystems.base import Subsystem
from astrosim.subsystems.compute import ComputeSubsystem
from astrosim.subsystems.eclss import ECLSSSubsystem
from astrosim.subsystems.isru import ISRUSubsystem
from astrosim.subsystems.power import PowerSubsystem
from astrosim.subsystems.registry import (
    build_subsystems,
    get_subsystem,
    list_subsystems,
    register_subsystem,
    unregister_subsystem,
)
from astrosim.subsystems.structure import StructureSubsystem
from astrosim.subsystems.thermal import ThermalSubsystem

DEFAULT_SUBSYSTEMS: list[Subsystem] = build_subsystems()

__all__ = [
    "ComputeSubsystem",
    "DEFAULT_SUBSYSTEMS",
    "ECLSSSubsystem",
    "ISRUSubsystem",
    "PowerSubsystem",
    "StructureSubsystem",
    "Subsystem",
    "ThermalSubsystem",
    "build_subsystems",
    "get_subsystem",
    "list_subsystems",
    "register_subsystem",
    "unregister_subsystem",
]