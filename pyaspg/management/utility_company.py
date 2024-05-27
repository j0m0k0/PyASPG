class UtilityCompany:
    """
    Class representing a utility company that manages the generation, transmission, and distribution of electricity.

    Attributes:
        name (str): The name of the utility company.
        received_data (list): The list of aggregated data packets received from net aggregators.
    """

    def __init__(self, name):
        """
        Initialize a UtilityCompany instance.

        Args:
            name (str): The name of the utility company.
        """
        self.name = name
        self.received_data = []

    def receive_data(self, data):
        """
        Receive aggregated data from a net aggregator.

        Args:
            data (dict): The aggregated data to be received.
        """
        self.received_data.append(data)
        print(f"UtilityCompany {self.name} received data: {data}")

    def manage_grid(self):
        """
        Manage the grid based on received data. This is a placeholder for actual grid management logic.
        """
        total_usage = sum(d['total_usage'] for d in self.received_data)
        total_production = sum(d['total_production'] for d in self.received_data)
        total_stored_energy = sum(d['total_stored_energy'] for d in self.received_data)

        # Placeholder for grid management logic
        print(f"Managing grid... Total Usage: {total_usage} W, Total Production: {total_production} W, "
              f"Total Stored Energy: {total_stored_energy} W")

    def __str__(self):
        """Return a string representation of the utility company."""
        return (f"UtilityCompany {self.name} (Received Data Packets: {len(self.received_data)})")

# Example usage
def main():
    # Creating instances for testing
    utility_company = UtilityCompany(name="Utility Company 1")
    
    # Mock data to simulate aggregated data from net aggregators
    aggregated_data_1 = {
        "total_usage": 10000,
        "total_production": 8000,
        "total_stored_energy": 2000
    }
  
    aggregated_data_2 = {
        "total_usage": 15000,
        "total_production": 12000,
        "total_stored_energy": 3000
    }

    # Simulating receiving data
    utility_company.receive_data(aggregated_data_1)
    utility_company.receive_data(aggregated_data_2)

    # Managing the grid based on received data
    utility_company.manage_grid()

    print(utility_company)

if __name__ == "__main__":
    main()
