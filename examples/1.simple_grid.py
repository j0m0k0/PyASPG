import random
import numpy as np

import pyaspg as pya


DURATION = 24*60
TIMESTEP = 1
NUMBER_OF_PROSUMERS = 3
NUMBER_OF_AGGREGATORS = 2

wind_turbine = pya.WindTurbine(name="Generator1", nominal_capacity=50000, voltage=25000)
solar_panel = pya.SolarPanel(name="Generator2", nominal_capacity=100000000, voltage=25000)
transmitter = pya.Transmitter(name="Transmitter1", efficiency=0.97, distance=100)
substation = pya.Substation(name="Substation1", input_voltage=25000, output_voltage=10000, efficiency=0.98)
distributor = pya.Distributor(name="Distributor1", efficiency=0.9, distance=10)
communication_network = pya.CommunicationNetwork(name="SGN", reliability=1.0)
utility_company = pya.UtilityCompany(name="UC1")

wind_speed = np.random.rand(DURATION // TIMESTEP)
d_to_p = []
p_to_m = []
m_to_a = []
a_to_u = []
aggregators_list = []

for j in range(NUMBER_OF_AGGREGATORS):
    _a = pya.NetAggregator(name=f"NA{j+1}")
    aggregators_list.append(_a)

for i in range(NUMBER_OF_PROSUMERS):
    _h = pya.Prosumer(name=f"H{i+1}", prosumer_type="House", storage_capacity=5000, consumption_file="consumption_patterns/2006-12-16.csv", bias=(i+1)*5, production_pattern=(600, 150))
    _m = pya.SmartMeter(prosumer=_h, communication_network=communication_network)
    _selected_a = aggregators_list[random.randint(0, (NUMBER_OF_AGGREGATORS - 1))]
    d_to_p.append((distributor, _h))
    p_to_m.append((_h, _m))
    m_to_a.append((_m, _selected_a))
    a_to_u.append((_selected_a, utility_company))

# control_system = ControlSystem(name="CS1")

# Define connections between components with parameters
my_grid = pya.PyASPGCreator()
my_grid.define_connections(
    generator_to_transmitter=[
        (wind_turbine, transmitter, {'wind_speed': wind_speed}),        
    ],
    transmitter_to_substation=[(transmitter, substation)],
    substation_to_distributor=[(substation, distributor)],
    distributor_to_prosumer=d_to_p,
    prosumer_to_smart_meter=p_to_m,
    smart_meter_to_aggregator=m_to_a,
    aggregator_to_utility=a_to_u,
    # utility_to_control=[],
)

# Run the simulation
simulator = pya.GridSimulator(my_grid)
simulator.run_simulation(duration=DURATION, timestep=TIMESTEP, output_dir='simulation_results')
