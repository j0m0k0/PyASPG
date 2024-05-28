from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.generation import WindTurbine, SolarPanel, PowerPlant

# generator_to_transmitter.py
class GeneratorToTransmitterHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep):
        if isinstance(source, WindTurbine):
            wind_speed = params.get('wind_speed', [])[timestep]
            output_power = source.generate(wind_speed)
        elif isinstance(source, SolarPanel):
            sunlight = params.get('sunlight', [])[timestep]
            output_power = source.generate(sunlight)
        elif isinstance(source, PowerPlant):
            output_power = source.generate()
        
        target.transmit(output_power)

