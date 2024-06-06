import pandas as pd
import os

class ConsumptionPatternParser:
    """
    Class to parse and provide consumption data from a CSV file with an optional bias.
    """

    def __init__(self, file_path, bias=0):
        """
        Initialize the ConsumptionPatternParser instance.

        Args:
            file_path (str): The path to the CSV file containing consumption data.
            bias (float): The bias to be added to each total meter reading. Default is 0.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        self.consumption_data = pd.read_csv(file_path)
        self.bias = bias
        self.timestep = 0

    def __iter__(self):
        """
        Make the class an iterator.
        """
        return self

    def __next__(self):
        """
        Return the next consumption value, looping infinitely through the data.

        Returns:
            float: The total consumption for the current timestep plus the bias.
        """
        if self.timestep >= len(self.consumption_data):
            self.timestep = 0  # Reset to the beginning of the data

        row = self.consumption_data.iloc[self.timestep]
        total_consumption = (row['Global_active_power'] * 1000 +
                             row['Sub_metering_1'] +
                             row['Sub_metering_2'] +
                             row['Sub_metering_3'] +
                             self.bias)
        self.timestep += 1
        return total_consumption
