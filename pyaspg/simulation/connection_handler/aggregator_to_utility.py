from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me

@log_me
class AggregatorToUtilityHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep):
        """
        Handle the connection between a net aggregator and a utility company.

        Args:
            source (NetAggregator): The source net aggregator.
            target (UtilityCompany): The target utility company.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """
        # Aggregate the data collected by the aggregator
        source.aggregate_data()

        # Send the aggregated data to the utility company
        source.send_data_to_utility(target)
