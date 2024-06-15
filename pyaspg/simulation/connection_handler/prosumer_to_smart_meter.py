from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me

@log_me
class ProsumerToSmartMeterHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep):
        """
        Handle the connection between a prosumer and a smart meter.

        Args:
            source (Prosumer): The source prosumer.
            target (SmartMeter): The target smart meter.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """
        # Measure the prosumer's electricity usage, production, and net power
        measured_data = target.measure()
        
        # Simulate sending the data to the communication network
        success = target.send_data()
        
        # if success:
        #     print(f"Data successfully transmitted from {source.name} at timestep {timestep}.")
        # else:
        #     print(f"Data transmission failed for {source.name} at timestep {timestep}.")
