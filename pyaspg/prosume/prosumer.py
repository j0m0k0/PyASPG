class Prosumer:
    """
    Class representing a prosumer who can both consume and produce electricity.

    Attributes:
        name (str): The name of the prosumer.
        consumption (float): The electricity consumption in watts (W).
        production (float): The electricity production in watts (W).
        storage_capacity (float): The storage capacity in watts (W).
        stored_energy (float): The current stored energy in watts (W).
    """

    def __init__(self, name, storage_capacity=0):
        """
        Initialize a Prosumer instance.

        Args:
            name (str): The name of the prosumer.
            storage_capacity (float): The storage capacity in watts (W). Default is 0.
        """
        self.name = name
        self.consumption = 0
        self.production = 0
        self.storage_capacity = storage_capacity
        self.stored_energy = 0

    def consume(self, power):
        """
        Simulate the consumption of electricity.

        Args:
            power (float): The power to be consumed in watts (W).
        """
        self.consumption += power

    def produce(self, power):
        """
        Simulate the production of electricity.

        Args:
            power (float): The power to be produced in watts (W).
        """
        self.production += power

    def store_energy(self, power):
        """
        Store produced energy if there is available storage capacity.

        Args:
            power (float): The power to be stored in watts (W).

        Returns:
            float: The amount of power stored.
        """
        available_capacity = self.storage_capacity - self.stored_energy
        power_to_store = min(power, available_capacity)
        self.stored_energy += power_to_store
        return power_to_store

    def use_stored_energy(self, power):
        """
        Use stored energy to meet consumption needs.

        Args:
            power (float): The power to be used in watts (W).

        Returns:
            float: The amount of power used from storage.
        """
        power_to_use = min(power, self.stored_energy)
        self.stored_energy -= power_to_use
        return power_to_use

    def net_power(self):
        """
        Calculate the net power that needs to be drawn from or sent to the grid.

        Returns:
            float: The net power in watts (W). Positive if power is needed from the grid, negative if power is sent to the grid.
        """
        net = self.consumption - self.production
        if net > 0:
            net -= self.use_stored_energy(net)
        elif net < 0:
            excess_production = -net
            stored = self.store_energy(excess_production)
            net = -(excess_production - stored)
        return net

    def __str__(self):
        """Return a string representation of the prosumer."""
        return (f"{self.name} (Consumption: {self.consumption} W, Production: {self.production} W, "
                f"Stored Energy: {self.stored_energy} W, Storage Capacity: {self.storage_capacity} W)")

# Example usage
def main():
    household = Prosumer(name="Household 1", storage_capacity=5000)
    household.consume(10000)  # 10 kW consumption
    household.produce(12000)  # 12 kW production

    net_power = household.net_power()
    print(household)
    print(f"Net Power: {net_power} W (positive means drawing from the grid, negative means sending to the grid)")

if __name__ == "__main__":
    main()
