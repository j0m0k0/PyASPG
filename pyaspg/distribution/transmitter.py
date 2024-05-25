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
        self.name = name
        self.input_power = 0
        self.efficiency = efficiency
        self.distance = distance
        self.output_power = 0

    def transmit(self, input_power):
        """
        Simulate the transmission of electricity.

        Args:
            input_power (float): The input power received from the generation sources in watts (W).

        Returns:
            float: The output power delivered to substations in watts (W).
        """
        self.input_power = input_power
        # Simulate power loss over distance
        loss_factor = (1 - self.efficiency) * self.distance / 100  # Loss increases with distance
        self.output_power = self.input_power * (1 - loss_factor)
        return self.output_power

    def __str__(self):
        """Return a string representation of the transmitter."""
        return (f"{self.name} (Input Power: {self.input_power} W, Output Power: {self.output_power} W, "
                f"Efficiency: {self.efficiency * 100}%, Distance: {self.distance} km)")

# Example usage
def main():
    transmitter = Transmitter(name="High Voltage Line 1", efficiency=0.97, distance=100)
    input_power = 1000000  # 1 MW input power
    output_power = transmitter.transmit(input_power)
    print(transmitter)
    print(f"Output Power: {output_power} W")

if __name__ == "__main__":
    main()
