import os
import csv
from pyaspg.utils import log_me

@log_me
class DataLog:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.files = {}
        self.writers = {}
        self.log_config = {           
            'smart_meters': {
                'header': ['timestep', 'prosumer_name', 'total_consumption', 'total_production', 'net_read', 'is_sent', 'consumption', 'production'],
                'data': lambda t, c, conn: [
                    t, c.prosumer.name, c.prosumer.total_consumption, c.prosumer.total_production, c.prosumer.net_power_before,
                    1 if c.communication_network.transmit_data(c.data) else 0,
                    c.prosumer.last_generated_consumption, c.prosumer.last_generated_production
                ]
            },
            'generators': {
                'header': ['timestep', 'name', 'nominal_capacity', 'input', 'output', 'controller'],
                'data': lambda t, c, conn: [
                    t, c.name, c.nominal_capacity, c.input, c.output, c.controller.name
                ]
            },
            'transmitters': {
                'header': ['timestep', 'name', 'input', 'output', 'distance', 'efficiency', 'connected_generators'],
                'data': lambda t, c, conn: [
                    t, c.name, c.input_power, c.output_power, c.distance, c.efficiency, [g.name for g in c.generators]
                ]
            },
            'substations': {
                'header': ['timestep', 'name', 'input', 'output', 'efficiency'],
                'data': lambda t, c, conn: [
                    t, c.name, c.input_power, c.output_power, c.efficiency
                ]
            },
            'distributors': {
                'header': ['timestep', 'name', 'input', 'output', 'efficiency', 'distance'],
                'data': lambda t, c, conn: [
                    t, c.name, c.input_power, c.output_power, c.efficiency, c.distance,
                ]
            },
            # Why I didn't showed the c.net_power in the net_power column?
            # Because in practice it becomes zero, no matter if we received
            # enough power or not. Therefore in the reporting it was not 
            # proper to show it. But in the simulator itself, it becomes 
            # zero since we reset the net power every timestep for each
            #  prosumer.
            'prosumers': {
                'header': ['timestep', 'name', 'net_power_before', 'received_power', 'net_power', 'stored_energy_before', 'stored_energy', 'storage_capacity', 'distributor_name', 'prosumer_type'],
                'data': lambda t, c, conn: [
                    t, c.name, c.net_power_before, c.received_power, c.net_power_before - c.received_power, c.stored_energy_before, c.stored_energy, c.storage_capacity, c.distributor_name, c.prosumer_type
                ]
            },
            'aggregators': {
                'header': ['timestep', 'name', 'prosumers', 'data_collected'],
                'data': lambda t, c, conn: [
                    t, c.name, [i.prosumer.name for i in c.smart_meters], c.data_collected[t]
                ]
            },
            'utility_companies': {
                'header': ['timestep', 'name', 'generators', 'total_prosumers_consumption', 'total_prosumers_production', 'total_prosumers_stored_energy', 'total_prosumers_net_power'],
                'data': lambda t, c, conn: [
                    # [t, c.name, [g.name for g in c.generators], c.received_data[-1]['total_consumption'], c.received_data[-1]['total_production']]
                    [t, c.name, [g.name for g in c.generators], sum(d['total_consumption'] for d in c.received_data), sum(d['total_production'] for d in c.received_data), sum(d['total_stored_energy'] for d in c.received_data), sum(d['total_net_power'] for d in c.received_data)]
                ]
            },
            'control_systems': {
                'header': ['timestep', 'utility_name', 'total_net_power', 'total_consumption', 'total_production', 'total_stored_energy', 'predicted_demand', 'predictor_error'],
                'data': lambda t, c, conn: [
                    [t, c.utility_data[-1]['utility_name'], c.utility_data[-1]['total_net_power'], c.utility_data[-1]['total_consumption'], c.utility_data[-1]['total_production'], c.utility_data[-1]['total_stored_energy'], c.predicted_demand[c.utility_data[-1]['utility_name']] if c.predicted_demand is not None else 0.0, c.generated_random_error if c.generated_random_error is not None else 0.0]
                ]
            },
        }

    def initialize_files(self, components, connections):
        for component_type, component_list in components.items():
            if component_list:
                file_path = os.path.join(self.output_dir, f"{component_type}.csv")
                self.files[component_type] = open(file_path, 'w', newline='')
                self.writers[component_type] = csv.writer(self.files[component_type])

                header = self.log_config.get(component_type, {}).get('header', ['timestep'])
                self.writers[component_type].writerow(header)


    def log_data(self, timestep, components, connections):
        for component_type, component_list in components.items():
            if component_list:
                writer = self.writers[component_type]
                data_func = self.log_config.get(component_type, {}).get('data', lambda t, c, conn: [t])

                for component in component_list:
                    data = data_func(timestep, component, connections)
                    if isinstance(data[0], list):  # For control_systems
                        for d in data:
                            writer.writerow(d)
                    else:
                        writer.writerow(data)

    def close_files(self):
        for f in self.files.values():
            f.close()
