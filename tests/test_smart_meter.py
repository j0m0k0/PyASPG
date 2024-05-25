import pytest
from consumer import Consumer, Household
from communication.smart_meter import SmartMeter


def test_smart_meter_initialization():
    """
    Test the initialization of the SmartMeter class.
    """
    household = Household(name="Household 1")
    smart_meter = SmartMeter(consumer=household)
    
    assert smart_meter.consumer == household
    assert smart_meter.usage_data == 0

def test_measure_usage():
    """
    Test the measurement of electricity usage by the SmartMeter class.
    """
    household = Household(name="Household 1")
    smart_meter = SmartMeter(consumer=household)
    
    input_power = 10000  # 10 kW input power
    household.consume(input_power)
    
    measured_usage = smart_meter.measure_usage()
    
    assert measured_usage == household.consumed_power
    assert smart_meter.usage_data == measured_usage

def test_send_data():
    """
    Test the sending of electricity usage data by the SmartMeter class.
    """
    household = Household(name="Household 1")
    smart_meter = SmartMeter(consumer=household)
    
    input_power = 10000  # 10 kW input power
    household.consume(input_power)
    smart_meter.measure_usage()
    
    sent_data = smart_meter.send_data()
    
    assert sent_data == smart_meter.usage_data
