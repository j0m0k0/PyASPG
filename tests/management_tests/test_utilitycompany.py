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
        "total_usage": 10000,
        "total_production": 8000,
        "total_stored_energy": 2000
    }
    utility_company.receive_data(data_packet)
    
    assert len(utility_company.received_data) == 1
    assert utility_company.received_data[0] == data_packet

def test_manage_grid(utility_company):
    """
    Test managing the grid in the UtilityCompany class.
    """
    data_packet_1 = {
        "total_usage": 10000,
        "total_production": 8000,
        "total_stored_energy": 2000
    }
    data_packet_2 = {
        "total_usage": 15000,
        "total_production": 12000,
        "total_stored_energy": 3000
    }
    utility_company.receive_data(data_packet_1)
    utility_company.receive_data(data_packet_2)
    
    utility_company.manage_grid()
    
    assert sum(d['total_usage'] for d in utility_company.received_data) == 25000
    assert sum(d['total_production'] for d in utility_company.received_data) == 20000
    assert sum(d['total_stored_energy'] for d in utility_company.received_data) == 5000
