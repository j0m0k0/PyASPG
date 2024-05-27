import pytest
from pyaspg.management.net_aggregator import NetAggregator
from pyaspg.communication.smart_meter import SmartMeter
from pyaspg.prosume.household import Household
from pyaspg.management.utility_company import UtilityCompany
from pyaspg.communication.communication_network import CommunicationNetwork

@pytest.fixture
def net_aggregator():
    return NetAggregator(name="Data Aggregator 1")

@pytest.fixture
def household():
    return Household(name="Household 1", storage_capacity=5000)

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
    input_power = 10000
    smart_meter.prosumer.consume(input_power)
    smart_meter.prosumer.produce(8000)
    
    success = net_aggregator.collect_data(smart_meter)
    assert success is True
    assert len(net_aggregator.data_collected) == 1

def test_aggregate_data(net_aggregator, smart_meter):
    """
    Test aggregating data in the NetAggregator class.
    """
    input_power = 10000
    smart_meter.prosumer.consume(input_power)
    smart_meter.prosumer.produce(8000)
    
    net_aggregator.collect_data(smart_meter)
    net_aggregator.aggregate_data()
    
    assert net_aggregator.utility_data["total_usage"] == 10000
    assert net_aggregator.utility_data["total_production"] == 8000
    assert net_aggregator.utility_data["total_stored_energy"] == 0

def test_send_data_to_utility(net_aggregator, smart_meter):
    """
    Test sending aggregated data to a utility company in the NetAggregator class.
    """
    class MockUtilityCompany(UtilityCompany):
        def receive_data(self, data):
            self.received_data.append(data)

    utility_company = MockUtilityCompany(name="Utility Company 1")
    
    input_power = 10000
    smart_meter.prosumer.consume(input_power)
    smart_meter.prosumer.produce(8000)
    
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
