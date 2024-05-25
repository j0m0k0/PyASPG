import pytest
from distribution.distributor import Distributor

def test_distributor_initialization():
    """
    Test the initialization of the Distributor class.
    """
    distributor = Distributor(name="Low Voltage Line 1", efficiency=0.9, distance=10)
    
    assert distributor.name == "Low Voltage Line 1"
    assert distributor.efficiency == 0.9
    assert distributor.distance == 10
    assert distributor.input_power == 0
    assert distributor.output_power == 0

def test_distribution():
    """
    Test the distribution of power.
    """
    distributor = Distributor(name="Low Voltage Line 1", efficiency=0.9, distance=10)
    input_power = 1000000  # 1 MW input power
    expected_output_power = input_power * (1 - (1 - 0.9) * 10 / 10)
    
    output_power = distributor.distribute(input_power)
    
    assert output_power == pytest.approx(expected_output_power, rel=1e-3)
    assert distributor.input_power == input_power
    assert distributor.output_power == output_power

def test_power_loss_over_distance():
    """
    Test that the power loss increases with distance.
    """
    distributor_short = Distributor(name="Short Distance Line", efficiency=0.9, distance=5)
    distributor_long = Distributor(name="Long Distance Line", efficiency=0.9, distance=20)
    input_power = 1000000  # 1 MW input power
    
    output_power_short = distributor_short.distribute(input_power)
    output_power_long = distributor_long.distribute(input_power)
    
    assert output_power_short > output_power_long
    assert distributor_short.output_power == output_power_short
    assert distributor_long.output_power == output_power_long