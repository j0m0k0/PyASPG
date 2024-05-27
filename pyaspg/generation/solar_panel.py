import numpy as np
from pyaspg.generation.generator import Generator

class SolarPanel(Generator):
    """
    Class representing a solar panel.
    """

    def generate(self, sunlight):
        """
        Generate electricity based on the amount of sunlight.

        Args:
            sunlight (float): The amount of sunlight, a factor between 0 and 1.
        """
        if sunlight < 0 or sunlight > 1:
            raise ValueError("Sunlight must be a value between 0 and 1")
        
        if sunlight:
            nominal_output = self.nominal_capacity * sunlight
            self.output = np.random.normal(nominal_output, self.std_dev * nominal_output)
            self.output = min(self.output, nominal_output)
        else:
            self.output = 0
        self.calculate_current()
        return self.output

    def __str__(self):
        """Return a string representation of the solar panel."""
        return (f"{self.name} (Nominal Capacity: {self.nominal_capacity} W, Voltage: {self.voltage} V, "
                f"Current: {self.current:.2f} A, Current Output: {self.output:.2f} W)")
