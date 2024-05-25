from .consumer import Consumer


class Industry(Consumer):
    """
    Class representing an industrial consumer of electricity.
    """
    def __init__(self, name, consumption_rate=100000):
        """
        Initialize an Industry instance.

        Args:
            name (str): The name of the industry.
            consumption_rate (float): The rate of electricity consumption in watts (W), default is 100000 W.
        """
        super().__init__(name, consumption_rate)


# Example usage
def main():
    industry = Industry(name="Industry 1")

    input_power = 10000  # 10 kW input power

    print(industry)
    print(f"Consumed Power: {industry.consume(input_power)} W")

if __name__ == "__main__":
    main()
