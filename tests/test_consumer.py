import pytest
from consumer import Consumer, Household, Business, Industry

def test_consumer_initialization():
    """
    Test the initialization of the Consumer class.
    """
    consumer = Consumer(name="Generic Consumer", consumption_rate=5000)
    
    assert consumer.name == "Generic Consumer"
    assert consumer.consumption_rate == 5000
    assert consumer.input_power == 0
    assert consumer.consumed_power == 0

def test_consumer_consumption():
    """
    Test the consumption of power by the Consumer class.
    """
    consumer = Consumer(name="Generic Consumer", consumption_rate=5000)
    input_power = 10000  # 10 kW input power
    expected_consumed_power = consumer.consumption_rate
    
    consumed_power = consumer.consume(input_power)
    
    assert consumed_power == expected_consumed_power
    assert consumer.input_power == input_power
    assert consumer.consumed_power == consumed_power

def test_consumer_consumption_bounds():
    """
    Test that the consumed power does not exceed the consumption rate.
    """
    consumer = Consumer(name="Generic Consumer", consumption_rate=5000)
    input_power = 4000  # 4 kW input power
    
    consumed_power = consumer.consume(input_power)
    
    assert consumed_power == input_power
    assert consumer.input_power == input_power
    assert consumer.consumed_power == consumed_power

def test_household_initialization():
    """
    Test the initialization of the Household class.
    """
    household = Household(name="Household 1")
    
    assert household.name == "Household 1"
    assert household.consumption_rate == 5000
    assert household.input_power == 0
    assert household.consumed_power == 0

def test_business_initialization():
    """
    Test the initialization of the Business class.
    """
    business = Business(name="Business 1")
    
    assert business.name == "Business 1"
    assert business.consumption_rate == 20000
    assert business.input_power == 0
    assert business.consumed_power == 0

def test_industry_initialization():
    """
    Test the initialization of the Industry class.
    """
    industry = Industry(name="Industry 1")
    
    assert industry.name == "Industry 1"
    assert industry.consumption_rate == 100000
    assert industry.input_power == 0
    assert industry.consumed_power == 0