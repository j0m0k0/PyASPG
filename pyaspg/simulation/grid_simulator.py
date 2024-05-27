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

class GridSimulator:
    def __init__(self, creator: PyASPGCreator):
        self.creator = creator

    def run_simulation(self, duration, timestep, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        components = self.creator.components
        connections = self.creator.connections

        # Create a CSV file for each component type
        files = {}
        writers = {}
        for component_type, component_list in components.items():
            if component_list:
                file_path = os.path.join(output_dir, f"{component_type}.csv")
                files[component_type] = open(file_path, 'w', newline='')
                writers[component_type] = csv.writer(files[component_type])
                header = ['timestep'] + [attr for attr in vars(component_list[0]).keys() if attr != 'env']
                writers[component_type].writerow(header)

        def log_data(timestep):
            for component_type, component_list in components.items():
                if component_list:
                    writer = writers[component_type]
                    for component in component_list:
                        data = [timestep] + [getattr(component, attr) for attr in vars(component) if attr != 'env']
                        writer.writerow(data)

        for t in range(0, duration + 1, timestep):
            for generator in components['generators']:
                if isinstance(generator, WindTurbine):
                    output_power = generator.generate(wind_speed=0.8)  # Example wind speed
                elif isinstance(generator, SolarPanel):
                    output_power = generator.generate(sunlight=0.8)  # Example sunlight intensity
                elif isinstance(generator, PowerPlant):
                    output_power = generator.generate()  # Power plant with default generation logic

                # Pass output to the connected transmitter
                for gen, trans in connections['generator_to_transmitter']:
                    if gen == generator:
                        trans.transmit(output_power)

            log_data(t)

        for f in files.values():
            f.close()

# Example usage
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

    transmitter = Transmitter(name="High Voltage Line 1", efficiency=0.97, distance=100)
    distributor = Distributor(name="Low Voltage Line 1", efficiency=0.9, distance=10)
    substation = Substation(name="Main Substation", input_voltage=25000, output_voltage=10000, efficiency=0.98)

    # Define connections between components
    grid_creator.define_connections(
        generator_to_transmitter=[(wind_turbine, transmitter)],
        # transmitter_to_substation=[(transmitter, substation)],
        # substation_to_distributor=[(substation, distributor)],
        # distributor_to_prosumer=[(distributor, household)],
        # prosumer_to_smart_meter=[(household, smart_meter)],
        # smart_meter_to_aggregator=[(smart_meter, aggregator)],
        # aggregator_to_utility=[(aggregator, utility_company)],
        # utility_to_control=[(utility_company, control_system)]
    )

    # Create the smart grid
    grid_creator.create_smart_grid()

    # Run the simulation
    simulator = GridSimulator(grid_creator)
    simulator.run_simulation(duration=100, timestep=10, output_dir='simulation_results')

if __name__ == "__main__":
    main()
