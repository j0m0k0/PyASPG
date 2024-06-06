import pytest
from pyaspg.distribution.substation import Substation

def test_substation_initialization():
    """
    Test the initialization of the Substation class.
    """
    substation = Substation(name="Main Substation", input_voltage=25000, output_voltage=10000, efficiency=0.98)
    
    assert substation.name == "Main Substation"
    assert substation.input_voltage == 25000
    assert substation.output_voltage == 10000
    assert substation.efficiency == 0.98
    assert substation.input_power == 0
    assert substation.output_power == 0

def test_transformation():
    """
    Test the transformation of power.
    """
    substation = Substation(name="Main Substation", input_voltage=25000, output_voltage=10000, efficiency=0.98)
    input_power = 1000000  # 1 MW input power
    expected_output_power = input_power * 0.98
    
    substation.receive(input_power)
    output_power = substation.transform()
    
    assert output_power == pytest.approx(expected_output_power, rel=1e-3)
    assert substation.input_power == input_power
    assert substation.output_power == output_power

def test_voltage_constraints():
    """
    Test that the input voltage is higher than the output voltage.
    """
    with pytest.raises(ValueError):
        Substation(name="Invalid Voltage", input_voltage=10000, output_voltage=25000, efficiency=0.98)

def test_substation_transform():
    """
    Test the transformation of electricity in the Substation class.
    """
    substation = Substation(name="Main Substation", input_voltage=25000, output_voltage=10000, efficiency=0.98)
    input_power = 1000000  # 1 MW input power
    
    substation.receive(input_power)
    output_power = substation.transform()
    
    assert output_power == input_power * 0.98  # Check that the output power matches the expected value
    assert substation.output_current == output_power / substation.output_voltage  # Check the calculated current