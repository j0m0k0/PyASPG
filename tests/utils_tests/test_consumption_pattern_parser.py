import os
import pytest
import pandas as pd
from pyaspg.utils import ConsumptionPatternParser

# Create a temporary CSV file for testing
@pytest.fixture(scope="module")
def temp_csv():
    data = {
        "Global_active_power": [1.5, 1.6, 1.7, 1.8],
        "Sub_metering_1": [10, 15, 20, 25],
        "Sub_metering_2": [5, 10, 15, 20],
        "Sub_metering_3": [3, 6, 9, 12]
    }
    df = pd.DataFrame(data)
    temp_csv_path = "temp_test_consumption.csv"
    df.to_csv(temp_csv_path, index=False)
    yield temp_csv_path
    os.remove(temp_csv_path)

def test_initialization(temp_csv):
    parser = ConsumptionPatternParser(temp_csv, bias=10)
    assert parser.bias == 10
    assert parser.timestep == 0
    assert not parser.consumption_data.empty

def test_get_consumption_without_bias(temp_csv):
    parser = ConsumptionPatternParser(temp_csv, bias=0)
    consumption = next(parser)
    expected_consumption = 1.5 * 1000 + 10 + 5 + 3  # Calculation based on the first row
    assert consumption == pytest.approx(expected_consumption, rel=1e-3)

def test_get_consumption_with_bias(temp_csv):
    parser = ConsumptionPatternParser(temp_csv, bias=10)
    consumption = next(parser)
    expected_consumption = 1.5 * 1000 + 10 + 5 + 3 + 10  # Calculation based on the first row plus bias
    assert consumption == pytest.approx(expected_consumption, rel=1e-3)
    assert parser.timestep == 1  # Ensure the timestep has advanced

def test_timestep_reset(temp_csv):
    parser = ConsumptionPatternParser(temp_csv, bias=0)
    for _ in range(len(parser.consumption_data) + 1):
        next(parser)
    assert parser.timestep == 1  # Ensure timestep resets after reaching the end

def test_infinite_loop(temp_csv):
    parser = ConsumptionPatternParser(temp_csv, bias=0)
    consumption_values = [next(parser) for _ in range(len(parser.consumption_data) * 2)]
    assert len(consumption_values) == len(parser.consumption_data) * 2
    assert consumption_values[:len(parser.consumption_data)] == consumption_values[len(parser.consumption_data):]
