import numpy as np
import simpy
from .generator import Generator


class WindTurbine(Generator):
    """
    Class representing a wind turbine.
    """

    def generate(self, wind_speed):
        """
        Generate electricity based on the wind speed.

        Args:
            wind_speed (float): The wind speed, a factor between 0 and 1.
        """
        if wind_speed < 0 or wind_speed > 1:
            raise ValueError("Wind speed must be a value between 0 and 1")
        
        while True:
            if wind_speed:
                nominal_output = self.nominal_capacity * wind_speed
                self.output = np.random.normal(nominal_output, self.std_dev * nominal_output)
                self.output = min(self.output, nominal_output)
            else:
                self.output = 0
            self.calculate_current()
            print(f"{self.env.now}: {self}")
            yield self.env.timeout(1)
