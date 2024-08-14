from pyaspg.utils import log_me

@log_me
class UtilityCompany:
    """
    Class representing a utility company that manages the generation, transmission, and distribution of electricity.

    Attributes:
        name (str): The name of the utility company.
        received_data (list): The list of aggregated data packets received from net aggregators.
        generators (list): The list of generators associated with this utility company.
    """

    def __init__(self, name, generators):
        """
        Initialize a UtilityCompany instance.

        Args:
            name (str): The name of the utility company.
            generators (list): The list of generators associated with this utility company.
        """
        self.name = name
        self.received_data = []
        self.generators = generators
        self.last_time_step = -1

    def receive_data(self, data, timestep):
        """
        Receive aggregated data from a net aggregator.

        Args:
            data (dict): The aggregated data to be received.
        """
        if self.last_time_step != timestep:
            self.received_data = []
            
        self.last_time_step = timestep
               

        if data not in self.received_data:      
            self.received_data.append(data)

    def __str__(self):
        """Return a string representation of the utility company."""
        return (f"UtilityCompany {self.name} (Received Data Packets: {len(self.received_data)})")
