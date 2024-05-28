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

class PyASPGCreator:
    """
    Class representing the creator for building a smart grid.

    Attributes:
        components (dict): A dictionary to store the components of the smart grid.
        connections (dict): A dictionary to store the connections between components.
    """

    def __init__(self):
        """
        Initialize a PyASPGCreator instance.
        """
        self.components = {
            "generators": [],
            "transmitters": [],
            "substations": [],
            "distributors": [],
            "prosumers": [],
            "communication_networks": [],
            "smart_meters": [],
            "aggregators": [],
            "utility_companies": [],
            "control_systems": []
        }
        self.connections = {
            "generator_to_transmitter": [],
            "transmitter_to_substation": [],
            "substation_to_distributor": [],
            "distributor_to_prosumer": [],
            "prosumer_to_smart_meter": [],
            "smart_meter_to_aggregator": [],
            "aggregator_to_utility": [],
            "utility_to_control": []
        }
        self.connection_rules = {
            "generator_to_transmitter": ("generators", "transmitters"),
            "transmitter_to_substation": ("transmitters", "substations"),
            "substation_to_distributor": ("substations", "distributors"),
            "distributor_to_prosumer": ("distributors", "prosumers"),
            "prosumer_to_smart_meter": ("prosumers", "smart_meters"),
            "smart_meter_to_aggregator": ("smart_meters", "aggregators"),
            "aggregator_to_utility": ("aggregators", "utility_companies"),
            "utility_to_control": ("utility_companies", "control_systems"),
        }

    def define_connections(self, **kwargs):
        """
        Define connections between components and store the components.

        Args:
            kwargs: Keyword arguments representing connections.
        """
        for connection_type, connection_list in kwargs.items():
            print("TEST", connection_type, connection_list)
            if connection_type in self.connections:
                source_type, target_type = self.connection_rules[connection_type]
                for connection in connection_list:
                    source, target = connection[:2]
                    params = connection[2] if len(connection) > 2 else {}

                    if not self.components[source_type] or not self.components[target_type]:
                        valid_source_type = type(source)
                        valid_target_type = type(target)
                    else:
                        valid_source_type = type(self.components[source_type][0])
                        valid_target_type = type(self.components[target_type][0])

                    if not isinstance(source, valid_source_type) or not isinstance(target, valid_target_type):
                        raise ValueError(f"Invalid connection: {source} -> {target} for {connection_type}")

                    if source not in self.components[source_type]:
                        self.components[source_type].append(source)
                    if target not in self.components[target_type]:
                        self.components[target_type].append(target)
                    
                    self.connections[connection_type].append((source, target, params))
            else:
                raise ValueError(f"Invalid connection type: {connection_type}")

    def create_smart_grid(self):
        """
        Create the smart grid based on the defined components and connections.
        """
        # Ensure smart meters measure data before printing their state
        for meter in self.components["smart_meters"]:
            meter.measure()

        print("Components:")
        for component_type, component_list in self.components.items():
            print(f"{component_type}: {[str(component) for component in component_list]}")

        print("\nConnections:")
        for connection_type, connection_list in self.connections.items():
            print(f"{connection_type}: {connection_list}")

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

if __name__ == "__main__":
    main()
