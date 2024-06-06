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
        # Generate power consumption and production, updating the net power
        target.generate_consumption()
        print(f"{target.net_power=}")
        target.generate_production()
        # target.produce(10000)
        print(f"{target.net_power=}")
        
        # Determine how much power the prosumer needs
        power_needed = target.net_power
        
        # If power is still needed after using stored energy, pull from the distributor
        if power_needed > 0:
            print("Power Needed")
            available_power = source.distribute()
            power_to_receive = min(power_needed, available_power)
            print(f"{power_to_receive=}")
            target.receive(power_to_receive)
            target.received_power = power_to_receive  # Track received power
            print(f"{target.net_power=}")
        else:
            print("Not Needed")
            target.received_power = 0  # No power received from distributor
        print("#"*50)
