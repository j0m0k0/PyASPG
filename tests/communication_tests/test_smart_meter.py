import pytest
from pyaspg.prosume import Prosumer
from pyaspg.communication import SmartMeter, CommunicationNetwork

@pytest.fixture
def household():
    return Prosumer(name="Household 1", consumption_file="consumption_patterns/2006-12-16.csv", storage_capacity=5000, prosumer_type="House")

@pytest.fixture
def communication_network():
    return CommunicationNetwork(name="Smart Grid Network", reliability=0.99)

@pytest.fixture
def smart_meter(household, communication_network):
    return SmartMeter(prosumer=household, communication_network=communication_network)

def test_smart_meter_initialization(household, communication_network):
    """
    Test the initialization of the SmartMeter class.
    """
    smart_meter = SmartMeter(prosumer=household, communication_network=communication_network)
    
    assert smart_meter.prosumer == household
    assert smart_meter.communication_network == communication_network
    assert smart_meter.data == {}

def test_measure(household, smart_meter):
    """
    Test the measurement of electricity usage, production, and net power by the SmartMeter class.
    """
    household.generate_consumption()  # Generate consumption
    household.generate_production()  # Generate production
    
    measured_data = smart_meter.measure()
    
    assert measured_data["usage"] == household.total_consumption
    assert measured_data["production"] == household.total_production
    assert measured_data["net_power"] == household.net_power
    assert measured_data["stored_energy"] == household.stored_energy

def test_send_data(household, smart_meter):
    """
    Test the sending of electricity usage, production, and net power data by the SmartMeter class.
    """
    household.generate_consumption()  # Generate consumption
    household.generate_production()  # Generate production
    
    smart_meter.measure()
    
    success = smart_meter.send_data()
    
    # Check if data transmission was successful
    assert success == True

    # Verify that the data was actually sent to the communication network
    data_packet = {
        "prosumer_name": household.name,
        "usage": household.total_consumption,
        "production": household.total_production,
        "net_power": household.net_power,
        "stored_energy": household.stored_energy
    }
    assert data_packet in smart_meter.communication_network.transmitted_data

if __name__ == "__main__":
    pytest.main()
