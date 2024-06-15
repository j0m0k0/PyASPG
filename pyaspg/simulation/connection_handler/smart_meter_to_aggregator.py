from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me

@log_me
class SmartMeterToAggregatorHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep):
        """
        Handle the connection between a smart meter and a net aggregator.

        Args:
            source (SmartMeter): The source smart meter.
            target (NetAggregator): The target net aggregator.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """
        # Collect data from the smart meter and send it to the aggregator
        if source.send_data():
            target.collect_data(source, timestep)
