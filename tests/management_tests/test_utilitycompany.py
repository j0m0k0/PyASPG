import pytest
from pyaspg.management.utility_company import UtilityCompany

@pytest.fixture
def utility_company():
    return UtilityCompany(name="Utility Company 1")

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
    utility_company.receive_data(data_packet)
    
    assert len(utility_company.received_data) == 1
    assert utility_company.received_data[0] == data_packet

if __name__ == "__main__":
    pytest.main()
