import os
import csv
import pytest
from pyaspg.simulation import PyASPGCreator, GridSimulator
from pyaspg.distribution import Transmitter, Distributor, Substation
from pyaspg.prosume import Prosumer
from pyaspg.generation import WindTurbine, SolarPanel

@pytest.fixture
def setup_simulation():
    grid_creator = PyASPGCreator()

    # Create components
    wind_turbine = WindTurbine(name="WT1", nominal_capacity=2000, voltage=25000)
    transmitter = Transmitter(name="HVL1", efficiency=0.97, distance=100)
    substation = Substation(name="MS1", input_voltage=25000, output_voltage=10000, efficiency=0.98)
    distributor = Distributor(name="LVL1", efficiency=0.9, distance=10)

    p_to_d = []
    for i in range(1):
        _h = Prosumer(name=f"H{i+1}", prosumer_type="House", storage_capacity=5000, consumption_file="consumption_patterns/2006-12-16.csv", bias=(i+1)*5, production_pattern=(600, 150))
        p_to_d.append((distributor, _h))

    # Define connections between components with parameters
    grid_creator.define_connections(
        generator_to_transmitter=[
            (wind_turbine, transmitter, {'wind_speed': [0.8, 0.6, 0.7]}),
        ],
        transmitter_to_substation=[(transmitter, substation)],
        substation_to_distributor=[(substation, distributor)],
        distributor_to_prosumer=p_to_d
    )

    # Run the simulation
    simulator = GridSimulator(grid_creator)
    simulator.run_simulation(duration=30, timestep=10, output_dir='test_simulation_results')

    return 'test_simulation_results'

def test_csv_columns_no_duplicates(setup_simulation):
    output_dir = setup_simulation
    csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]

    for csv_file in csv_files:
        with open(os.path.join(output_dir, csv_file), 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            print(f"{csv_file=}, {headers=}")
            assert len(headers) == len(set(headers)), f"Duplicate columns found in {csv_file}"
