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

    def transform(self, input_power):
        """
        Simulate the transformation of electricity.

        Args:
            input_power (float): The input power received from transmitters in watts (W).

        Returns:
            float: The output power delivered for distribution in watts (W).
        """
        self.input_power = input_power
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

# Example usage
def main():
    substation = Substation(name="Main Substation", input_voltage=25000, output_voltage=10000, efficiency=0.98)
    input_power = 1000000  # 1 MW input power
    output_power = substation.transform(input_power)
    print(substation)
    print(f"Output Power: {output_power} W")

if __name__ == "__main__":
    main()
