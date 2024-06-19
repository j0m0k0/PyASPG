from pyaspg.utils import log_me

@log_me
class UtilityCompany:
    """
    Class representing a utility company that manages the generation, transmission, and distribution of electricity.

    Attributes:
        name (str): The name of the utility company.
        received_data (list): The list of aggregated data packets received from net aggregators.
    """

    def __init__(self, name):
        """
        Initialize a UtilityCompany instance.

        Args:
            name (str): The name of the utility company.
        """
        self.name = name
        self.received_data = []


    def receive_data(self, data):
        """
        Receive aggregated data from a net aggregator.

        Args:
            data (dict): The aggregated data to be received.
        """
        self.received_data = [data]

    def __str__(self):
        """Return a string representation of the utility company."""
        return (f"UtilityCompany {self.name} (Received Data Packets: {len(self.received_data)})")
