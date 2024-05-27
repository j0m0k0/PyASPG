import pytest
from pyaspg.distribution.transmitter import Transmitter

def test_transmitter_initialization():
    """
    Test the initialization of the Transmitter class.
    """
    transmitter = Transmitter(name="High Voltage Line 1", efficiency=0.97, distance=100)
    
    assert transmitter.name == "High Voltage Line 1"
    assert transmitter.efficiency == 0.97
    assert transmitter.distance == 100
    assert transmitter.input_power == 0
    assert transmitter.output_power == 0

def test_transmission():
    """
    Test the transmission of power.
    """
    transmitter = Transmitter(name="High Voltage Line 1", efficiency=0.97, distance=100)
    input_power = 1000000  # 1 MW input power
    expected_output_power = input_power * (1 - (1 - 0.97) * 100 / 100)
    
    output_power = transmitter.transmit(input_power)
    
    assert output_power == pytest.approx(expected_output_power, rel=1e-3)
    assert transmitter.input_power == input_power
    assert transmitter.output_power == output_power

def test_power_loss_over_distance():
    """
    Test that the power loss increases with distance.
    """
    transmitter_short = Transmitter(name="Short Distance Line", efficiency=0.97, distance=50)
    transmitter_long = Transmitter(name="Long Distance Line", efficiency=0.97, distance=200)
    input_power = 1000000  # 1 MW input power
    
    output_power_short = transmitter_short.transmit(input_power)
    output_power_long = transmitter_long.transmit(input_power)
    
    assert output_power_short > output_power_long
    assert transmitter_short.output_power == output_power_short
    assert transmitter_long.output_power == output_power_long

def test_transmit_large_distance():
    """
    Test the transmission of electricity over a very large distance.
    """
    transmitter = Transmitter(name="Long Distance Line", efficiency=0.97, distance=10000)
    input_power = 1000000  # 1 MW input power
    
    output_power = transmitter.transmit(input_power)
    
    assert output_power >= 0  # Output power should never be negative
    assert output_power <= input_power  # Output power should not exceed input power
