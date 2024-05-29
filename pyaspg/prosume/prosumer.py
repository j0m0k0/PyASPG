from pyaspg.utils import log_me


@log_me
class Prosumer:
    """
    Class representing a prosumer who can both consume and produce electricity.

    Attributes:
        name (str): The name of the prosumer.
        total_consumption (float): The total electricity consumption in watts (W).
        total_production (float): The total electricity production in watts (W).
        storage_capacity (float): The storage capacity in watts (W).
        stored_energy (float): The current stored energy in watts (W).
        received_commands (list): List of received commands from the aggregator.
    """

    def __init__(self, name, storage_capacity=0):
        """
        Initialize a Prosumer instance.

        Args:
            name (str): The name of the prosumer.
            storage_capacity (float): The storage capacity in watts (W). Default is 0.
        """
        self.name = name
        self.total_consumption = 0
        self.total_production = 0
        self.storage_capacity = storage_capacity
        self.stored_energy = 0
        self.received_commands = []
        self._net_power = 0

    def _update_net_power(self, amount, is_consumption=False, is_production=False):
        """
        Calculate and update the net power based on the current state.

        Args:
            amount (float): The amount of power to be consumed or produced.
            is_consumption (bool): Indicates if the action is consumption.
            is_production (bool): Indicates if the action is production.
        """
        if is_consumption:
            # First use stored energy
            used_from_storage = min(amount, self.stored_energy)
            self.stored_energy -= used_from_storage
            remaining_consumption = amount - used_from_storage
            self._net_power += remaining_consumption
        elif is_production:
            # First try to meet the net power need
            # if self._net_power == 0:
            #     # Just add to the storage
            #     self.stored_energy = min(self.stored_energy + amount, self.storage_capacity)
            # else:
            net_before_production = self._net_power
            self._net_power -= min(amount, self._net_power)
            remaining_amount = amount - (net_before_production - self._net_power)
            stored_energy = min(remaining_amount, self.storage_capacity - self.stored_energy)
            self.stored_energy += stored_energy
            self._net_power -= (remaining_amount - stored_energy)

    @property
    def net_power(self):
        """
        Get the current net power.

        Returns:
            float: The net power in watts (W). Positive if power is needed from the grid, negative if power is sent to the grid.
        """
        return self._net_power

    def consume(self, power):
        """
        Simulate the consumption of electricity.

        Args:
            power (float): The power to be consumed in watts (W).
        """
        self.total_consumption += power
        self._update_net_power(power, is_consumption=True)

    def produce(self, power):
        """
        Simulate the production of electricity.

        Args:
            power (float): The power to be produced in watts (W).
        """
        self.total_production += power
        self._update_net_power(power, is_production=True)

    def receive_command(self, command):
        """
        Receive a command from the aggregator and store it.

        Args:
            command (str): The command to be received.
        """
        self.received_commands.append(command)

    def __str__(self):
        """Return a string representation of the prosumer."""
        return (f"{self.name} (Consumption: {self.total_consumption} W, Production: {self.total_production} W, "
                f"Stored Energy: {self.stored_energy} W, Storage Capacity: {self.storage_capacity} W, "
                f"Net Power: {self._net_power} W, Received Commands: {self.received_commands})")

