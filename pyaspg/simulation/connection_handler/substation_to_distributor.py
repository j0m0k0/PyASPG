from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me

@log_me
class SubstationToDistributorHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep):
        """
        Handle the connection between a substation and a distributor.

        Args:
            source (Substation): The source substation.
            target (Distributor): The target distributor.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """
        # Get the output power from the substation and pass it to the distributor
        output_power = source.transform()
        target.receive(output_power)
