class Distributor:
    """
    Class representing lower-voltage power lines that deliver electricity to consumers.

    Attributes:
        name (str): The name of the distributor.
        input_power (float): The input power received from substations in watts (W).
        efficiency (float): The efficiency of the distribution (a factor between 0 and 1).
        output_power (float): The output power delivered to end-users in watts (W).
        distance (float): The distance over which the power is distributed in kilometers (km).
        available_power (float): The available power that can be distributed to end-users in watts (W).
    """

    def __init__(self, name, efficiency=0.9, distance=10):
        """
        Initialize a Distributor instance.

        Args:
            name (str): The name of the distributor.
            efficiency (float): The efficiency of the distribution (a factor between 0 and 1).
            distance (float): The distance over which the power is distributed in kilometers (km).
        """
        if not (0 <= efficiency <= 1):
            raise ValueError("Efficiency must be between 0 and 1")

        self.name = name
        self.input_power = 0
        self.efficiency = efficiency
        self.distance = distance
        self.output_power = 0
        self.available_power = 0

    def receive(self, input_power):
        """
        Receive the power from the generator.

        Args:
            input_power (float): The input power received from the generation sources in watts (W).
        """
        self.input_power = input_power
        self.available_power = self.distribute()  # Update available power

    def distribute(self):
        """
        Simulate the distribution of electricity.

        Returns:
            float: The output power delivered to end-users in watts (W).
        """
        # Simulate power loss over distance
        loss_factor = min((1 - self.efficiency) * self.distance / 10, 1)  # Cap loss factor at 1
        self.output_power = max(self.input_power * (1 - loss_factor), 0)  # Ensure non-negative output power
        return self.output_power

    def __str__(self):
        """Return a string representation of the distributor."""
        return (f"{self.name} (Input Power: {self.input_power} W, Output Power: {self.output_power} W, "
                f"Efficiency: {self.efficiency * 100}%, Distance: {self.distance} km)")
