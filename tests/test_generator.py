import simpy
import pytest
from Generator import Generator, PowerPlant, SolarPanel, WindTurbine

@pytest.fixture
def env():
    """
    Fixture to create a SimPy environment for the tests.
    
    Returns:
        simpy.Environment: A new SimPy environment.
    """
    return simpy.Environment()

@pytest.mark.parametrize("generator_class, generator_args", [
    (PowerPlant, {"name": "Coal Plant", "nominal_capacity": 500000000, "voltage": 25000, "fuel_capacity": 10000, "consumption_rate": 50}),
    (SolarPanel, {"name": "Solar Panel", "nominal_capacity": 100000000, "voltage": 25000}),
    (WindTurbine, {"name": "Wind Turbine", "nominal_capacity": 200000000, "voltage": 25000}),
])
def test_exceeding_nominal_capacity(env, generator_class, generator_args):
    """
    Test to ensure that the generated power does not exceed the nominal capacity of the generators.

    Args:
        env (simpy.Environment): The SimPy environment for the test.
        generator_class (class): The class of the generator to test.
        generator_args (dict): The arguments to initialize the generator.
    """
    if generator_class == PowerPlant:
        generator = generator_class(env, **generator_args)
        env.process(generator.generate())
    elif generator_class == SolarPanel:
        generator = generator_class(env, **generator_args)
        env.process(generator.generate(sunlight=0.8))
    elif generator_class == WindTurbine:
        generator = generator_class(env, **generator_args)
        env.process(generator.generate(wind_speed=0.5))

    env.run(until=10)  # Run the simulation for 10 hours

    assert generator.output <= generator.nominal_capacity, f"{generator.name} exceeded its nominal capacity"

def test_solar_panel_zero_output_no_sunlight(env):
    """
    Test to ensure that the SolarPanel generates zero power when there is no sunlight.

    Args:
        env (simpy.Environment): The SimPy environment for the test.
    """
    solar_panel = SolarPanel(env, name="Solar Panel", nominal_capacity=100000000, voltage=25000)
    env.process(solar_panel.generate(sunlight=0))
    env.run(until=1)  # Run the simulation for 1 hour
    
    assert solar_panel.output == 0, "Solar Panel generated power with no sunlight"

def test_wind_turbine_zero_output_no_wind(env):
    """
    Test to ensure that the WindTurbine generates zero power when there is no wind.

    Args:
        env (simpy.Environment): The SimPy environment for the test.
    """
    wind_turbine = WindTurbine(env, name="Wind Turbine", nominal_capacity=200000000, voltage=25000)
    env.process(wind_turbine.generate(wind_speed=0))
    env.run(until=1)  # Run the simulation for 1 hour
    
    assert wind_turbine.output == 0, "Wind Turbine generated power with no wind"
