import pandas as pd

from pyaspg.utils import log_me, generate_random_error


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

    def __init__(self, name, safety_margin=1.0, uc_frame=None, cs_frame=None, error_rate=0.0):
        """
        Initialize a ControlSystem instance.

        Args:
            name (str): The name of the control system.
            safety_margin (float): The safety margin for power generation to prevent blackouts.
        """
        self.name = name
        self.utility_companies = []
        # utility_data is only used when we are not in replay mode
        self.utility_data = []
        self.safety_margin = safety_margin
        self.predicted_demand = None

        # utility company frame for replay mode
        # this data is necessary for logging correct data in the control_systems.csv
        self.uc_frame = uc_frame

        # control system frame for replay mode
        self.cs_frame = cs_frame

        # error_rate is the error range we declare for the ideal predictor
        # the actual error will be generated randomly within this range
        # using the generate_random_error function
        # so the eventual error will be stored at generated_random_error
        # for every timestep
        # in replay_mode, it will be read from the replay data
        self.error_rate = error_rate
        self.generated_random_error = None

        self.bias_collection = {}

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

    def ideal_predictor(self, timestep, attacked=False):
        utility_demand_predictions = {}
        for utility_company in self.utility_companies:
            # ideal predictor without attack, generates the error randomly            
            _total_net_power = (self.cs_frame.loc[
                        (self.cs_frame['timestep'] == timestep + 1) & (self.cs_frame['utility_name'] == utility_company.name),
                        'total_net_power'
                    ].values)
            # print("total net before: ", _total_net_power)
            if attacked:
                try:
                    self.generated_random_error = self.cs_frame.loc[
                        (self.cs_frame['timestep'] == timestep + 1) & (self.cs_frame['utility_name'] == utility_company.name),
                        'predictor_error'
                    ].values[0]
                except IndexError:
                    self.generated_random_error = generate_random_error(self.error_rate)
                # add the bias that we received to the _total_net_power
                # data is like this: {80: [{'name': 'NA1', 'data': 44.45440534186522}, {'name': 'NA1', 'data': 42.36084480489373}, {'name': 'NA1', 'data': 44.739440229669775}, {'name': 'NA1', 'data': 45.427594804231575}, {'name': 'NA1', 'data': 44.39472485585387}, {'name': 'NA1', 'data': 45.15459771637452}, {'name': 'NA1', 'data': 47.47227813312898}, {'name': 'NA1', 'data': 42.875716077032926}, {'name': 'NA1', 'data': 42.54645832883865}, {'name': 'NA1', 'data': 45.969003124130495}]}
                try:
                    bias_term = sum([i['data'] for i in self.bias_collection[timestep]])
                    _total_net_power += bias_term
                except KeyError:
                    # print("Error: No bias data for timestep", timestep)
                    pass
                # _total_net_power += [i['data'] for i in self.bias_collection[timestep]]

            else:
                    self.generated_random_error = generate_random_error(self.error_rate)

            # print("total net after: ", _total_net_power)
            demand = _total_net_power * self.safety_margin * (1 - self.generated_random_error)

            # print(f"XOXO {timestep=} {_total_net_power=} {demand=} {self.generated_random_error=} {self.safety_margin=}")

            if len(demand) > 0:
                # Ideal prediction assumes perfect knowledge of future demand
                utility_demand_predictions[utility_company.name] = demand[0]
        # print(f"{timestep=} {self.predicted_demand=}")
        self.predicted_demand = utility_demand_predictions

    def replay_update_prediction(self, timestep, update_interval, attacked, predictor='ideal'):
        """
        Update the demand prediction based on replay data for the specified timestep.

        Args:
            timestep (int): The current timestep of the simulation.
            predictor (str): The predictor type. Default is 'ideal'.
        """
        if predictor != 'ideal':
            raise NotImplementedError("Only 'ideal' predictor is currently implemented.")

        if self.cs_frame is None:
            raise ValueError("No replay data available for replay mode.")

        if timestep % update_interval == 0:
                self.ideal_predictor(timestep, attacked)

    def receive_message(self, message_type, timestep, data):
        if message_type == "bias":
            try:
                self.bias_collection[timestep].append(data)
            except KeyError:
                self.bias_collection[timestep] = [data]
            # print(f"ControlSystem {self.name} received a bias message from {data['name']} at timestep {timestep}: {data}")
            # print(self.bias_collection)
    
    def __str__(self):
        """Return a string representation of the control system."""
        return (f"ControlSystem {self.name} (Utility Companies: {self.utility_companies})")
