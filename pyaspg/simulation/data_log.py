import os
import csv

class DataLog:
    """
    Class to handle logging data into CSV files.

    Attributes:
        output_dir (str): Directory where the CSV files will be saved.
        files (dict): Dictionary to store file handles.
        writers (dict): Dictionary to store CSV writers.
    """

    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.files = {}
        self.writers = {}

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def initialize_files(self, components):
        """
        Create a CSV file for each component type.

        Args:
            components (dict): Dictionary of components.
        """
        for component_type, component_list in components.items():
            if component_list:
                file_path = os.path.join(self.output_dir, f"{component_type}.csv")
                self.files[component_type] = open(file_path, 'w', newline='')
                self.writers[component_type] = csv.writer(self.files[component_type])
                header = ['timestep'] + [attr for attr in vars(component_list[0]).keys() if attr != 'env']
                self.writers[component_type].writerow(header)

    def log_data(self, timestep, components):
        """
        Log data for each component type at a given timestep.

        Args:
            timestep (int): Current timestep.
            components (dict): Dictionary of components.
        """
        for component_type, component_list in components.items():
            if component_list:
                writer = self.writers[component_type]
                for component in component_list:
                    data = [timestep] + [getattr(component, attr) for attr in vars(component) if attr != 'env']
                    writer.writerow(data)

    def close_files(self):
        """
        Close all open files.
        """
        for f in self.files.values():
            f.close()
