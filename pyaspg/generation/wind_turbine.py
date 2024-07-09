import numpy as np
from pyaspg.generation.generator import Generator

class WindTurbine(Generator):
    """
    Class representing a wind turbine.
    """

    def generate(self):
        """
        Generate electricity based on the wind speed.

        Args:
            wind_speed (float): The wind speed, a factor between 0 and 1.
        """
        print("Generate Function", self.name)
        self.input = self._get_demand()
        self.input = abs(self.nominal_capacity * self.input) if self.input < 0 else self.input
        # self.input = 2000
        nominal_output = self.nominal_capacity
        self.output = min(self.input, nominal_output)
        self.calculate_current()
        # print(f"{self.output=}")
        return self.output

    def __str__(self):
        """Return a string representation of the wind turbine."""
        return (f"{self.name} (Nominal Capacity: {self.nominal_capacity} W, Voltage: {self.voltage} V, "
                f"Current: {self.current:.2f} A, Current Output: {self.output:.2f} W)")
