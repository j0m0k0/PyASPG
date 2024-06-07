import numpy as np
from pyaspg.utils import log_me, ConsumptionPatternParser

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
        consumption_pattern_parser (ConsumptionPatternParser): A parser for consumption pattern.
        production_pattern (tuple): A tuple representing the mean and standard deviation of the production pattern.
    """

    def __init__(self, name, prosumer_type="House", storage_capacity=0, consumption_file=None, bias=0, production_pattern=(500, 100)):
        """
        Initialize a Prosumer instance.

        Args:
            name (str): The name of the prosumer.
            storage_capacity (float): The storage capacity in watts (W). Default is 0.
            consumption_file (str): The path to the consumption pattern file.
            bias (float): The bias to be added to each total meter reading.
            production_pattern (tuple): A tuple representing the mean and standard deviation of the production pattern.
        """
        self.name = name
        self.total_consumption = 0
        self.total_production = 0
        self.storage_capacity = storage_capacity
        self.stored_energy = 0
        self.received_commands = []
        self._net_power = 0
        self.consumption_pattern_parser = ConsumptionPatternParser(consumption_file, bias) if consumption_file else None
        self.production_pattern = production_pattern
        self.received_power = 0  # Track received power
        self.prosumer_type = prosumer_type
        self.net_power_before = 0
        self.stored_energy_before = 0

    def _update_net_power(self, amount, is_consumption=False, is_production=False):
        if is_consumption:
            # First use stored energy
            used_from_storage = min(amount, self.stored_energy)
            self.stored_energy -= used_from_storage
            remaining_consumption = amount - used_from_storage
            self._net_power += remaining_consumption
        elif is_production:
            # First try to meet the net power need
            net_before_production = self._net_power
            self._net_power -= min(amount, self._net_power)
            remaining_amount = amount - (net_before_production - self._net_power)
            stored_energy = min(remaining_amount, self.storage_capacity - self.stored_energy)
            self.stored_energy += stored_energy
            self._net_power -= (remaining_amount - stored_energy)

    def receive(self, power, distributor_name):
        """
        Receive power from the distribution line.

        Args:
            power (float): The amount of power received in watts (W).
            distributor_name (str): The name of the distributor providing the power.
        """
        # Track values before receiving power
        self.net_power_before = self._net_power
        self.stored_energy_before = self.stored_energy

        needed_power = self._net_power
        received_power = min(needed_power, power)
        self._net_power -= received_power
        self.stored_energy = min(self.stored_energy + (power - received_power), self.storage_capacity)

        # Track received power and distributor name
        self.received_power = received_power
        self.distributor_name = distributor_name
        
    @property
    def net_power(self):
        """
        Get the current net power.

        Returns:
            float: The net power in watts (W). Positive if power is needed from the grid, negative if power is sent to the grid.
        """
        return self._net_power

    def generate_consumption(self):
        """
        Generate a power consumption based on the consumption pattern from the file.

        Returns:
            float: The generated power consumption in watts (W).
        """
        if self.consumption_pattern_parser:
            consumption = next(self.consumption_pattern_parser)
            self.consume(consumption)
            return consumption
        else:
            return 0

    def generate_production(self):
        """
        Generate a random power production based on the production pattern.

        Returns:
            float: The generated power production in watts (W).
        """
        production = max(0, np.random.normal(*self.production_pattern))
        self.produce(production)
        return production

    def consume(self, power):
        """
        Simulate the consumption of electricity.

        Args:
            power (float): The power to be consumed in watts (W).
        """
        self.total_consumption += power
        # First use stored energy
        used_from_storage = min(power, self.stored_energy)
        self.stored_energy -= used_from_storage
        remaining_consumption = power - used_from_storage
        if remaining_consumption > 0:
            self._net_power += remaining_consumption

    def produce(self, power):
        """
        Simulate the production of electricity.

        Args:
            power (float): The power to be produced in watts (W).
        """
        self.total_production += power
        # First try to reduce net power to zero
        if self._net_power > 0:
            reduction = min(self._net_power, power)
            self._net_power -= reduction
            power -= reduction
        # Store any remaining power if possible
        if power > 0:
            storage_space = self.storage_capacity - self.stored_energy
            stored = min(storage_space, power)
            self.stored_energy += stored
            power -= stored
        # If there is still remaining power, update net power
        if power > 0:
            self._net_power -= power

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
                f"Stored Energy: {self.stored_energy} W, Storage Capacity: {self.storage_capacity})")
