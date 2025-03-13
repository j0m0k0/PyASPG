"""Reproducible time-slotted smart-grid model for FDIA research.

The model abstracts dispatch at substation level. It is intended for scenario
analysis and education; it is not an AC power-flow or protection-system model.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import random
from typing import Any


@dataclass(frozen=True)
class SimulationConfig:
    steps: int = 240
    timestep_hours: float = 1.0 / 60.0
    prosumers: int = 240
    aggregators: int = 5
    substations: int = 2
    compromised_aggregator: int = 0
    attack: str = "hybrid"  # none, inflation, deflation, hybrid, replay, noise, ramp, outage
    attack_start: int = 80
    attack_end: int = 100
    attack_strength: float = 0.10
    aggregator_topology: str = "pareto"  # uniform or pareto
    pareto_alpha: float = 3.0
    substation_topology: str = "skewed"  # balanced or skewed
    skew: float = 0.80
    safety_margin: float = 1.10
    forecast_error: float = 0.05
    line_loss_rate: float = 0.035
    redistribution: bool = True
    redistribution_distance_km: float = 2.0
    line_reliability: float = 0.90
    redistribution_exponent: float = 2.0
    battery_share: float = 0.0
    battery_hours: float = 3.0
    nsr_threshold: float = 0.05
    seed: int = 42

    def validate(self) -> None:
        if self.steps < 1 or self.timestep_hours <= 0 or self.prosumers < 2 or self.aggregators < 1 or self.substations < 1:
            raise ValueError("steps and timestep_hours must be positive; aggregators and substations positive; prosumers at least 2")
        if not 0 <= self.compromised_aggregator < self.aggregators:
            raise ValueError("compromised_aggregator must identify an existing aggregator")
        if self.attack not in {"none", "inflation", "deflation", "hybrid", "replay", "noise", "ramp", "outage"}:
            raise ValueError("unsupported attack; choose none, inflation, deflation, hybrid, replay, noise, ramp or outage")
        if not 0 <= self.attack_start <= self.attack_end <= self.steps:
            raise ValueError("attack window must satisfy 0 <= attack_start <= attack_end <= steps")
        if not 0 <= self.attack_strength <= 0.95:
            raise ValueError("attack_strength must be in [0, 0.95]")
        if not 0 < self.safety_margin or not 0 <= self.forecast_error < 1:
            raise ValueError("safety_margin must be positive and forecast_error in [0, 1)")
        if not 0 <= self.line_loss_rate < 1 or not 0 <= self.battery_share <= 1:
            raise ValueError("line_loss_rate must be in [0, 1) and battery_share in [0, 1]")
        if not 0 < self.line_reliability <= 1 or self.redistribution_exponent <= 0:
            raise ValueError("line_reliability must be in (0, 1] and redistribution_exponent positive")
        if self.pareto_alpha <= 0 or not 0 <= self.skew <= 1 or self.battery_hours < 0:
            raise ValueError("pareto_alpha must be positive, skew in [0, 1], and battery_hours non-negative")
        if self.redistribution_distance_km < 0:
            raise ValueError("redistribution_distance_km must be non-negative")
        if self.aggregator_topology not in {"uniform", "pareto"} or self.substation_topology not in {"balanced", "skewed"}:
            raise ValueError("invalid topology mode")


@dataclass
class SimulationResult:
    config: dict[str, Any]
    series: list[dict[str, Any]]
    metrics: dict[str, float]
    topology: dict[str, Any]


def _weighted_choice(rng: random.Random, weights: list[float]) -> int:
    target = rng.random() * sum(weights)
    for index, weight in enumerate(weights):
        target -= weight
        if target <= 0:
            return index
    return len(weights) - 1


def _topology(cfg: SimulationConfig, rng: random.Random) -> tuple[list[int], list[int]]:
    if cfg.aggregator_topology == "uniform":
        a_weights = [1.0] * cfg.aggregators
    else:
        a_weights = [1.0 / ((i + 1) ** cfg.pareto_alpha) for i in range(cfg.aggregators)]
    if cfg.substations == 1:
        s_weights = [1.0]
    elif cfg.substation_topology == "balanced":
        s_weights = [1.0] * cfg.substations
    else:
        s_weights = [cfg.skew] + [(1.0 - cfg.skew) / (cfg.substations - 1)] * (cfg.substations - 1)
    return ([_weighted_choice(rng, a_weights) for _ in range(cfg.prosumers)],
            [_weighted_choice(rng, s_weights) for _ in range(cfg.prosumers)])


def _demand_profile(cfg: SimulationConfig, rng: random.Random) -> tuple[list[list[float]], list[list[float]]]:
    actual: list[list[float]] = []
    renewable: list[list[float]] = []
    household = [rng.uniform(0.65, 1.35) for _ in range(cfg.prosumers)]
    solar = [rng.uniform(0.05, 0.60) for _ in range(cfg.prosumers)]
    phase = [rng.uniform(-0.15, 0.15) for _ in range(cfg.prosumers)]
    for t in range(cfg.steps):
        hour = (t % 96) / 96 * 24
        day = 0.84 + 0.17 * math.sin((hour - 7) * math.pi / 12) + 0.12 * math.sin((hour - 18) * math.pi / 6)
        daylight = max(0.0, math.sin((hour - 6) * math.pi / 12))
        actual.append([max(0.1, household[i] * day * (1 + phase[i]) * rng.uniform(0.96, 1.04)) for i in range(cfg.prosumers)])
        renewable.append([solar[i] * daylight for i in range(cfg.prosumers)])
    return actual, renewable


def _reported_loads(cfg: SimulationConfig, t: int, actual: list[float], aggregator: list[int], substation: list[int], rng: random.Random, prior: list[float]) -> tuple[list[float], list[float]]:
    report = actual.copy()
    active = cfg.attack_start <= t < cfg.attack_end and cfg.attack != "none"
    if not active:
        return report, [0.0] * cfg.prosumers
    attacked = [i for i, agg in enumerate(aggregator) if agg == cfg.compromised_aggregator]
    delta = min(cfg.attack_strength, 0.95)
    if cfg.attack == "inflation":
        for i in attacked: report[i] *= 1 + delta
    elif cfg.attack == "deflation":
        for i in attacked: report[i] *= max(0.01, 1 - delta)
    elif cfg.attack == "hybrid":
        # Topology-aware, aggregate-stealth manipulation: shift reported load
        # from one physical substation's cohort to another while preserving the
        # compromised aggregator's total as closely as the bounded multipliers allow.
        cohorts = [[i for i in attacked if substation[i] == s] for s in range(cfg.substations)]
        cohorts = [cohort for cohort in cohorts if cohort]
        if len(cohorts) >= 2:
            high = max(cohorts, key=lambda group: sum(actual[i] for i in group))
            low = min(cohorts, key=lambda group: sum(actual[i] for i in group))
            high_load = sum(actual[i] for i in high)
            low_load = sum(actual[i] for i in low)
            shifted = min(delta * high_load, delta * low_load)
            for i in high: report[i] += actual[i] * shifted / high_load
            for i in low: report[i] -= actual[i] * shifted / low_load
    elif cfg.attack == "replay":
        for i in attacked: report[i] = prior[i]
    elif cfg.attack == "noise":
        for i in attacked: report[i] *= rng.uniform(1 - delta, 1 + delta)
    elif cfg.attack == "ramp":
        progress = (t - cfg.attack_start + 1) / max(1, cfg.attack_end - cfg.attack_start)
        for i in attacked: report[i] *= 1 + delta * progress
    elif cfg.attack == "outage":
        for i in attacked: report[i] = 0.0
    return report, [report[i] - actual[i] for i in range(cfg.prosumers)]


def run_simulation(config: SimulationConfig | None = None) -> SimulationResult:
    """Run paired secure and compromised cases on the same seeded topology/load."""
    cfg = config or SimulationConfig()
    cfg.validate()
    rng = random.Random(cfg.seed)
    aggregator, substation = _topology(cfg, rng)
    actual, renewables = _demand_profile(cfg, rng)
    prior = actual[0].copy()
    battery_capacity = [0.0] * cfg.substations
    battery_state = [0.0] * cfg.substations
    for s in range(cfg.substations):
        station_load = sum(actual[0][i] for i in range(cfg.prosumers) if substation[i] == s)
        battery_capacity[s] = station_load * cfg.battery_share * cfg.battery_hours
        battery_state[s] = battery_capacity[s] * 0.5

    series: list[dict[str, Any]] = []
    for t in range(cfg.steps):
        reports, _ = _reported_loads(cfg, t, actual[t], aggregator, substation, rng, prior)
        prior = actual[t].copy()
        secure_demand = [0.0] * cfg.substations
        attacked_demand = [0.0] * cfg.substations
        renewable = [0.0] * cfg.substations
        for i in range(cfg.prosumers):
            s = substation[i]
            secure_demand[s] += actual[t][i]
            attacked_demand[s] += reports[i]
            renewable[s] += renewables[t][i]
        # Bounded forecast error applies identically to both paired cases.
        # One forecast realization per substation, shared by the secure and
        # attacked cases so the paired comparison isolates the attack effect.
        forecast_noise = [rng.uniform(-cfg.forecast_error, cfg.forecast_error) for _ in range(cfg.substations)]
        secure_generation = [max(0.0, secure_demand[s] * cfg.safety_margin * (1 + forecast_noise[s])) for s in range(cfg.substations)]
        attacked_generation = [max(0.0, attacked_demand[s] * cfg.safety_margin * (1 + forecast_noise[s])) for s in range(cfg.substations)]
        actual_generation = [sum(secure_generation), sum(attacked_generation)]
        actual_load = sum(actual[t])
        loss = actual_load * cfg.line_loss_rate

        # Energy storage is local to each substation and discharges only against
        # a real power deficit; surplus charging is limited by remaining capacity.
        supplies = [max(0.0, attacked_generation[s] + renewable[s] - secure_demand[s] * (1 + cfg.line_loss_rate)) for s in range(cfg.substations)]
        deficits = [max(0.0, secure_demand[s] * (1 + cfg.line_loss_rate) - attacked_generation[s] - renewable[s]) for s in range(cfg.substations)]
        discharge = [min(deficits[s], battery_state[s] / cfg.timestep_hours) for s in range(cfg.substations)]
        for s in range(cfg.substations): battery_state[s] -= discharge[s] * cfg.timestep_hours
        deficits = [max(0.0, deficits[s] - discharge[s]) for s in range(cfg.substations)]
        charge = [min(supplies[s], (battery_capacity[s] - battery_state[s]) / cfg.timestep_hours) for s in range(cfg.substations)]
        for s in range(cfg.substations):
            battery_state[s] += charge[s] * cfg.timestep_hours
            supplies[s] -= charge[s]
        transfers = 0.0
        if cfg.redistribution and cfg.substations > 1:
            for receiver in range(cfg.substations):
                for donor in range(cfg.substations):
                    if receiver == donor or deficits[receiver] <= 1e-9: continue
                    moved = min(deficits[receiver], supplies[donor] * cfg.line_reliability)
                    if moved > 0:
                        supplies[donor] -= moved / cfg.line_reliability
                        deficits[receiver] -= moved
                        transfers += moved
        outage_count = sum(1 for d in deficits if d > 1e-9)
        unserved = sum(deficits)
        net_available = sum(attacked_generation) + sum(renewable) - loss
        nsr = (net_available - actual_load) / max(actual_load, 1e-9)
        rc = transfers ** cfg.redistribution_exponent * cfg.redistribution_distance_km / cfg.line_reliability
        series.append({
            "timestep": t, "actual_demand": actual_load, "reported_demand": sum(reports),
            "secure_generation": actual_generation[0], "generated_power": actual_generation[1],
            "renewable_power": sum(renewable), "line_losses": loss, "unserved_energy": unserved * cfg.timestep_hours,
            "storage_charge": sum(charge) * cfg.timestep_hours, "storage_discharge": sum(discharge) * cfg.timestep_hours,
            "outage_substations": outage_count, "redistributed_power": transfers,
            "redistribution_cost": rc, "net_surplus_ratio": nsr,
            "attack_active": int(cfg.attack_start <= t < cfg.attack_end and cfg.attack != "none"),
            "por_event": int(nsr < cfg.nsr_threshold),
        })

    attack_rows = [row for row in series if row["attack_active"]]
    window = attack_rows or series
    baseline_generation = sum(row["secure_generation"] for row in window)
    dn = sum(abs(row["secure_generation"] - row["generated_power"]) for row in window) / max(baseline_generation, 1e-9)
    metrics = {
        "deviation_from_nominal": dn,
        "power_outage_count": sum(row["outage_substations"] for row in window) / max(1, len(window)),
        "outage_events": float(sum(row["outage_substations"] for row in window)),
        "unserved_energy": sum(row["unserved_energy"] for row in window),
        "redistribution_cost": sum(row["redistribution_cost"] for row in window),
        "redistributed_power": sum(row["redistributed_power"] for row in window),
        "potential_outage_risk": sum(row["por_event"] for row in window) / max(1, len(window)),
        "average_report_error": sum(abs(row["reported_demand"] - row["actual_demand"]) for row in window) / max(1, len(window)),
        "energy_waste": sum(max(0.0, row["generated_power"] + row["renewable_power"] - row["actual_demand"] - row["line_losses"]) * cfg.timestep_hours for row in window),
    }
    agg_counts = [aggregator.count(a) for a in range(cfg.aggregators)]
    station_counts = [substation.count(s) for s in range(cfg.substations)]
    topology = {
        "aggregator_prosumers": agg_counts,
        "substation_prosumers": station_counts,
        "compromised_aggregator_share": agg_counts[cfg.compromised_aggregator] / cfg.prosumers,
        "joint_counts": [[sum(1 for i in range(cfg.prosumers) if aggregator[i] == a and substation[i] == s) for s in range(cfg.substations)] for a in range(cfg.aggregators)],
    }
    return SimulationResult(asdict(cfg), series, metrics, topology)
