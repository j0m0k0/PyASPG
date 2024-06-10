from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me

@log_me
class DistributorToProsumerHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep):
        """
        Handle the connection between a distributor and a prosumer.

        Args:
            source (Distributor): The source distributor.
            target (Prosumer): The target prosumer.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """
        # Generate power consumption, production and update the net
        # print("\nNew timestep", "#"*50)
        random_consumption = target.generate_consumption()
        # print("Net power after consumption:", target.net_power)
        random_generation = target.generate_production()
        # Determine how much power the prosumer needs
        power_needed = target.net_power
        # print("Net power after generation:", target.net_power)
        # Prosumer first uses stored energy
        # target.consume(power_needed)

        # Any remaining power needed is pulled from the distributor
        remaining_power_needed = target.net_power
        if remaining_power_needed > 0 and source.available_power > 0:
            power_to_receive = min(remaining_power_needed, source.available_power)
            # print("Available power", available_power)
            # print("Power to receive", power_to_receive)
            target.receive(power_to_receive, source.name)
            source.available_power -= power_to_receive 
            target.received_power = power_to_receive  # Track received power
        else:
            target.received_power = 0  # No power received from distributor
            target.distributor_name = ""
        
        # print("Final net power at this timestep:", target.net_power)
