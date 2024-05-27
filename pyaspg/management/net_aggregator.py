from pyaspg.communication.smart_meter import SmartMeter, CommunicationNetwork
from pyaspg.prosume.household import Household
from pyaspg.management.utility_company import UtilityCompany

class NetAggregator:
    """
    Class representing a third-party data aggregator that collects and manages data from consumers and communicates with utility companies.

    Attributes:
        name (str): The name of the aggregator.
        data_collected (list): The list of data packets collected from smart meters.
        utility_data (dict): The aggregated data sent to utility companies.
        commands (dict): Commands to be sent to prosumers.
    """

    def __init__(self, name):
        """
        Initialize a NetAggregator instance.

        Args:
            name (str): The name of the aggregator.
        """
        self.name = name
        self.data_collected = []
        self.utility_data = {}
        self.commands = {}

    def collect_data(self, smart_meter):
        """
        Collect data from a smart meter.

        Args:
            smart_meter (SmartMeter): The smart meter to collect data from.

        Returns:
            bool: True if the data was collected successfully, False otherwise.
        """
        data = smart_meter.measure()
        if data:
            self.data_collected.append(data)
            return True
        return False

    def aggregate_data(self):
        """
        Aggregate the collected data for utility companies.
        """
        total_usage = sum(data['usage'] for data in self.data_collected)
        total_production = sum(data['production'] for data in self.data_collected)
        total_stored_energy = sum(data['stored_energy'] for data in self.data_collected)
        
        self.utility_data = {
            'total_usage': total_usage,
            'total_production': total_production,
            'total_stored_energy': total_stored_energy
        }

    def send_data_to_utility(self, utility_company):
        """
        Send aggregated data to a utility company.

        Args:
            utility_company (UtilityCompany): The utility company to send data to.
        """
        utility_company.receive_data(self.utility_data)

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
        print(f"NetAggregator {self.name} received command: {command} - {message}")

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

# Example usage
def main():
    # Creating instances for testing
    household = Household(name="Household 1", storage_capacity=5000)
    communication_network = CommunicationNetwork(name="Smart Grid Network", reliability=0.99)
    smart_meter = SmartMeter(prosumer=household, communication_network=communication_network)
    
    aggregator = NetAggregator(name="Data Aggregator 1")
    
    input_power = 10000  # 10 kW input power
    produced_power = 12000  # 12 kW produced power

    # Simulate consumption and production
    household.consume(input_power)
    household.produce(produced_power)

    # Collect data from smart meter
    aggregator.collect_data(smart_meter)
    
    # Aggregate data
    aggregator.aggregate_data()

    utility_company = UtilityCompany(name='CPS Energy')
    aggregator.send_data_to_utility(utility_company)

    # Sending command to prosumer
    command = "Reduce consumption by 500 W"
    aggregator.send_command(household, command)

    print(aggregator)
    print(f"Commands sent to {household.name}: {aggregator.commands[household.name]}")

if __name__ == "__main__":
    main()
