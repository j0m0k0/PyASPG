import os
import csv
from pyaspg.generation import WindTurbine, SolarPanel
from pyaspg.utils import log_me

@log_me
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
                
                # Define headers
                if component_type == 'prosumers':
                    header = ['timestep', 'name', 'stored_energy_before', 'net_power_before', 'received_power', 'stored_energy', 'net_power', 'distributor_name']
                else:
                    header = ['timestep'] + [attr for attr in vars(component_list[0]).keys() if attr != 'env']

                # Add wind_speed or sunlight to the header if applicable
                if component_type == 'generators':
                    for source, target, params in connections['generator_to_transmitter']:
                        if 'wind_speed' in params:
                            header.append('wind_speed')
                        elif 'sunlight' in params:
                            header.append('sunlight')
                
                # Add specific headers for distributors
                if component_type == 'distributors':
                    header.extend(['power_to_prosumers'])

                self.writers[component_type].writerow(header)
                
                # Save params for later use
                if component_type == 'generators':
                    self.params[component_type] = params

    def log_data(self, timestep, components, connections):
        for component_type, component_list in components.items():
            if component_list:
                writer = self.writers[component_type]
                for i, component in enumerate(component_list):
                    data = [timestep]
                    if component_type == 'prosumers':
                        data.extend([
                            component.name,
                            component.stored_energy_before,
                            component.net_power_before,
                            component.received_power,
                            component.stored_energy,
                            component.net_power,
                            component.distributor_name
                        ])
                    else:
                        data += [getattr(component, attr) for attr in vars(component) if attr != 'env']
                    
                    # Add wind_speed or sunlight to the data if applicable
                    if component_type == 'generators':
                        for source, target, params in connections['generator_to_transmitter']:
                            if source == component:
                                if 'wind_speed' in params:
                                    data.append(params['wind_speed'][timestep // 10])
                                elif 'sunlight' in params:
                                    data.append(params['sunlight'][timestep // 10])
                    
                    # Add specific data for distributors
                    if component_type == 'distributors':
                        power_to_prosumers = sum([target.received_power for _, target, _ in connections['distributor_to_prosumer'] if _ == component])
                        data.append(power_to_prosumers)

                    writer.writerow(data)

    def close_files(self):
        for f in self.files.values():
            f.close()
