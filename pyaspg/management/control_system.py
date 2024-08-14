from pyaspg.utils import log_me

@log_me
class ControlSystem:
    """
    Class representing control systems that manage the operation of the power grid, including demand response and load balancing.

    Attributes:
        name (str): The name of the control system.
        utility_companies (list): The list of utility companies.
        utility_data (list): The data received from utility companies.
        safety_margin (float): The safety margin for power generation to prevent blackouts.
    """

    def __init__(self, name, safety_margin=1.2):
        """
        Initialize a ControlSystem instance.

        Args:
            name (str): The name of the control system.
            safety_margin (float): The safety margin for power generation to prevent blackouts.
        """
        self.name = name
        self.utility_companies = []
        self.utility_data = []
        self.safety_margin = safety_margin
        self.predicted_demand = None

    def register_utility_company(self, utility_company):
        """
        Add a utility company to the list of utility companies under the control of this control system.

        Args:
            utility_company: The utility company to be registered.
        """
        self.utility_companies.append(utility_company)

    def receive_data(self, data):
        """
        Receive data from utility companies.

        Args:
            data (dict): The data to be received from utility companies.
        """

        self.utility_data.append(data)

    def predict_demand(self):
        """
        Predict future power needs and set the predicted_demand attribute for each utility company.
        """
        if not self.utility_data:
            return


        utility_demand_predictions = {}
        for utility_company in self.utility_companies:
            relevant_data = [data for data in self.utility_data if data['utility_name'] == utility_company.name]
            if not relevant_data:
                continue
            
            # if len(relevant_data) >= 2:
            #     recent_data = relevant_data[-2:]
            #     current_consumption = recent_data[-1]['total_consumption'] - recent_data[-2]['total_consumption']
            # else:
            #     current_consumption = relevant_data[-1]['total_consumption']
            current_consumption = relevant_data[-1]['total_net_power']
            
            utility_demand_predictions[utility_company.name] = current_consumption * self.safety_margin

        self.predicted_demand = utility_demand_predictions


    def distribute_demand(self):
        """
        Distribute the predicted demand among the registered generators based on their nominal capacities.

        Returns:
            dict: A dictionary with generator names as keys and their respective power demands as values.
        """
        demand_distribution = {}

        for utility_company in self.utility_companies:
            utility_demand = self.predicted_demand.get(utility_company.name, -1) if self.predicted_demand else -1
            total_nominal_capacity = sum(gen.nominal_capacity for gen in utility_company.generators)

            if total_nominal_capacity == 0:
                continue

            if utility_demand == -1:
                for generator in utility_company.generators:
                    demand_distribution[generator.name] = 1.0
            else:
                for generator in utility_company.generators:
                    share = generator.nominal_capacity / total_nominal_capacity
                    required_power = utility_demand * share
                    fraction_of_nominal_capacity = min(1.0, max(0.0, required_power / generator.nominal_capacity))
                    demand_distribution[generator.name] = fraction_of_nominal_capacity
            
        return demand_distribution



    def get_demand(self, generator_name):
        """
        Get the predicted demand for a specific generator.

        Args:
            generator_name (str): The name of the generator.

        Returns:
            float: The predicted power demand for the generator.
        """
        demand_distribution = self.distribute_demand()

        return demand_distribution.get(generator_name, 0)

    def update_prediction(self, timestep, update_interval):
        """
        Update the demand prediction at specified intervals.

        Args:
            timestep (int): The current timestep of the simulation.
            update_interval (int): The interval at which to update the prediction.
        """
        if timestep % update_interval == 0:
            self.predict_demand()

    def __str__(self):
        """Return a string representation of the control system."""
        return (f"ControlSystem {self.name} (Utility Companies: {self.utility_companies})")
