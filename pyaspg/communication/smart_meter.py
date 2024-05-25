from consumer.household import Household


class SmartMeter:
    """
    Class representing a smart meter that measures electricity usage and communicates with utility companies and third-party data aggregators.

    Attributes:
        consumer (Consumer): The consumer associated with this smart meter.
        usage_data (float): The total electricity usage measured by the smart meter in watts (W).
    """

    def __init__(self, consumer):
        """
        Initialize a SmartMeter instance.

        Args:
            consumer (Consumer): The consumer associated with this smart meter.
        """
        self.consumer = consumer
        self.usage_data = 0

    def measure_usage(self):
        """
        Measure the electricity usage of the consumer.

        Returns:
            float: The current electricity usage in watts (W).
        """
        current_usage = self.consumer.consumed_power
        self.usage_data += current_usage
        return current_usage

    def send_data(self):
        """
        Simulate sending real-time usage data to utility companies and third-party aggregators.

        Returns:
            float: The total electricity usage data sent in watts (W).
        """
        return self.usage_data

    def __str__(self):
        """Return a string representation of the smart meter."""
        return (f"SmartMeter for {self.consumer.name} (Total Usage Data: {self.usage_data} W)")

# Example usage
def main():
    household = Household(name="Household 1")
    smart_meter = SmartMeter(consumer=household)

    input_power = 10000  # 10 kW input power

    # Simulate consumption
    household.consume(input_power)
    smart_meter.measure_usage()

    # Simulate sending data
    usage_data = smart_meter.send_data()
    print(smart_meter)
    print(f"Usage Data Sent: {usage_data} W")

if __name__ == "__main__":
    main()
