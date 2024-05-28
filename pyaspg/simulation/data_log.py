import os
import csv
from pyaspg.generation import WindTurbine, SolarPanel


class DataLog:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.files = {}
        self.writers = {}
        self.params = {}

    def initialize_files(self, components, connections):
        for component_type, component_list in components.items():
            if component_list:
                file_path = os.path.join(self.output_dir, f"{component_type}.csv")
                self.files[component_type] = open(file_path, 'w', newline='')
                self.writers[component_type] = csv.writer(self.files[component_type])
                header = ['timestep'] + [attr for attr in vars(component_list[0]).keys() if attr != 'env']
                
                # Add wind_speed or sunlight to the header if applicable
                if component_type == 'generators':
                    for source, target, params in connections['generator_to_transmitter']:
                        if 'wind_speed' in params:
                            header.append('wind_speed')
                        elif 'sunlight' in params:
                            header.append('sunlight')

                self.writers[component_type].writerow(header)
                
                # Save params for later use
                if component_type == 'generators':
                    self.params[component_type] = params

    def log_data(self, timestep, components, connections):
        for component_type, component_list in components.items():
            if component_list:
                writer = self.writers[component_type]
                for i, component in enumerate(component_list):
                    data = [timestep] + [getattr(component, attr) for attr in vars(component) if attr != 'env']
                    
                    # Add wind_speed or sunlight to the data if applicable
                    if component_type == 'generators':
                        for source, target, params in connections['generator_to_transmitter']:
                            if source == component:
                                if 'wind_speed' in params:
                                    data.append(params['wind_speed'][timestep // 10])
                                elif 'sunlight' in params:
                                    data.append(params['sunlight'][timestep // 10])

                    writer.writerow(data)

    def close_files(self):
        for f in self.files.values():
            f.close()
