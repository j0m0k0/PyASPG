import numpy as np
import simpy
from .generator import Generator


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
        
        while True:
            if sunlight:
                nominal_output = self.nominal_capacity * sunlight
                self.output = np.random.normal(nominal_output, self.std_dev * nominal_output)
                self.output = min(self.output, nominal_output)
            else:
                self.output = 0
            self.calculate_current()
            print(f"{self.env.now}: {self}")
            yield self.env.timeout(1)
