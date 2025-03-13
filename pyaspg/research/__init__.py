"""Paper-inspired, topology-aware smart-grid research simulator.

This layer is deliberately independent from the legacy component simulator so
experiments can be reproduced without coupling their results to SimPy timing.
"""

from .simulator import SimulationConfig, SimulationResult, run_simulation

__all__ = ["SimulationConfig", "SimulationResult", "run_simulation"]
