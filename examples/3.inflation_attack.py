import math
import random
import numpy as np

import pyaspg as pya


DURATION = 120
TIMESTEP = 1
NUMBER_OF_PROSUMERS = 200
NUMBER_OF_AGGREGATORS = 5
CONTROL_CLOCK = 1
aggregator_weights = [0.4, 0.2, 0.1, 0.25, 0.05]
distributor_weights = [0.78, 0.22]
BIAS_CONSTANT = 400
SIGN_CONSTANT = [-1, 1]
control_system = pya.ControlSystem(name="CS1", safety_margin=1)

assert sum(aggregator_weights) == 1
assert sum(distributor_weights) == 1

wind_turbine = pya.WindTurbine(name="G1", nominal_capacity=200000, voltage=25000, controller=control_system)
wind_turbine2 = pya.WindTurbine(name="G2", nominal_capacity=150000, voltage=25000, controller=control_system)
wind_turbine3 = pya.WindTurbine(name="G3", nominal_capacity=220000, voltage=25000, controller=control_system)
wind_turbine4 = pya.WindTurbine(name="G4", nominal_capacity=180000, voltage=25000, controller=control_system)

transmitter = pya.Transmitter(name="T1", efficiency=1.0, distance=100, generators=[wind_turbine, wind_turbine2])
transmitter2 = pya.Transmitter(name="T2", efficiency=1.0, distance=100, generators=[wind_turbine3, wind_turbine4])

substation = pya.Substation(name="S1", input_voltage=25000, output_voltage=10000, efficiency=1.0)
substation2 = pya.Substation(name="S2", input_voltage=25000, output_voltage=10000, efficiency=1.0)

distributor = pya.Distributor(name="D1", efficiency=1.0, distance=10)
distributor2 = pya.Distributor(name="D2", efficiency=1.0, distance=10)

communication_network = pya.CommunicationNetwork(name="SGN", reliability=1.0)

utility_company = pya.UtilityCompany(name="UC1", generators=[wind_turbine, wind_turbine2, wind_turbine3, wind_turbine4]) # This is correct
control_system.register_utility_company(utility_company)

# utility_company2 = pya.UtilityCompany(name="UC2")
# utility_company3 = pya.UtilityCompany(name="UC3")


DISTRIBUTORS = [distributor, distributor2]

wind_speed = np.random.rand(DURATION // TIMESTEP)
d_to_p = []
p_to_m = []
m_to_a = []
a_to_u = []
aggregators_list = []

# New Weighted Round-Robin Style
aggregators_list = []
for i in range(NUMBER_OF_AGGREGATORS):
    temp_comp = [0]
    # aggregators_list.append(pya.NetAggregator(name=f"NA{i+1}", compromised=True if i in temp_comp else False, attack_method=pya.attacks.inflate.inflation_attack))
    aggregators_list.append(pya.NetAggregator(name=f"NA{i+1}"))

# print("Compromised NAs:")
for agg in aggregators_list:
    if agg.compromised:
        print(agg.name)

smart_meters = []

# Calculate the exact number of prosumers for each distributor
num_prosumers = NUMBER_OF_PROSUMERS
num_prosumers_per_distributor = [math.floor(weight * num_prosumers) for weight in distributor_weights]

# Ensure the sum matches exactly by adjusting the last one
num_prosumers_per_distributor[-1] = num_prosumers - sum(num_prosumers_per_distributor[:-1])

assert sum(num_prosumers_per_distributor) == NUMBER_OF_PROSUMERS

distributor_assignments = []
for i, num in enumerate(num_prosumers_per_distributor):
    distributor_assignments.extend([DISTRIBUTORS[i]] * num)

# Shuffle the distributor_assignments list to distribute prosumers randomly but exactly
random.shuffle(distributor_assignments)

for i in range(NUMBER_OF_PROSUMERS):
    random_bias = random.random() * BIAS_CONSTANT * random.choice(SIGN_CONSTANT)
    _h = pya.Prosumer(
        name=f"H{i+1}",
        prosumer_type="House",
        storage_capacity=0,
        consumption_file="consumption_patterns/2010-02-16.csv",
        # bias=(i+1)*5,
        bias=random_bias,
        production_pattern=(0, 0)
    )
    _m = pya.SmartMeter(prosumer=_h, communication_network=communication_network)
    smart_meters.append(_m)

    # NEW: assign prosumers to distributors exactly based on the weight distribution
    distributor = distributor_assignments[i]
    
    d_to_p.append((distributor, _h))
    p_to_m.append((_h, _m))

assert len(d_to_p) == NUMBER_OF_PROSUMERS

pya.RR_distribution.assign_smart_meters(aggregators_list, aggregator_weights, smart_meters)

for aggregator in aggregators_list:
    if len(aggregator.smart_meters) > 0:
        a_to_u.append((aggregator, utility_company))
    
        for meter in aggregator.smart_meters:
            m_to_a.append((meter, aggregator))

# Define connections between components with parameters
my_grid = pya.PyASPGCreator()
my_grid.define_connections(
    generator_to_transmitter=[
        (wind_turbine, transmitter),
        (wind_turbine2, transmitter),
        (wind_turbine3, transmitter2),
        # (wind_turbine3, transmitter),
        (wind_turbine4, transmitter2),
    ],
    transmitter_to_substation=[(transmitter, substation), (transmitter2, substation2)],
    substation_to_distributor=[(substation, distributor), (substation2, distributor2)],
    distributor_to_prosumer=d_to_p,
    prosumer_to_smart_meter=p_to_m,
    smart_meter_to_aggregator=m_to_a,
    aggregator_to_utility=a_to_u,
    utility_to_control=[(utility_company, control_system)],
)

# Run the simulation
simulator = pya.GridSimulator(my_grid)
simulator.run_simulation(duration=DURATION, timestep=TIMESTEP, control_clock=CONTROL_CLOCK, output_dir='simulation_results', replay_mode=False)
