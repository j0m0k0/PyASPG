from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.generation import WindTurbine, SolarPanel, PowerPlant
from pyaspg.utils import log_me


@log_me
class GeneratorToTransmitterHandler(BaseHandler):
    """
        Handler for Generator to Transmitter Connections
    """
    def __init__(self):
        super().__init__()

        self.transmitter_groups = {}
    def handle_connection(self, source, target, params, timestep):
        print("Handler called for", source.name)
    
        print(self.transmitter_groups)
        if isinstance(source, WindTurbine):
            output_power = source.generate()
        elif isinstance(source, SolarPanel):
            sunlight = params.get('sunlight', [])[timestep]
            output_power = source.generate(sunlight)
        elif isinstance(source, PowerPlant):
            output_power = source.generate()
        
        target.receive(output_power, timestep)

