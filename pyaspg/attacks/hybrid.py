"""Topology-aware hybrid false-data injection helpers."""

from numbers import Real

from pyaspg.attacks.deflate import deflation_attack
from pyaspg.attacks.inflate import inflation_attack


def hybrid_attack(net_power, **kwargs):
    """Apply bounded, aggregate-stealth manipulation across substation cohorts.

    For backward compatibility, a scalar retains the old criteria-based
    inflation/deflation behavior. For a sequence, pass ``substation_ids`` and
    optionally ``aggregator_ids`` plus ``compromised_aggregator``. One
    substation cohort is inflated while another is deflated by the same total
    amount, preserving the compromised aggregator's aggregate report.

    Args:
        net_power: A scalar (legacy API) or one load value per prosumer.
        substation_ids: Physical substation assignment for each prosumer.
        aggregator_ids: Aggregator assignment for each prosumer. Defaults to
            assigning every prosumer to the compromised aggregator.
        compromised_aggregator: Aggregator identifier to manipulate.
        deviation: Maximum fractional change for either cohort (default 0.1).

    Returns:
        A scalar for the legacy API, or a list of manipulated load values.
    """
    if isinstance(net_power, Real):
        if kwargs.get("criteria", True):
            return inflation_attack(net_power, inflation_rate=kwargs.get("inflation_rate", 1.1))
        return deflation_attack(net_power, deflation_rate=kwargs.get("deflation_rate", 0.9))

    values = [float(value) for value in net_power]
    stations = kwargs.get("substation_ids")
    if stations is None or len(stations) != len(values):
        raise ValueError("sequence input requires one substation_id per prosumer")
    aggregators = kwargs.get("aggregator_ids", [kwargs.get("compromised_aggregator", 0)] * len(values))
    if len(aggregators) != len(values):
        raise ValueError("aggregator_ids must have the same length as net_power")
    compromised = kwargs.get("compromised_aggregator", 0)
    deviation = float(kwargs.get("deviation", 0.1))
    if not 0 <= deviation <= 0.95:
        raise ValueError("deviation must be in [0, 0.95]")

    cohorts = {}
    for index, (agg, station) in enumerate(zip(aggregators, stations)):
        if agg == compromised:
            cohorts.setdefault(station, []).append(index)
    nonempty = [indices for indices in cohorts.values() if indices]
    if len(nonempty) < 2 or deviation == 0:
        return values
    inflate = max(nonempty, key=lambda indices: sum(values[i] for i in indices))
    deflate = min(nonempty, key=lambda indices: sum(values[i] for i in indices))
    inflate_total = sum(values[i] for i in inflate)
    deflate_total = sum(values[i] for i in deflate)
    if inflate_total <= 0 or deflate_total <= 0:
        return values
    shifted = min(deviation * inflate_total, deviation * deflate_total)
    for index in inflate:
        values[index] += values[index] * shifted / inflate_total
    for index in deflate:
        values[index] -= values[index] * shifted / deflate_total
    return values
