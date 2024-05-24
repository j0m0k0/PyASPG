import pytest
from CommunicationNetwork import CommunicationNetwork

def test_communication_network_initialization():
    """
    Test the initialization of the CommunicationNetwork class.
    """
    network = CommunicationNetwork(name="Smart Grid Network", reliability=0.99)
    
    assert network.name == "Smart Grid Network"
    assert network.reliability == 0.99
    assert network.transmitted_data == []
    assert network.received_data == []

def test_transmit_data():
    """
    Test the transmission of data by the CommunicationNetwork class.
    """
    network = CommunicationNetwork(name="Smart Grid Network", reliability=0.99)
    data_packet = {"meter_id": 1, "usage": 500}
    
    success = network.transmit_data(data_packet)
    
    if success:
        assert data_packet in network.transmitted_data
    else:
        assert data_packet not in network.transmitted_data

def test_receive_data():
    """
    Test the reception of data by the CommunicationNetwork class.
    """
    network = CommunicationNetwork(name="Smart Grid Network", reliability=0.99)
    data_packet = {"meter_id": 1, "usage": 500}
    
    success = network.receive_data(data_packet)
    
    if success:
        assert data_packet in network.received_data
    else:
        assert data_packet not in network.received_data

def test_reliability_bounds():
    """
    Test that the reliability is within the valid range (0 to 1).
    """
    with pytest.raises(ValueError):
        CommunicationNetwork(name="Invalid Reliability", reliability=1.1)
    
    with pytest.raises(ValueError):
        CommunicationNetwork(name="Invalid Reliability", reliability=-0.1)
