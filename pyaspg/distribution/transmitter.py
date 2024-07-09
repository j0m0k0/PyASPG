class Transmitter:
    """
    Class representing high-voltage power lines that transport electricity from generation sources to substations.

    Attributes:
        name (str): The name of the transmitter.
        input_power (float): The input power received from the generation sources in watts (W).
        efficiency (float): The efficiency of the transmission (a factor between 0 and 1).
        output_power (float): The output power delivered to substations in watts (W).
        distance (float): The distance over which the power is transmitted in kilometers (km).
        generators (list): The list of generators connected to this transmitter.
    """

    def __init__(self, name, efficiency=0.95, distance=50, generators=[]):
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
        self.latest_timestep = -1
        self.generators = set(generators)

    def receive(self, input_power, timestep):
        """
        Receive the power from the generator.

        Args:
            input_power (float): The input power received from the generation sources in watts (W).
            generator: The generator sending the power.
        
        Returns:
            None
        """
        if timestep != self.latest_timestep:
            self.reset_input_power()

        self.input_power += input_power
        self.latest_timestep = timestep

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
    
    def reset_input_power(self):
        """
        Reset the input power to zero at the start of each timestep.
        """
        self.input_power = 0

    def __str__(self):
        """Return a string representation of the transmitter."""
        return (f"{self.name} (Input Power: {self.input_power} W, Output Power: {self.output_power} W, "
                f"Efficiency: {self.efficiency * 100}%, Distance: {self.distance} km)")
