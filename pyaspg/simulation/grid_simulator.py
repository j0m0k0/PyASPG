# grid_simulator.py
import os
import csv
from datetime import datetime

import simpy
from tqdm import tqdm
from pyaspg.management import ControlSystem, NetAggregator, UtilityCompany
from pyaspg.communication import SmartMeter, CommunicationNetwork
from pyaspg.prosume import Prosumer
from pyaspg.generation import PowerPlant, SolarPanel, WindTurbine
from pyaspg.distribution import Transmitter, Distributor, Substation
from pyaspg.utils import log_me
from .grid_creator import PyASPGCreator
from .data_log import DataLog

from .connection_handler import (
    GeneratorToTransmitterHandler,
    TransmitterToSubstationHandler,
    SubstationToDistributorHandler,
    DistributorToProsumerHandler,
    ProsumerToSmartMeterHandler,
    SmartMeterToAggregatorHandler,
    AggregatorToUtilityHandler,
    UtilityToControlHandler,
)


@log_me
class GridSimulator:
    """
    The GridSimulator class is responsible for managing and running power grid simulations. It coordinates the interactions between various components
    of the grid such as generators, transmitters, substations, distributors, prosumers, smart meters, and control systems. The simulation can either
    run in a standard mode or a replay mode where it uses pre-recorded data to replay a previous simulation.

    Attributes:
        creator (PyASPGCreator): An instance of the PyASPGCreator class, responsible for setting up the grid components and their connections.
        data_log (DataLog): An instance of the DataLog class for recording simulation data into CSV files.
        simlog_path (str): The path to the simulation log file.
        replay_mode (bool): A flag indicating whether the simulation is running in replay mode, where it uses pre-recorded data.
        connection_handlers (dict): A dictionary mapping connection types to their corresponding handler classes, responsible for managing interactions
                                    between different grid components.

    Methods:
        run_simulation(duration, timestep, control_clock, output_dir, replay_mode=False):
            Runs the simulation for the specified duration and timestep, with an option to run in replay mode. Creates a unique subdirectory within
            the specified output directory to store the simulation results.

        _initialize_simlog(output_dir, components):
            Initializes the simulation log file, recording the start time and component counts.

        _finalize_simlog(output_dir, start_time, end_time, components):
            Finalizes the simulation log file, recording the end time and total duration.

        _get_control_system(components):
            Retrieves the control system component from the list of grid components.
    """
    def __init__(self, creator: PyASPGCreator):
        self.creator = creator
        self.data_log = None
        self.simlog_path = None
        self.replay_mode = False
        self.attacked = False
        self.connection_handlers = {
            'generator_to_transmitter': GeneratorToTransmitterHandler(),
            'transmitter_to_substation': TransmitterToSubstationHandler(),
            'substation_to_distributor': SubstationToDistributorHandler(),
            'distributor_to_prosumer': DistributorToProsumerHandler(),
            'prosumer_to_smart_meter': ProsumerToSmartMeterHandler(),
            'smart_meter_to_aggregator': SmartMeterToAggregatorHandler(),
            'aggregator_to_utility': AggregatorToUtilityHandler(),
            'utility_to_control': UtilityToControlHandler(),
            # Add other connection handlers here...
        }

    def run_simulation(self, duration, timestep, control_clock, output_dir, replay_mode, attacked=False):
        self.replay_mode = replay_mode  # Set the replay mode
        self.attacked = attacked

        # Create a unique subdirectory within output_dir
        timestamp = datetime.now().strftime("%d-%m-%Y")
        sim_dir_base = os.path.join(output_dir, f"{timestamp}-")
        sim_dir = sim_dir_base + "1"
        count = 1
        while os.path.exists(sim_dir):
            count += 1
            sim_dir = sim_dir_base + str(count)

        os.makedirs(sim_dir, exist_ok=True)

        self.data_log = DataLog(sim_dir)
        env = simpy.Environment()
        
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        components = self.creator.components
        connections = self.creator.connections


        self._initialize_simlog(sim_dir, components)
        start_time = datetime.now()

        # Create a CSV file for each component type
        self.data_log.initialize_files(components, connections)

        # Initialize the progress bar
        total_steps = duration // timestep

        pbar = tqdm(total=total_steps, desc="Replaying Simulation" if self.replay_mode else "Running Simulation", unit="timestep", colour="green", bar_format = "{desc}: {percentage:.1f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")

        def log_and_handle(t):
            for connection_type, connection_list in connections.items():
                handler = self.connection_handlers.get(connection_type)
                if handler:
                    # print(f"Handling {connection_type} connections at timestep {t}")
                    for source, target, params in connection_list:
                        handler.handle_connection(source, target, params, t // timestep, self.replay_mode, self.attacked)
            self.data_log.log_data(t, components, connections)

        def run_simulation_step(env):
            while True:
                log_and_handle(env.now)

                # Update prediction every update_interval timesteps
                control_system = self._get_control_system(components)
                if control_system:
                    if replay_mode:
                        control_system.replay_update_prediction(env.now, update_interval=control_clock, predictor='ideal', attacked=attacked)
                    else:
                        control_system.update_prediction(env.now, update_interval=control_clock)

                yield env.timeout(timestep)

                # Update the progress bar
                pbar.update(1)

        env.process(run_simulation_step(env))
        env.run(until=duration)

        # Manually ensure the progress bar reaches 100%
        if pbar.n < pbar.total:
            pbar.n = pbar.total
            pbar.refresh()

        end_time = datetime.now()

        # Close the progress bar
        pbar.close()

        # Close CSV files
        self.data_log.close_files()

        self._finalize_simlog(sim_dir, start_time, end_time, components)

    def _initialize_simlog(self, output_dir, components):
        self.simlog_path = os.path.join(output_dir, 'simlog.txt')
        with open(self.simlog_path, 'w') as log_file:
            log_file.write("Simulation Log\n")
            log_file.write("=============================\n")
            log_file.write(f"Simulation started at: {datetime.now()}\n")
            log_file.write("-----------------------------\n")
            log_file.write("Component Counts:\n")
            for component_type, component_list in components.items():
                log_file.write(f"{component_type.capitalize()}: {len(component_list)}\n")
            log_file.write("=============================\n")

    def _finalize_simlog(self, output_dir, start_time, end_time, components):
        duration = end_time - start_time
        with open(self.simlog_path, 'a') as log_file:
            log_file.write(f"Simulation ended at: {end_time}\n")
            log_file.write(f"Total duration: {duration}\n")
            log_file.write("=============================\n")

    def _get_control_system(self, components):
        control_systems = components.get('control_systems', [])
        return control_systems[0] if control_systems else None
