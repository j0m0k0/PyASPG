import pytest
from pyaspg.generation.generator import Generator
from pyaspg.generation.power_plant import PowerPlant
from pyaspg.generation.solar_panel import SolarPanel
from pyaspg.generation.wind_turbine import WindTurbine

@pytest.mark.parametrize("generator_class, generator_args, generate_args", [
    (PowerPlant, {"name": "Coal Plant", "nominal_capacity": 500000000, "voltage": 25000, "fuel_capacity": 10000, "consumption_rate": 50}, {}),
    (SolarPanel, {"name": "Solar Panel", "nominal_capacity": 100000000, "voltage": 25000}, {"sunlight": 0.8}),
    (WindTurbine, {"name": "Wind Turbine", "nominal_capacity": 200000000, "voltage": 25000}, {"wind_speed": 0.5}),
])
def test_exceeding_nominal_capacity(generator_class, generator_args, generate_args):
    """
    Test to ensure that the generated power does not exceed the nominal capacity of the generators.

    Args:
        generator_class (class): The class of the generator to test.
        generator_args (dict): The arguments to initialize the generator.
        generate_args (dict): The arguments to pass to the generate method.
    """
    generator = generator_class(**generator_args)
    
    if generator_class == PowerPlant:
        generator.generate()
    elif generator_class == SolarPanel:
        generator.generate(**generate_args)
    elif generator_class == WindTurbine:
        generator.generate(**generate_args)

    assert generator.output <= generator.nominal_capacity, f"{generator.name} exceeded its nominal capacity"

def test_solar_panel_zero_output_no_sunlight():
    """
    Test to ensure that the SolarPanel generates zero power when there is no sunlight.
    """
    solar_panel = SolarPanel(name="Solar Panel", nominal_capacity=100000000, voltage=25000)
    solar_panel.generate(sunlight=0)
    
    assert solar_panel.output == 0, "Solar Panel generated power with no sunlight"

def test_wind_turbine_zero_output_no_wind():
    """
    Test to ensure that the WindTurbine generates zero power when there is no wind.
    """
    wind_turbine = WindTurbine(name="Wind Turbine", nominal_capacity=200000000, voltage=25000)
    wind_turbine.generate(wind_speed=0)
    
    assert wind_turbine.output == 0, "Wind Turbine generated power with no wind"

if __name__ == "__main__":
    pytest.main()
