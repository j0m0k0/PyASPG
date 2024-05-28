import os
import csv
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

class GridSimulator:
    def __init__(self, creator: PyASPGCreator, output_dir: str):
        self.creator = creator
        self.data_log = DataLog(output_dir)

    def run_simulation(self, duration, timestep, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        components = self.creator.components
        connections = self.creator.connections

        # Create a CSV file for each component type
        self.data_log.initialize_files(components)

        for t in range(0, duration + 1, timestep):
            for generator in components['generators']:
                output_power = 0
                param_value = None
                if isinstance(generator, WindTurbine):
                    for gen, trans, params in connections['generator_to_transmitter']:
                        if gen == generator:
                            wind_speed = params.get('wind_speed', [0.8])[t // timestep]
                            param_value = wind_speed
                            output_power = generator.generate(wind_speed=wind_speed)
                            trans.transmit(output_power)
                elif isinstance(generator, SolarPanel):
                    for gen, trans, params in connections['generator_to_transmitter']:
                        if gen == generator:
                            sunlight = params.get('sunlight', [0.8])[t // timestep]
                            param_value = sunlight
                            output_power = generator.generate(sunlight=sunlight)
                            trans.transmit(output_power)
                elif isinstance(generator, PowerPlant):
                    for gen, trans, _ in connections['generator_to_transmitter']:
                        if gen == generator:
                            output_power = generator.generate()
                            trans.transmit(output_power)

                self.data_log.log_data(t, components, param_value)

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
            # (wind_turbine, transmitter, {'wind_speed': [0.8, 0.0, 0.7, 0.5]}),
            (solar_panel, transmitter, {'sunlight': [0.8, 0.0, 0.7, 0.6]})
        ],
        transmitter_to_substation=[(transmitter, substation)],
        substation_to_distributor=[(substation, distributor)],
        distributor_to_prosumer=[(distributor, household)],
        prosumer_to_smart_meter=[(household, smart_meter)],
        smart_meter_to_aggregator=[(smart_meter, aggregator)],
        aggregator_to_utility=[(aggregator, utility_company)],
        utility_to_control=[(utility_company, control_system)]
    )

    # Create the smart grid
    grid_creator.create_smart_grid()

    # Run the simulation
    simulator = GridSimulator(grid_creator, output_dir='simulation_results')
    simulator.run_simulation(duration=30, timestep=10, output_dir='simulation_results')

if __name__ == "__main__":
    main()
