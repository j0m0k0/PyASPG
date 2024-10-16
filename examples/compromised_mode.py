import random
import numpy as np
import pandas as pd

import pyaspg as pya


DURATION = 240
TIMESTEP = 1
NUMBER_OF_PROSUMERS = 5000
NUMBER_OF_AGGREGATORS = 5
CONTROL_CLOCK = 1
ALPHA = 10.0

# aggregator_weights = [0.2, 0.2, 0.2, 0.2, 0.2]
aggregator_weights = pya.utils.distribute_pareto(alpha=ALPHA, num_classes=NUMBER_OF_AGGREGATORS)

# Correct Name: Distribution Substations and Transmission Substations
distributor_weights = [0.5, 0.5]

BIAS_CONSTANT = 40
SIGN_CONSTANT = [-1, 1]
ATTACKED = True
# Replay Mode new variables
REPLAY_PATH = f"./simulation_results/dataset2/pareto-10/pareto-secure-{'ideal' if ATTACKED else 'echo'}/"

prosumers_df = pd.read_csv(REPLAY_PATH + "prosumers.csv")
aggregators_df = pd.read_csv(REPLAY_PATH + "aggregators.csv")
control_system_df = pd.read_csv(REPLAY_PATH + "control_systems.csv")
utility_companies_df = pd.read_csv(REPLAY_PATH + "utility_companies.csv")

assert 1 - sum(aggregator_weights) <  0.000000001
assert sum(distributor_weights) == 1

control_system = pya.ControlSystem(name="CS1", safety_margin=1.1, uc_frame=utility_companies_df, cs_frame=control_system_df, error_rate=0.05)

wind_turbine = pya.WindTurbine(name="G1", nominal_capacity=11200000, voltage=25000, controller=control_system)
wind_turbine2 = pya.WindTurbine(name="G2", nominal_capacity=55000000, voltage=25000, controller=control_system)
wind_turbine3 = pya.WindTurbine(name="G3", nominal_capacity=12300000, voltage=25000, controller=control_system)
wind_turbine4 = pya.WindTurbine(name="G4", nominal_capacity=52000000, voltage=25000, controller=control_system)

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


wind_speed = np.random.rand(DURATION // TIMESTEP)
d_to_p = []
p_to_m = []
m_to_a = []
a_to_u = []
aggregators_list = []

# New Weighted Round-Robin Style
aggregators_list = []
for i in range(NUMBER_OF_AGGREGATORS):
    if ATTACKED:
        temp_comp = [0]
        aggregators_list.append(pya.NetAggregator(name=f"NA{i+1}", compromised=True if i in temp_comp else False, attack_method=pya.attacks.inflate.inflation_attack, compromise_start_time=80, compromise_duration=20, control_system=control_system))
    else:
        temp_comp = []
        aggregators_list.append(pya.NetAggregator(name=f"NA{i+1}"))
    

print("Compromised NAs:")
for agg in aggregators_list:
    if agg.compromised:
        print(agg.name)
smart_meters = []

for i, row in prosumers_df.iterrows():
    _h = pya.Prosumer(
        name=row['name'],
        replay_mode=True,
        prosumer_type=row['prosumer_type'],
        storage_capacity=row['storage_capacity'],
        replay_frame=prosumers_df[prosumers_df["name"] == row["name"]],
        distributor_name=row['distributor_name'],
        bias=0,
        production_pattern=(0, 0)
        )

    _m = pya.SmartMeter(prosumer=_h, communication_network=communication_network)
    smart_meters.append(_m)

    if i == NUMBER_OF_PROSUMERS:
        break

    # d_to_p.append((distributor, _h))
    # TODO: This part should be fixed
    d_to_p.append((distributor if row['distributor_name'] == distributor.name else distributor2, _h))
    p_to_m.append((_h, _m))


pya.RR_distribution.load_smart_meter_assignments(aggregators_list, smart_meters, aggregators_df=aggregators_df[aggregators_df['timestep'] == 0])


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
simulator.run_simulation(
    duration=DURATION, timestep=TIMESTEP, control_clock=CONTROL_CLOCK,
    output_dir='simulation_results',
    replay_mode=True,
    attacked=ATTACKED,)
