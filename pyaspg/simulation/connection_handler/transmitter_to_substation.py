from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me


@log_me
class TransmitterToSubstationHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep):
        """
        Handle the connection between a transmitter and a substation.

        Args:
            source (Transmitter): The source transmitter.
            target (Substation): The target substation.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """
        # Get the input power from the transmitter and pass it to the substation
        input_power = source.transmit()
        target.receive(input_power)
