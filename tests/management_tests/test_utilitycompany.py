import pytest
from pyaspg import UtilityCompany, WindTurbine

@pytest.fixture
def utility_company():
    wind_turbine = WindTurbine(name='WT1', nominal_capacity=5000, voltage=10000)
    return UtilityCompany(name="Utility Company 1", generators=[wind_turbine])

def test_utility_company_initialization(utility_company):
    """
    Test the initialization of the UtilityCompany class.
    """
    assert utility_company.name == "Utility Company 1"
    assert utility_company.received_data == []

def test_receive_data(utility_company):
    """
    Test receiving aggregated data in the UtilityCompany class.
    """
    data_packet = {
        "total_consumption": 10000,
        "total_production": 8000,
        "total_stored_energy": 2000
    }
    timestep = 1
    utility_company.receive_data(data_packet, timestep)
    
    assert len(utility_company.received_data) == 1
    assert utility_company.received_data[0] == data_packet

if __name__ == "__main__":
    pytest.main()
