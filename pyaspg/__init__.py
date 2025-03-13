"""PyASPG package.

Legacy component classes remain available from the package root, but are
loaded only when requested. This keeps the standard-library research simulator
usable without importing the legacy numerical stack.
"""

from importlib import import_module

_EXPORTS = {
    "CommunicationNetwork": ("pyaspg.communication", "CommunicationNetwork"),
    "SmartMeter": ("pyaspg.communication", "SmartMeter"),
    "Transmitter": ("pyaspg.distribution", "Transmitter"),
    "Distributor": ("pyaspg.distribution", "Distributor"),
    "Substation": ("pyaspg.distribution", "Substation"),
    "WindTurbine": ("pyaspg.generation", "WindTurbine"),
    "SolarPanel": ("pyaspg.generation", "SolarPanel"),
    "PowerPlant": ("pyaspg.generation", "PowerPlant"),
    "Generator": ("pyaspg.generation", "Generator"),
    "NetAggregator": ("pyaspg.management", "NetAggregator"),
    "UtilityCompany": ("pyaspg.management", "UtilityCompany"),
    "ControlSystem": ("pyaspg.management", "ControlSystem"),
    "PyASPGCreator": ("pyaspg.simulation", "PyASPGCreator"),
    "GridSimulator": ("pyaspg.simulation", "GridSimulator"),
    "Prosumer": ("pyaspg.prosume", "Prosumer"),
    "RR_distribution": ("pyaspg.utils", "RR_distribution"),
    "find_multipliers": ("pyaspg.utils", "find_multipliers"),
    "inflation_attack": ("pyaspg.attacks", "inflation_attack"),
    "deflation_attack": ("pyaspg.attacks", "deflation_attack"),
    "hybrid_attack": ("pyaspg.attacks", "hybrid_attack"),
}
__all__ = list(_EXPORTS)


def __getattr__(name: str):
    if name not in _EXPORTS:
        raise AttributeError(f"module 'pyaspg' has no attribute {name!r}")
    module_name, attribute = _EXPORTS[name]
    value = getattr(import_module(module_name), attribute)
    globals()[name] = value
    return value
