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

    def add_components(self, **kwargs):
        """
        Add components to the creator.

        Args:
            kwargs: Keyword arguments representing component lists.
        """
        for component_type, component_list in kwargs.items():
            if component_type in self.components:
                self.components[component_type].extend(component_list)
            else:
                raise ValueError(f"Invalid component type: {component_type}")

    def define_connections(self, **kwargs):
        """
        Define connections between components.

        Args:
            kwargs: Keyword arguments representing connections.
        """
        for connection_type, connection_list in kwargs.items():
            if connection_type in self.connections:
                self.connections[connection_type].extend(connection_list)
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

    coal_plant = PowerPlant(None, name="Coal Plant", nominal_capacity=500000000, voltage=25000, fuel_capacity=10000, consumption_rate=50)
    solar_panel = SolarPanel(None, name="Solar Panel 1", nominal_capacity=100000000, voltage=25000)
    wind_turbine = WindTurbine(None, name="Wind Turbine 1", nominal_capacity=200000000, voltage=25000)

    transmitter = Transmitter(name="High Voltage Line 1", efficiency=0.97, distance=100)
    distributor = Distributor(name="Low Voltage Line 1", efficiency=0.9, distance=10)
    substation = Substation(name="Main Substation", input_voltage=25000, output_voltage=10000, efficiency=0.98)

    # Add components to the grid
    grid_creator.add_components(
        generators=[coal_plant, solar_panel, wind_turbine],
        transmitters=[transmitter],
        substations=[substation],
        distributors=[distributor],
        prosumers=[household],
        communication_networks=[communication_network],
        smart_meters=[smart_meter],
        aggregators=[aggregator],
        utility_companies=[utility_company],
        control_systems=[control_system]
    )

    # Define connections between components
    grid_creator.define_connections(
        generator_to_transmitter=[(coal_plant, transmitter), (solar_panel, transmitter), (wind_turbine, transmitter)],
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
