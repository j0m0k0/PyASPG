import pytest
from pyaspg.management import NetAggregator, UtilityCompany
from pyaspg.communication import SmartMeter, CommunicationNetwork
from pyaspg.prosume import Prosumer

@pytest.fixture
def net_aggregator():
    return NetAggregator(name="Data Aggregator 1")

@pytest.fixture
def household():
    return Prosumer(name="Household 1", consumption_file="consumption_patterns/2006-12-16.csv", storage_capacity=5000, prosumer_type="House")

@pytest.fixture
def communication_network():
    return CommunicationNetwork(name="Smart Grid Network", reliability=0.99)

@pytest.fixture
def smart_meter(household, communication_network):
    return SmartMeter(prosumer=household, communication_network=communication_network)

def test_net_aggregator_initialization(net_aggregator):
    """
    Test the initialization of the NetAggregator class.
    """
    assert net_aggregator.name == "Data Aggregator 1"
    assert net_aggregator.data_collected == []
    assert net_aggregator.utility_data == {}
    assert net_aggregator.commands == {}

def test_collect_data(net_aggregator, smart_meter):
    """
    Test collecting data from a smart meter in the NetAggregator class.
    """
    smart_meter.prosumer.generate_consumption()
    smart_meter.prosumer.generate_production()
    
    success = net_aggregator.collect_data(smart_meter)
    assert success is True
    assert len(net_aggregator.data_collected) == 1

def test_aggregate_data(net_aggregator, smart_meter):
    """
    Test aggregating data in the NetAggregator class.
    """
    smart_meter.prosumer.generate_consumption()
    smart_meter.prosumer.generate_production()
    
    net_aggregator.collect_data(smart_meter)
    net_aggregator.aggregate_data()
    
    assert net_aggregator.utility_data["total_usage"] == smart_meter.prosumer.total_consumption
    assert net_aggregator.utility_data["total_production"] == smart_meter.prosumer.total_production
    assert net_aggregator.utility_data["total_stored_energy"] == smart_meter.prosumer.stored_energy

def test_send_data_to_utility(net_aggregator, smart_meter):
    """
    Test sending aggregated data to a utility company in the NetAggregator class.
    """
    class MockUtilityCompany(UtilityCompany):
        def __init__(self, name):
            super().__init__(name)
            self.received_data = []

        def receive_data(self, data):
            self.received_data.append(data)

    utility_company = MockUtilityCompany(name="Utility Company 1")
    
    smart_meter.prosumer.generate_consumption()
    smart_meter.prosumer.generate_production()
    
    net_aggregator.collect_data(smart_meter)
    net_aggregator.aggregate_data()
    net_aggregator.send_data_to_utility(utility_company)
    
    assert len(utility_company.received_data) == 1
    assert utility_company.received_data[0] == net_aggregator.utility_data

def test_send_command(net_aggregator, household):
    """
    Test sending a command to a prosumer in the NetAggregator class.
    """
    command = "Reduce consumption by 500 W"
    net_aggregator.send_command(household, command)
    
    assert command in household.received_commands

if __name__ == "__main__":
    pytest.main()
