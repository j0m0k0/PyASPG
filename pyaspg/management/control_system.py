from pyaspg.management.net_aggregator import NetAggregator

class ControlSystem:
    """
    Class representing control systems that manage the operation of the power grid, including demand response and load balancing.

    Attributes:
        name (str): The name of the control system.
        grid_data (dict): The data from various parts of the grid.
    """

    def __init__(self, name):
        """
        Initialize a ControlSystem instance.

        Args:
            name (str): The name of the control system.
        """
        self.name = name
        self.grid_data = {
            "generation": {},
            "transmission": {},
            "distribution": {},
            "consumption": {}
        }

    def update_grid_data(self, component, data):
        """
        Update the grid data for a specific component.

        Args:
            component (str): The component of the grid (generation, transmission, distribution, consumption).
            data (dict): The data to update for the specified component.
        """
        if component in self.grid_data:
            self.grid_data[component].update(data)
        else:
            raise ValueError("Invalid grid component")

    def analyze_grid(self):
        """
        Analyze the grid data to optimize operations, manage demand, and ensure stability.

        Returns:
            dict: The commands to optimize grid operations.
        """
        total_generation = sum(self.grid_data["generation"].values())
        total_consumption = sum(self.grid_data["consumption"].values())
        total_transmission = sum(self.grid_data["transmission"].values())
        total_distribution = sum(self.grid_data["distribution"].values())

        commands = {
            "load_balancing": None,
            "demand_response": None,
            "stability": None
        }

        # Example logic for load balancing
        if total_generation > total_consumption:
            commands["load_balancing"] = "Reduce generation"
        elif total_generation < total_consumption:
            commands["load_balancing"] = "Increase generation"

        # Example logic for demand response
        if total_consumption > total_generation * 0.9:
            commands["demand_response"] = "Send demand response signal to consumers"

        # Example logic for stability
        if total_transmission > total_generation * 0.8 or total_distribution > total_generation * 0.8:
            commands["stability"] = "Adjust transmission and distribution to ensure stability"

        return commands

    def issue_commands(self, net_aggregator, commands):
        """
        Issue commands to net aggregators to optimize grid operations.

        Args:
            net_aggregator (NetAggregator): The net aggregator to send commands to.
            commands (dict): The commands to be issued.
        """
        for command, message in commands.items():
            if message:
                net_aggregator.receive_command(command, message)

    def __str__(self):
        """Return a string representation of the control system."""
        return (f"ControlSystem {self.name} (Grid Data: {self.grid_data})")

# Example usage
def main():
    control_system = ControlSystem(name="Control System 1")
    
    # Mock data to simulate updates from various parts of the grid
    generation_data = {"Plant 1": 5000, "Plant 2": 7000}
    transmission_data = {"Line 1": 6000, "Line 2": 4000}
    distribution_data = {"Region 1": 8000, "Region 2": 3000}
    consumption_data = {"Household 1": 2000, "Business 1": 3000}

    # Updating grid data
    control_system.update_grid_data("generation", generation_data)
    control_system.update_grid_data("transmission", transmission_data)
    control_system.update_grid_data("distribution", distribution_data)
    control_system.update_grid_data("consumption", consumption_data)

    # Analyzing grid data
    commands = control_system.analyze_grid()
    print("Analyzed Commands:", commands)

    # Mock net aggregator to simulate issuing commands
    class MockNetAggregator:
        def __init__(self):
            self.received_commands = []

        def receive_command(self, command, message):
            self.received_commands.append((command, message))
            print(f"Received command: {command} - {message}")

    net_aggregator = MockNetAggregator()
    control_system.issue_commands(net_aggregator, commands)

    print(control_system)

if __name__ == "__main__":
    main()
