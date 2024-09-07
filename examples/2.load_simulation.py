import random
import numpy as np
import pandas as pd

import pyaspg as pya


DURATION = 30
TIMESTEP = 1
NUMBER_OF_PROSUMERS = 100
NUMBER_OF_AGGREGATORS = 5
CONTROL_CLOCK = 1
aggregator_weights = [0.02, 0.08, 0.7, 0.05, 0.15]
# Replay Mode new variables
REPLAY_PATH = './simulation_results/01-09-2024-1/'
prosumers_df = pd.read_csv(REPLAY_PATH + "prosumers.csv")
aggregators_df = pd.read_csv(REPLAY_PATH + "aggregators.csv")
control_system_df = pd.read_csv(REPLAY_PATH + "control_systems.csv")

control_system = pya.ControlSystem(name="CS1", safety_margin=1.1, cs_frame=control_system_df)

wind_turbine = pya.WindTurbine(name="G1", nominal_capacity=500000000, voltage=25000, controller=control_system)
wind_turbine2 = pya.WindTurbine(name="G2", nominal_capacity=80000000, voltage=25000, controller=control_system)
wind_turbine3 = pya.WindTurbine(name="G3", nominal_capacity=40000000, voltage=25000, controller=control_system)
wind_turbine4 = pya.WindTurbine(name="G4", nominal_capacity=10000000, voltage=25000, controller=control_system)

transmitter = pya.Transmitter(name="T1", efficiency=1.0, distance=100, generators=[wind_turbine, wind_turbine2, wind_turbine3, wind_turbine4])
# transmitter2 = pya.Transmitter(name="T2", efficiency=1.0, distance=100, generators=[wind_turbine3])

substation = pya.Substation(name="S1", input_voltage=25000, output_voltage=10000, efficiency=1.0)

distributor = pya.Distributor(name="D1", efficiency=1.0, distance=10)

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
aggregators_list = [pya.NetAggregator(name=f"NA{i+1}") for i in range(NUMBER_OF_AGGREGATORS)]
smart_meters = []

for i, row in prosumers_df.iterrows():
    _h = pya.Prosumer(
        name=row['name'],
        replay_mode=True,
        prosumer_type=row['prosumer_type'],
        storage_capacity=row['storage_capacity'],
        replay_frame=prosumers_df[prosumers_df["name"] == row["name"]],
        distributor_name=row['distributor_name']
        )

    _m = pya.SmartMeter(prosumer=_h, communication_network=communication_network)
    smart_meters.append(_m)

    if i == NUMBER_OF_PROSUMERS:
        break

    d_to_p.append((distributor, _h))
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
        # (wind_turbine3, transmitter2),
        (wind_turbine2, transmitter),
        (wind_turbine3, transmitter),
        (wind_turbine4, transmitter),
    ],
    transmitter_to_substation=[(transmitter, substation)],
    substation_to_distributor=[(substation, distributor)],
    distributor_to_prosumer=d_to_p,
    prosumer_to_smart_meter=p_to_m,
    smart_meter_to_aggregator=m_to_a,
    aggregator_to_utility=a_to_u,
    utility_to_control=[(utility_company, control_system)],
)

# Run the simulation
simulator = pya.GridSimulator(my_grid)
simulator.run_simulation(duration=DURATION, timestep=TIMESTEP, control_clock=CONTROL_CLOCK, output_dir='simulation_results', replay_mode=True)
