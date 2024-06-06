from pyaspg.management.control_system import ControlSystem
from pyaspg.management.net_aggregator import NetAggregator
from pyaspg.management.utility_company import UtilityCompany
from pyaspg.communication.smart_meter import SmartMeter
from pyaspg.communication.communication_network import CommunicationNetwork
from pyaspg.prosume import Prosumer
from pyaspg.generation.power_plant import PowerPlant
from pyaspg.generation.solar_panel import SolarPanel
from pyaspg.generation.wind_turbine import WindTurbine
from pyaspg.distribution.transmitter import Transmitter
from pyaspg.distribution.distributor import Distributor
from pyaspg.distribution.substation import Substation
from pyaspg.utils import log_me


@log_me
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

