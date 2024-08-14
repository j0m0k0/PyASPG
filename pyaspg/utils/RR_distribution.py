# Distribute Prosumers among Net Aggregators in a fair way of receiving power from the grid.

import itertools
import random
import pyaspg as pya

def assign_smart_meters(aggregators_list, aggregator_weights, smart_meters_list):
    # Ensure that the lengths of aggregators_list and aggregator_weights match
    assert len(aggregators_list) == len(aggregator_weights), "Mismatch between aggregators and weights."
    assert abs(sum(aggregator_weights) - 1.0) < 1e-6, "Weights should sum up to 1.0."

    random.shuffle(smart_meters_list)
    
    # Calculate the number of items (smart meters) each aggregator should ideally get
    num_smart_meters = len(smart_meters_list)
    weighted_counts = [round(weight * num_smart_meters) for weight in aggregator_weights]

    # Create a weighted round-robin iterator
    weighted_aggregators = [
        aggregator for aggregator, count in zip(aggregators_list, weighted_counts) for _ in range(count)
    ]

    # Ensure the round-robin can handle leftover smart meters due to rounding
    while len(weighted_aggregators) < num_smart_meters:
        weighted_aggregators.append(aggregators_list[len(weighted_aggregators) % len(aggregators_list)])

    # Assign smart meters to aggregators
    for smart_meter, aggregator in zip(smart_meters_list, itertools.cycle(weighted_aggregators)):
        aggregator.add_smart_meter(smart_meter)


# Example data
# aggregators = [pya.NetAggregator(name=f"NA{i+1}") for i in range(2)]
# print(aggregators)
# weights = [0.6, 0.4]
# smart_meters = [pya.SmartMeter(prosumer=pya.Prosumer(name=f'H{i+1}'), communication_network=None) for i in range(100)]


# # Call the function
# assign_smart_meters(aggregators, weights, smart_meters)

# # Output the result
# for aggregator in aggregators:
#     print("X")
#     print([i.prosumer.name for i in aggregator.smart_meters])
