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


class PowerPlant(Generator):
    """
    Class representing a power plant.

    Attributes:
        fuel_capacity (float): The total fuel available in liters or kilograms.
        consumption_rate (float): The fuel consumption rate per hour of operation.
    """

    def __init__(self, env, name, nominal_capacity, voltage, fuel_capacity, consumption_rate, std_dev=0.1):
        """
        Initialize a PowerPlant instance.

        Args:
            env (simpy.Environment): The simulation environment.
            name (str): The name of the power plant.
            nominal_capacity (float): The nominal electricity generation capacity in watts (W).
            voltage (float): The voltage in volts (V).
            fuel_capacity (float): The total fuel available in liters or kilograms.
            consumption_rate (float): The fuel consumption rate per hour of operation.
            std_dev (float): The standard deviation for output variation.
        """
        super().__init__(env, name, nominal_capacity, voltage, std_dev)
        self.fuel_capacity = fuel_capacity
        self.consumption_rate = consumption_rate

    def generate(self):
        """Generate electricity while consuming fuel."""
        while True:
            if self.fuel_capacity > 0:
                self.output = np.random.normal(self.nominal_capacity, self.std_dev * self.nominal_capacity)
                self.output = min(self.output, self.nominal_capacity)
                self.fuel_capacity -= self.consumption_rate
                if self.fuel_capacity < 0:
                    self.fuel_capacity = 0
            else:
                self.output = 0
            self.calculate_current()
            print(f"{self.env.now}: {self}")
            yield self.env.timeout(1)


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
