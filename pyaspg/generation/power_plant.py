import numpy as np
from pyaspg.generation.generator import Generator

class PowerPlant(Generator):
    """
    Class representing a power plant.

    Attributes:
        fuel_capacity (float): The total fuel available in liters or kilograms.
        consumption_rate (float): The fuel consumption rate per hour of operation.
    """

    def __init__(self, name, nominal_capacity, voltage, fuel_capacity, consumption_rate, std_dev=0.1):
        """
        Initialize a PowerPlant instance.

        Args:
            name (str): The name of the power plant.
            nominal_capacity (float): The nominal electricity generation capacity in watts (W).
            voltage (float): The voltage in volts (V).
            fuel_capacity (float): The total fuel available in liters or kilograms.
            consumption_rate (float): The fuel consumption rate per hour of operation.
            std_dev (float): The standard deviation for output variation.
        """
        super().__init__(name, nominal_capacity, voltage, std_dev)
        self.fuel_capacity = fuel_capacity
        self.consumption_rate = consumption_rate

    def generate(self):
        """Generate electricity while consuming fuel."""
        if self.fuel_capacity > 0:
            self.output = np.random.normal(self.nominal_capacity, self.std_dev * self.nominal_capacity)
            self.output = min(self.output, self.nominal_capacity)
            self.fuel_capacity -= self.consumption_rate
            if self.fuel_capacity < 0:
                self.fuel_capacity = 0
        else:
            self.output = 0
        self.calculate_current()
        return self.output

    def __str__(self):
        """Return a string representation of the power plant."""
        return (f"{self.name} (Nominal Capacity: {self.nominal_capacity} W, Voltage: {self.voltage} V, "
                f"Current: {self.current:.2f} A, Current Output: {self.output:.2f} W, "
                f"Fuel Capacity: {self.fuel_capacity} L or kg)")
