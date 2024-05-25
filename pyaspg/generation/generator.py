import numpy as np
import simpy


class Generator:
    """
    Base class for all types of power generators.

    Attributes:
        env (simpy.Environment): The simulation environment.
        name (str): The name of the generator.
        nominal_capacity (float): The nominal electricity generation capacity in watts (W).
        voltage (float): The voltage in volts (V).
        current (float): The current in amperes (A).
        output (float): The current electricity output in watts (W).
        std_dev (float): The standard deviation for output variation.
    """

    def __init__(self, env, name, nominal_capacity, voltage, std_dev=0.1):
        """
        Initialize a Generator instance.

        Args:
            env (simpy.Environment): The simulation environment.
            name (str): The name of the generator.
            nominal_capacity (float): The nominal electricity generation capacity in watts (W).
            voltage (float): The voltage in volts (V).
            std_dev (float): The standard deviation for output variation.
        """
        self.env = env
        self.name = name
        self.nominal_capacity = nominal_capacity
        self.voltage = voltage
        self.current = 0
        self.output = 0
        self.std_dev = std_dev

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

    def __str__(self):
        """Return a string representation of the generator."""
        return (f"{self.name} (Nominal Capacity: {self.nominal_capacity} W, Voltage: {self.voltage} V, "
                f"Current: {self.current:.2f} A, Current Output: {self.output:.2f} W)")

# def main():
#     """Main function to run the simulation."""
#     env = simpy.Environment()

#     coal_plant = PowerPlant(env, name="Coal Plant", nominal_capacity=500000000, voltage=25000,
#                             fuel_capacity=10000, consumption_rate=50)
#     solar_panel = SolarPanel(env, name="Solar Panel", nominal_capacity=100000000, voltage=25000)
#     wind_turbine = WindTurbine(env, name="Wind Turbine", nominal_capacity=200000000, voltage=25000)

#     env.process(coal_plant.generate())
#     env.process(solar_panel.generate(sunlight=0.8))
#     env.process(wind_turbine.generate(wind_speed=0.5))

#     env.run(until=10)


# if __name__ == "__main__":
#     main()
