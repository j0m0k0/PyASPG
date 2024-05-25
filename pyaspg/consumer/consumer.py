class Consumer:
    """
    Base class representing end-users of electricity.

    Attributes:
        name (str): The name of the consumer.
        input_power (float): The input power received from the distribution network in watts (W).
        consumption_rate (float): The rate of electricity consumption in watts (W).
        consumed_power (float): The total electricity consumed in watts (W).
    """

    def __init__(self, name, consumption_rate):
        """
        Initialize a Consumer instance.

        Args:
            name (str): The name of the consumer.
            consumption_rate (float): The rate of electricity consumption in watts (W).
        """
        self.name = name
        self.input_power = 0
        self.consumption_rate = consumption_rate
        self.consumed_power = 0

    def consume(self, input_power):
        """
        Simulate the consumption of electricity.

        Args:
            input_power (float): The input power received from the distribution network in watts (W).

        Returns:
            float: The power consumed by the consumer in watts (W).
        """
        self.input_power = input_power
        self.consumed_power = min(self.input_power, self.consumption_rate)
        return self.consumed_power

    def __str__(self):
        """Return a string representation of the consumer."""
        return (f"{self.name} (Input Power: {self.input_power} W, Consumption Rate: {self.consumption_rate} W, "
                f"Consumed Power: {self.consumed_power} W)")

