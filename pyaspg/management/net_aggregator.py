from pyaspg.communication.smart_meter import SmartMeter, CommunicationNetwork
from pyaspg.prosume import Prosumer
from pyaspg.management.utility_company import UtilityCompany
from pyaspg.utils import log_me
from pyaspg.attacks import inflate, deflate, hybrid


@log_me
class NetAggregator:
    """
    Class representing a third-party data aggregator that collects and manages data from consumers and communicates with utility companies.

    Attributes:
        name (str): The name of the aggregator.
        data_collected (list): The list of data packets collected from smart meters.
        utility_data (dict): The aggregated data sent to utility companies.
        commands (dict): Commands to be sent to prosumers.
    """

    def __init__(self, name, compromised=False, attack_method=None, attack_metadata=None, compromise_start_time=None, compromise_duration=None, control_system=None):
        """
        Initialize a NetAggregator instance.

        Args:
            name (str): The name of the aggregator.
        """
        self.name = name
        self.data_collected = {}
        self.utility_data = {}
        self.commands = {}
        self.latest_timestep = -1
        self.smart_meters = []
        self.compromised = compromised
        self.attack_method = attack_method
        self.attack_metadata = attack_metadata        
        self.compromise_start_time = compromise_start_time
        self.compromise_duration = compromise_duration
        self.end_time = None
        self.control_system = control_system
        if self.compromise_start_time is not None and self.compromise_duration is not None:
            self.end_time = compromise_start_time + compromise_duration        

    def report_bias_to_control_system(self, control_system, timestep):
        if self.compromised and self.attack_method is not None:
            # This amount should be based on attack_type and the rates
            amount = None
            if self.attack_method is inflate.inflation_attack:
                amount = (self.data_collected[timestep][-1]["net_power"] / 1.1) * 0.1
            elif self.attack_method is deflate.deflation_attack:
                amount = (self.data_collected[timestep][-1]["net_power"] / 0.9) * -0.1
            else:
                INFLATION_DISTRIBURATION = self.attack_metadata['distribution_data'].get(self.data_collected[timestep][-1]["prosumer"]) == 'D1'  
                # TODO the multipliers should be calculated per each distribution and passed as meta data probably.
                              
                if INFLATION_DISTRIBURATION:
                    amount = (self.data_collected[timestep][-1]["net_power"] / self.attack_metadata['multipliers_data'][timestep]['Multiplier_A']) * (self.attack_metadata['multipliers_data'][timestep]['Multiplier_A'] - 1)
                else:
                    amount = (self.data_collected[timestep][-1]["net_power"] / self.attack_metadata['multipliers_data'][timestep]['Multiplier_B']) * (self.attack_metadata['multipliers_data'][timestep]['Multiplier_B'] - 1)
            control_system.receive_message("bias", timestep, dict(name=self.name, data=amount))

    def add_smart_meter(self, smart_meter):
        """
        Collection of smart meters connected to this net aggregator
        """
        self.smart_meters.append(smart_meter)

    def collect_data(self, smart_meter, timestep):
        """
        Collect data from a smart meter.

        Args:
            smart_meter (SmartMeter): The smart meter to collect data from.

        Returns:
            bool: True if the data was collected successfully, False otherwise.
        """
        data = smart_meter.measure()
        if timestep != self.latest_timestep:
            self.data_collected[timestep] = []
            self.latest_timestep = timestep


        data["timestep"] = timestep
        data["aggregator_name"] = self.name
        # Check if the aggregator is compromised and an attack method exists
        if self.compromised and self.attack_method is not None:
            # whole simulation time attack
            if (self.compromise_start_time is None) and (self.compromise_duration is None):            
                data["net_power"] = self.attack_method(data["net_power"], criteria=timestep % 2 == 0)
            # partial simulation time attack
            else:
                if timestep >= self.compromise_start_time and timestep <= self.end_time:
                    # attack only for a specific duration
                    data["net_power"] = self.attack_method(data["net_power"], criteria=timestep % 2 == 0)
        
        # Collect the data
        self.data_collected[timestep].append(data)
        
        conditions_to_report_bias_to_cs = self.compromised and (self.attack_method is not None)
        if conditions_to_report_bias_to_cs:
            # print("We should report")
            if self.end_time is not None:
                # timed attack
                if timestep >= self.compromise_start_time and timestep <= self.end_time:
                    self.report_bias_to_control_system(self.control_system, timestep)
            else:
                # continuous attack
                self.report_bias_to_control_system(self.control_system, timestep)
            

    def aggregate_data(self, timestep):
        """
        Aggregate the collected data for utility companies for the specified timestep.

        Args:
            timestep (int): The current timestep for which to aggregate data.
        """
        # Ensure the current timestep has data collected
        collected_data = self.data_collected[timestep]


        # Check if the number of collected data matches the number of smart meters

        total_usage = sum(data['total_consumption'] for data in collected_data)
        total_production = sum(data['total_production'] for data in collected_data)
        total_stored_energy = sum(data['stored_energy'] for data in collected_data)
        total_net_power = sum(data['net_power'] for data in collected_data)

        self.utility_data = {
            'total_consumption': total_usage,
            'total_production': total_production,
            'total_stored_energy': total_stored_energy,
            'aggregator_name': self.name,
            'total_net_power': total_net_power,
        }

    def send_data_to_utility(self, utility_company, timestep):
        """
        Send aggregated data to a utility company.

        Args:
            utility_company (UtilityCompany): The utility company to send data to.
        """        
        utility_company.receive_data(self.utility_data, timestep)

    def receive_command(self, command, message):
        """
        Receive a command from the control system.

        Args:
            command (str): The command to be received.
            message (str): The message or details of the command.
        """
        if command not in self.commands:
            self.commands[command] = []
        self.commands[command].append(message)

    def send_command(self, prosumer, command):
        """
        Send a command to a prosumer.

        Args:
            prosumer (Prosumer): The prosumer to send the command to.
            command (str): The command to be sent.
        """
        if prosumer.name not in self.commands:
            self.commands[prosumer.name] = []
        self.commands[prosumer.name].append(command)
        prosumer.receive_command(command)

    def __str__(self):
        """Return a string representation of the aggregator."""
        return (f"NetAggregator {self.name} (Data Collected: {len(self.data_collected)} packets, "
                f"Utility Data: {self.utility_data}, Commands: {self.commands})")
