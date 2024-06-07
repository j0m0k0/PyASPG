from pyaspg.simulation import PyASPGCreator, GridSimulator
from pyaspg.distribution import Transmitter, Distributor, Substation
from pyaspg.prosume import Prosumer
from pyaspg.generation import WindTurbine, SolarPanel
from pyaspg.communication import CommunicationNetwork, SmartMeter
from pyaspg.management import NetAggregator, UtilityCompany, ControlSystem


grid_creator = PyASPGCreator()

# Create components

wind_turbine = WindTurbine(name="WT1", nominal_capacity=2000, voltage=25000)
solar_panel = SolarPanel(name="SP1", nominal_capacity=100000000, voltage=25000)
transmitter = Transmitter(name="HVL1", efficiency=0.97, distance=100)
substation = Substation(name="MS1", input_voltage=25000, output_voltage=10000, efficiency=0.98)
distributor = Distributor(name="LVL1", efficiency=0.9, distance=10)


p_to_d = []
for i in range(1):
    _h = Prosumer(name=f"H{i+1}", prosumer_type="House", storage_capacity=5000, consumption_file="consumption_patterns/2006-12-16.csv", bias=(i+1)*5, production_pattern=(600, 150))
    p_to_d.append((distributor, _h))

# communication_network = CommunicationNetwork(name="SGN", reliability=0.99)
# aggregator = NetAggregator(name="NA1")
# utility_company = UtilityCompany(name="UC1")
# control_system = ControlSystem(name="CS1")
# smart_meter = SmartMeter(prosumer=household, communication_network=communication_network)

# Define connections between components with parameters
grid_creator.define_connections(
    generator_to_transmitter=[
        (wind_turbine, transmitter, {'wind_speed': [0.8, 0.6, 0.7]}),
        # (solar_panel, transmitter, {'sunlight': [0.8, 0.9, 0.7, 0.6]})
    ],
    transmitter_to_substation=[(transmitter, substation)],
    substation_to_distributor=[(substation, distributor)],
    distributor_to_prosumer=p_to_d
)

# Run the simulation
simulator = GridSimulator(grid_creator)
simulator.run_simulation(duration=30, timestep=10, output_dir='simulation_results')
