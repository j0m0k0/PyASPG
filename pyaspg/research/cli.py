"""Command-line entry point for paper-inspired simulations."""

import argparse

from .report import render_report
from .simulator import SimulationConfig, run_simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a reproducible PyASPG topology-aware FDIA scenario")
    parser.add_argument("--attack", choices=["none", "inflation", "deflation", "hybrid", "replay", "noise", "ramp", "outage"], default="hybrid")
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--prosumers", type=int, default=240)
    parser.add_argument("--aggregators", type=int, default=5)
    parser.add_argument("--substations", type=int, default=2)
    parser.add_argument("--attack-start", type=int, default=80)
    parser.add_argument("--attack-end", type=int, default=100)
    parser.add_argument("--strength", type=float, default=0.10)
    parser.add_argument("--topology", choices=["uniform", "pareto"], default="pareto")
    parser.add_argument("--substation-topology", choices=["balanced", "skewed"], default="skewed")
    parser.add_argument("--safety-margin", type=float, default=1.10)
    parser.add_argument("--no-redistribution", action="store_true")
    parser.add_argument("--battery-share", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="simulation_results/paper_demo")
    args = parser.parse_args()
    config = SimulationConfig(
        steps=args.steps, prosumers=args.prosumers, aggregators=args.aggregators,
        substations=args.substations, attack=args.attack, attack_start=args.attack_start,
        attack_end=args.attack_end, attack_strength=args.strength,
        aggregator_topology=args.topology, substation_topology=args.substation_topology,
        safety_margin=args.safety_margin, redistribution=not args.no_redistribution,
        battery_share=args.battery_share, seed=args.seed,
    )
    result = run_simulation(config)
    report = render_report(result, args.output)
    print(f"Report: {report}")
    for key, value in result.metrics.items(): print(f"{key}: {value:.5g}")


if __name__ == "__main__":
    main()
