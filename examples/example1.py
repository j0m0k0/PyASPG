from pyaspg.simulation import PyASPGCreator, GridSimulator
from pyaspg.distribution import Transmitter, Distributor, Substation
from pyaspg.prosume import Household
from pyaspg.generation import WindTurbine, SolarPanel
from pyaspg.communication import CommunicationNetwork, SmartMeter
from pyaspg.management import NetAggregator, UtilityCompany, ControlSystem


grid_creator = PyASPGCreator()

# Create components
household = Household(name="Household 1", storage_capacity=5000)
communication_network = CommunicationNetwork(name="Smart Grid Network", reliability=0.99)
smart_meter = SmartMeter(prosumer=household, communication_network=communication_network)
aggregator = NetAggregator(name="Data Aggregator 1")
utility_company = UtilityCompany(name="Utility Company 1")
control_system = ControlSystem(name="Control System 1")

wind_turbine = WindTurbine(name="Wind Turbine 1", nominal_capacity=200000000, voltage=25000)
solar_panel = SolarPanel(name="Solar Panel 1", nominal_capacity=100000000, voltage=25000)

transmitter = Transmitter(name="High Voltage Line 1", efficiency=0.97, distance=100)
distributor = Distributor(name="Low Voltage Line 1", efficiency=0.9, distance=10)
substation = Substation(name="Main Substation", input_voltage=25000, output_voltage=10000, efficiency=0.98)

# Define connections between components with parameters
grid_creator.define_connections(
    generator_to_transmitter=[
        (wind_turbine, transmitter, {'wind_speed': [0.8, 0.6, 0.7, 0.5]}),
        # (solar_panel, transmitter, {'sunlight': [0.8, 0.9, 0.7, 0.6]})
    ],
)

# Run the simulation
simulator = GridSimulator(grid_creator, output_dir='simulation_results')
simulator.run_simulation(duration=30, timestep=10, output_dir='simulation_results')
