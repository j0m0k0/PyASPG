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
from pyaspg.utils import log_me


@log_me
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
