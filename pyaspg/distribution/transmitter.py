class Transmitter:
    """
    Class representing high-voltage power lines that transport electricity from generation sources to substations.

    Attributes:
        name (str): The name of the transmitter.
        input_power (float): The input power received from the generation sources in watts (W).
        efficiency (float): The efficiency of the transmission (a factor between 0 and 1).
        output_power (float): The output power delivered to substations in watts (W).
        distance (float): The distance over which the power is transmitted in kilometers (km).
    """

    def __init__(self, name, efficiency=0.95, distance=50):
        """
        Initialize a Transmitter instance.

        Args:
            name (str): The name of the transmitter.
            efficiency (float): The efficiency of the transmission (a factor between 0 and 1).
            distance (float): The distance over which the power is transmitted in kilometers (km).
        """
        if not (0 <= efficiency <= 1):
            raise ValueError("Efficiency must be between 0 and 1")

        self.name = name
        self.input_power = 0
        self.efficiency = efficiency
        self.distance = distance
        self.output_power = 0

    def receive(self, input_power):
        """
        Receive the power from the generator.

        Args:
            input_power (float): The input power received from the generation sources in watts (W).
        
        Returns:
            None
        """

        self.input_power = input_power

    def transmit(self):
        """
        Simulate the transmission of electricity.

        Returns:
            float: The output power delivered to substations in watts (W).
        """
        # Simulate power loss over distance
        loss_factor = min((1 - self.efficiency) * self.distance / 100, 1)  # Cap loss factor at 1
        self.output_power = max(self.input_power * (1 - loss_factor), 0)  # Ensure non-negative output power
        return self.output_power

    def __str__(self):
        """Return a string representation of the transmitter."""
        return (f"{self.name} (Input Power: {self.input_power} W, Output Power: {self.output_power} W, "
                f"Efficiency: {self.efficiency * 100}%, Distance: {self.distance} km)")
