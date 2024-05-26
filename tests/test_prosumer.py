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
    assert prosumer.consumption == 0
    assert prosumer.production == 0
    assert prosumer.storage_capacity == 5000
    assert prosumer.stored_energy == 0

def test_prosumer_consumption(prosumer):
    """
    Test the consumption of electricity by the Prosumer class.
    """
    prosumer.consume(1000)
    assert prosumer.consumption == 1000

def test_prosumer_production(prosumer):
    """
    Test the production of electricity by the Prosumer class.
    """
    prosumer.produce(2000)
    assert prosumer.production == 2000

def test_prosumer_storage(prosumer):
    """
    Test the storage of electricity by the Prosumer class.
    """
    stored = prosumer.store_energy(3000)
    assert stored == 3000
    assert prosumer.stored_energy == 3000
    stored = prosumer.store_energy(3000)
    assert stored == 2000
    assert prosumer.stored_energy == 5000

def test_prosumer_use_stored_energy(prosumer):
    """
    Test the usage of stored electricity by the Prosumer class.
    """
    prosumer.store_energy(3000)
    used = prosumer.use_stored_energy(1000)
    assert used == 1000
    assert prosumer.stored_energy == 2000

def test_prosumer_net_power(prosumer):
    """
    Test the net power calculation of the Prosumer class.
    """
    prosumer.consume(10000)
    prosumer.produce(8000)
    net = prosumer.net_power()
    assert net == 2000  # Should draw 2000 W from the grid

    prosumer.produce(3000)
    net = prosumer.net_power()
    assert net == 0  # Should store 1000 W in the storage instead of sending to the grid

    # Consume some power to use stored energy
    prosumer.consume(1000)
    net = prosumer.net_power()
    assert net == 0  # Should use 1000 W from storage, resulting in net 0

    # Consume additional power to test sending power to the grid
    prosumer.consume(4000)
    net = prosumer.net_power()
    assert net == 3000  # Should draw 3000 W from the grid since 2000 W was stored

if __name__ == "__main__":
    pytest.main()
