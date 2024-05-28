# grid_simulator.py
import os
import csv
import simpy
from pyaspg.management.control_system import ControlSystem
from pyaspg.management.net_aggregator import NetAggregator
from pyaspg.management.utility_company import UtilityCompany
from pyaspg.communication.smart_meter import SmartMeter
from pyaspg.communication.communication_network import CommunicationNetwork
from pyaspg.prosume.household import Household, Prosumer
from pyaspg.generation.power_plant import PowerPlant
from pyaspg.generation.solar_panel import SolarPanel
from pyaspg.generation.wind_turbine import WindTurbine
from pyaspg.distribution.transmitter import Transmitter
from pyaspg.distribution.distributor import Distributor
from pyaspg.distribution.substation import Substation
from pyaspg.simulation.grid_creator import PyASPGCreator
from pyaspg.simulation.data_log import DataLog
from pyaspg.simulation.connection_handler import GeneratorToTransmitterHandler, TransmitterToSubstationHandler

class GridSimulator:
    def __init__(self, creator: PyASPGCreator, output_dir: str):
        self.creator = creator
        self.data_log = DataLog(output_dir)
        self.connection_handlers = {
            'generator_to_transmitter': GeneratorToTransmitterHandler(),
            'transmitter_to_substation': TransmitterToSubstationHandler(),
            # Add other connection handlers here...
        }

    def run_simulation(self, duration, timestep, output_dir):
        env = simpy.Environment()
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        components = self.creator.components
        connections = self.creator.connections

        # Create a CSV file for each component type
        self.data_log.initialize_files(components, connections)

        def log_and_handle(t):
            for connection_type, connection_list in connections.items():
                handler = self.connection_handlers.get(connection_type)
                if handler:
                    for source, target, params in connection_list:
                        handler.handle_connection(source, target, params, t // timestep)

            self.data_log.log_data(t, components, connections)

        def run_simulation_step(env):
            while True:
                log_and_handle(env.now)
                yield env.timeout(timestep)
        
        env.process(run_simulation_step(env))
        env.run(until=duration)

        # Close CSV files
        self.data_log.close_files()

def main():
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
        # transmitter_to_substation=[(transmitter, substation, {})],
        # substation_to_distributor=[(substation, distributor, {})],
        # distributor_to_prosumer=[(distributor, household, {})],
        # prosumer_to_smart_meter=[(household, smart_meter, {})],
        # smart_meter_to_aggregator=[(smart_meter, aggregator, {})],
        # aggregator_to_utility=[(aggregator, utility_company, {})],
        # utility_to_control=[(utility_company, control_system, {})]
    )

    # Create the smart grid
    grid_creator.create_smart_grid()

    # Run the simulation
    simulator = GridSimulator(grid_creator, output_dir='simulation_results')
    simulator.run_simulation(duration=30, timestep=10, output_dir='simulation_results')

if __name__ == "__main__":
    main()
