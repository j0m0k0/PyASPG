import pytest
from pyaspg.prosume.prosumer import Prosumer

@pytest.fixture
def prosumer():
    return Prosumer(name="Test Prosumer", storage_capacity=5000)

def test_prosumer_initialization(prosumer):
    """
    Test the initialization of the Prosumer class.
    """
    assert prosumer.name == "Test Prosumer"
    assert prosumer.total_consumption == 0
    assert prosumer.total_production == 0
    assert prosumer.storage_capacity == 5000
    assert prosumer.stored_energy == 0
    assert prosumer.net_power == 0
    assert prosumer.received_commands == []

def test_prosumer_net_power(prosumer):
    """
    Test the net power calculation of the Prosumer class.
    """
    prosumer.consume(10000)
    assert prosumer.total_consumption == 10000
    assert prosumer.net_power == 10000  # Needs 10000 W from the grid

    prosumer.produce(12000)
    assert prosumer.total_production == 12000
    assert prosumer.stored_energy == 2000  # Stores 2000 W
    assert prosumer.net_power == 0  # No net power needed from the grid

    prosumer.consume(1000)
    assert prosumer.net_power == 0  # Uses 1000 W from storage
    assert prosumer.stored_energy == 1000  # Stored energy decreases to 1000 W

    prosumer.consume(4000)
    assert prosumer.net_power == 3000  # Needs 3000 W from the grid
    assert prosumer.stored_energy == 0  # Stored energy depletes to 0

    prosumer.produce(3000)
    assert prosumer.net_power == 0  # No net power needed from the grid

    prosumer.produce(2000)
    assert prosumer.net_power == 0  # Sends 2000 W to the grid

def test_prosumer_storage(prosumer):
    """
    Test the storage behavior of the Prosumer class.
    """
    prosumer.produce(6000)
    assert prosumer.stored_energy == 5000  # Storage should be capped at 5000 W
    assert prosumer.net_power == -1000  # Should export 1000 W to the grid

    prosumer.consume(2000)
    assert prosumer.stored_energy == 3000  # Should use 2000 W from storage
    assert prosumer.net_power == -1000  # Should still export 1000 W to the grid

    prosumer.consume(6000)
    assert prosumer.stored_energy == 0  # Should deplete storage
    assert prosumer.net_power == 2000  # Should draw 3000 W from the grid

def test_prosumer_receive_command(prosumer):
    """
    Test receiving commands from the aggregator.
    """
    command = "Reduce consumption by 500 W"
    prosumer.receive_command(command)
    assert command in prosumer.received_commands

def test_prosumer_produce_consume_sequence(prosumer):
    """
    Test a sequence of production and consumption to ensure the net power and storage are updated correctly.
    """
    prosumer.produce(5000)
    assert prosumer.net_power == 0  # Sends 5000 W to the grid

    prosumer.consume(2000)
    assert prosumer.net_power == 0  # Reduces grid export to 3000 W
    assert prosumer.stored_energy == 3000  # Stored energy remains 0

    prosumer.produce(2000)
    assert prosumer.net_power == 0  # Sends 5000 W to the grid again

    prosumer.consume(7000)
    assert prosumer.net_power == 2000  # Needs 2000 W from the grid
    assert prosumer.stored_energy == 0  # Stored energy remains 0

