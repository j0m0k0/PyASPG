from .consumer import Consumer


class Household(Consumer):
    """
    Class representing a household consumer of electricity.
    """
    def __init__(self, name, consumption_rate=5000):
        """
        Initialize a Household instance.

        Args:
            name (str): The name of the household.
            consumption_rate (float): The rate of electricity consumption in watts (W), default is 5000 W.
        """
        super().__init__(name, consumption_rate)

# Example usage
def main():
    household = Household(name="Household 1")


    input_power = 10000  # 10 kW input power

    print(household)
    print(f"Consumed Power: {household.consume(input_power)} W")

if __name__ == "__main__":
    main()
