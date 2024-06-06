from pyaspg.prosume import Prosumer
from pyaspg.communication.communication_network import CommunicationNetwork

class SmartMeter:
    """
    Class representing a smart meter that measures electricity usage and communicates with utility companies and third-party data aggregators.

    Attributes:
        prosumer (Prosumer): The prosumer associated with this smart meter.
        communication_network (CommunicationNetwork): The communication network used for transmitting data.
        data (dict): The measured data including usage, production, net power, and stored energy in watts (W).
    """

    def __init__(self, prosumer, communication_network):
        """
        Initialize a SmartMeter instance.

        Args:
            prosumer (Prosumer): The prosumer associated with this smart meter.
            communication_network (CommunicationNetwork): The communication network used for transmitting data.
        """
        self.prosumer = prosumer
        self.communication_network = communication_network
        self.data = {}

    def measure(self):
        """
        Measure the electricity usage, production, and net power of the prosumer.

        Returns:
            dict: The measured data including usage, production, and net power in watts (W).
        """
        self.data = {
            "usage": self.prosumer.total_consumption,
            "production": self.prosumer.total_production,
            "net_power": self.prosumer.net_power,
            "stored_energy": self.prosumer.stored_energy
        }
        return self.data

    def send_data(self):
        """
        Simulate sending real-time usage and production data to utility companies and third-party aggregators.

        Returns:
            bool: True if the data was transmitted successfully, False otherwise.
        """
        data_packet = self.measure()
        data_packet["prosumer_name"] = self.prosumer.name
        success = self.communication_network.transmit_data(data_packet)
        return success

    def __str__(self):
        """Return a string representation of the smart meter."""
        data = self.data
        return (f"SmartMeter for {self.prosumer.name} (Usage: {data['usage']} W, "
                f"Production: {data['production']} W, Net Power: {data['net_power']} W, "
                f"Stored Energy: {data['stored_energy']} W)")