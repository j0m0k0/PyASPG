class Substation:
    """
    Class representing a substation that transforms high-voltage electricity from transmitters to lower voltage for distribution.

    Attributes:
        name (str): The name of the substation.
        input_power (float): The input power received from transmitters in watts (W).
        input_voltage (float): The input voltage in volts (V).
        output_voltage (float): The output voltage in volts (V).
        efficiency (float): The efficiency of the transformation (a factor between 0 and 1).
        output_power (float): The output power delivered for distribution in watts (W).
        output_current (float): The output current delivered for distribution in amperes (A).
    """

    def __init__(self, name, input_voltage, output_voltage, efficiency=0.98):
        """
        Initialize a Substation instance.

        Args:
            name (str): The name of the substation.
            input_voltage (float): The input voltage in volts (V).
            output_voltage (float): The output voltage in volts (V).
            efficiency (float): The efficiency of the transformation (a factor between 0 and 1).
        """
        if not (0 <= efficiency <= 1):
            raise ValueError("Efficiency must be between 0 and 1")
        if input_voltage <= output_voltage:
            raise ValueError("Input voltage must be higher than output voltage")

        self.name = name
        self.input_power = 0
        self.input_voltage = input_voltage
        self.output_voltage = output_voltage
        self.efficiency = efficiency
        self.output_power = 0
        self.output_current = 0
    
    def receive(self, input_power):
        """
        Receive the power from the generator.

        Args:
            input_power (float): The input power received from the generation sources in watts (W).
        
        Returns:
            None
        """

        self.input_power = input_power

    def transform(self):
        """
        Simulate the transformation of electricity.

        Args:

        Returns:
            float: The output power delivered for distribution in watts (W).
        """

        # Simulate power loss during transformation
        self.output_power = self.input_power * self.efficiency
        # Calculate the output current using the output voltage
        if self.output_voltage > 0:
            self.output_current = self.output_power / self.output_voltage
        else:
            self.output_current = 0
        return self.output_power

    def __str__(self):
        """Return a string representation of the substation."""
        return (f"{self.name} (Input Power: {self.input_power} W, Output Power: {self.output_power} W, "
                f"Input Voltage: {self.input_voltage} V, Output Voltage: {self.output_voltage} V, "
                f"Output Current: {self.output_current:.2f} A, Efficiency: {self.efficiency * 100}%)")