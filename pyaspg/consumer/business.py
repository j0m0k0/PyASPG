from .consumer import Consumer


class Business(Consumer):
    """
    Class representing a business consumer of electricity.
    """
    def __init__(self, name, consumption_rate=20000):
        """
        Initialize a Business instance.

        Args:
            name (str): The name of the business.
            consumption_rate (float): The rate of electricity consumption in watts (W), default is 20000 W.
        """
        super().__init__(name, consumption_rate)

# Example usage
def main():
  
    business = Business(name="Business 1")
    
    input_power = 10000  # 10 kW input power

    print(business)
    print(f"Consumed Power: {business.consume(input_power)} W")

if __name__ == "__main__":
    main()
