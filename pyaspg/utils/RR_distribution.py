# Distribute Prosumers among Net Aggregators in a fair way of receiving power from the grid.

import itertools
import random
import ast
import pyaspg as pya


def load_smart_meter_assignments(aggregators_list, smart_meters, aggregators_df=None):
    if aggregators_df is not None:
        # Ensure that the dataframe contains the required columns
        required_columns = {'name', 'prosumers'}
        if not required_columns.issubset(aggregators_df.columns):
            raise ValueError(f"Dataframe must contain the following columns: {required_columns}")
        
        # Loop through each row in the dataframe
        for index, row in aggregators_df.iterrows():
            # Find the corresponding net aggregator by its name
            aggregator_name = row['name']
            aggregator = next((agg for agg in aggregators_list if agg.name == aggregator_name), None)
            
            if aggregator is None:
                raise ValueError(f"Aggregator with name {aggregator_name} not found in the provided list.")
            
            # Convert the prosumers string to an actual list
            prosumers_list = ast.literal_eval(row['prosumers'])            
            
            # Assign the corresponding smart meters to the aggregator
            for prosumer_name in prosumers_list:
                # Find the smart meter corresponding to the prosumer name
                smart_meter = next((sm for sm in smart_meters if sm.prosumer.name == prosumer_name), None)
                
                if smart_meter is None:
                    raise ValueError(f"Smart meter for prosumer {prosumer_name} not found in the provided list.")
                
                # Add the smart meter to the aggregator
                aggregator.add_smart_meter(smart_meter)

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
