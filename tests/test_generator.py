import numpy as np
import simpy
import pytest
from Generator import Generator, PowerPlant, SolarPanel, WindTurbine

@pytest.fixture
def env():
    return simpy.Environment()

@pytest.mark.parametrize("generator_class, generator_args", [
    (PowerPlant, {"name": "Coal Plant", "nominal_capacity": 500000000, "voltage": 25000, "fuel_capacity": 10000, "consumption_rate": 50}),
    (SolarPanel, {"name": "Solar Panel", "nominal_capacity": 100000000, "voltage": 25000}),
    (WindTurbine, {"name": "Wind Turbine", "nominal_capacity": 200000000, "voltage": 25000}),
])
def test_exceeding_nominal_capacity(env, generator_class, generator_args):
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

