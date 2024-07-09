import numpy as np

class Generator:
    """
    Base class for all types of power generators.

    Attributes:
        name (str): The name of the generator.
        nominal_capacity (float): The nominal electricity generation capacity in watts (W).
        voltage (float): The voltage in volts (V).
        current (float): The current in amperes (A).
        output (float): The current electricity output in watts (W).
        std_dev (float): The standard deviation for output variation.
    """

    def __init__(self, name, nominal_capacity, voltage, controller=None, std_dev=0.1):
        """
        Initialize a Generator instance.

        Args:
            name (str): The name of the generator.
            nominal_capacity (float): The nominal electricity generation capacity in watts (W).
            voltage (float): The voltage in volts (V).
            std_dev (float): The standard deviation for output variation.
            controller (SystemController): The controller of generator.
        """
        self.name = name
        self.nominal_capacity = nominal_capacity
        self.voltage = voltage
        self.current = 0
        self.input = 0
        self.output = 0
        self.std_dev = std_dev
        self.controller = controller


    def generate(self, input_resource):
        """
        Abstract method to be overridden by subclasses to generate electricity.

        Args:
            input_resource: The input resource required for electricity generation.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def calculate_current(self):
        """Calculate the current based on the output power and voltage."""
        if self.voltage > 0:
            self.current = self.output / self.voltage
        else:
            self.current = 0

    def _get_demand(self):
        """Return the demanded power by the system controller"""
        print("_get_demand called in the generator object")
        return self.controller.get_demand(self.name)

    def __str__(self):
        """Return a string representation of the generator."""
        return (f"{self.name} (Nominal Capacity: {self.nominal_capacity} W, Voltage: {self.voltage} V, "
                f"Current: {self.current:.2f} A, Current Output: {self.output:.2f} W)")
