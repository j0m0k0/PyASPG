import os
import csv
from pyaspg.generation import WindTurbine, SolarPanel


class DataLog:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.files = {}
        self.writers = {}

    def initialize_files(self, components):
        for component_type, component_list in components.items():
            if component_list:
                file_path = os.path.join(self.output_dir, f"{component_type}.csv")
                self.files[component_type] = open(file_path, 'w', newline='')
                self.writers[component_type] = csv.writer(self.files[component_type])
                header = ['timestep'] + [attr for attr in vars(component_list[0]).keys() if attr != 'env']
                if component_type == "generators":
                    if isinstance(component_list[0], WindTurbine):
                        header.append('wind_speed')
                    elif isinstance(component_list[0], SolarPanel):
                        header.append('sunlight')
                self.writers[component_type].writerow(header)

    def log_data(self, timestep, components, param_value=None):
        for component_type, component_list in components.items():
            if component_list:
                writer = self.writers[component_type]
                for component in component_list:
                    data = [timestep] + [getattr(component, attr) for attr in vars(component) if attr != 'env']
                    if component_type == "generators" and param_value is not None:
                        data.append(param_value)
                    writer.writerow(data)

    def close_files(self):
        for f in self.files.values():
            f.close()
