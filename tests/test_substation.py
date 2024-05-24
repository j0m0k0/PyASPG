import pytest
from Substation import Substation

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
    
    output_power = substation.transform(input_power)
    
    assert output_power == pytest.approx(expected_output_power, rel=1e-3)
    assert substation.input_power == input_power
    assert substation.output_power == output_power

def test_voltage_constraints():
    """
    Test that the input voltage is higher than the output voltage.
    """
    with pytest.raises(ValueError):
        Substation(name="Invalid Voltage", input_voltage=10000, output_voltage=25000, efficiency=0.98)