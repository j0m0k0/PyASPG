import pytest
from pyaspg.management.control_system import ControlSystem
from pyaspg.management.net_aggregator import NetAggregator

@pytest.fixture
def control_system():
    return ControlSystem(name="Control System 1")

@pytest.fixture
def net_aggregator():
    return NetAggregator(name="Data Aggregator 1")

def test_control_system_initialization(control_system):
    """
    Test the initialization of the ControlSystem class.
    """
    assert control_system.name == "Control System 1"
    assert control_system.grid_data == {
        "generation": {},
        "transmission": {},
        "distribution": {},
        "consumption": {}
    }

def test_update_grid_data(control_system):
    """
    Test updating grid data in the ControlSystem class.
    """
    generation_data = {"Plant 1": 5000, "Plant 2": 7000}
    control_system.update_grid_data("generation", generation_data)
    assert control_system.grid_data["generation"] == generation_data

def test_analyze_grid(control_system):
    """
    Test analyzing grid data in the ControlSystem class.
    """
    control_system.update_grid_data("generation", {"Plant 1": 5000, "Plant 2": 7000})
    control_system.update_grid_data("consumption", {"Household 1": 2000, "Business 1": 3000})
    
    commands = control_system.analyze_grid()
    
    assert commands["load_balancing"] == "Reduce generation"
    assert commands["demand_response"] is None
    assert commands["stability"] is None

def test_issue_commands(control_system, net_aggregator):
    """
    Test issuing commands from the ControlSystem class to the NetAggregator class.
    """
    control_system.update_grid_data("generation", {"Plant 1": 5000, "Plant 2": 7000})
    control_system.update_grid_data("consumption", {"Household 1": 2000, "Business 1": 3000})
    
    commands = control_system.analyze_grid()
    control_system.issue_commands(net_aggregator, commands)
    
    assert net_aggregator.commands["load_balancing"] == ["Reduce generation"]
