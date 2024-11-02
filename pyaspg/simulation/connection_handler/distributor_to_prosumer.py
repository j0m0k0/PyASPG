from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me

@log_me
class DistributorToProsumerHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep, replay_mode, attacked):
        """
        Handle the connection between a distributor and a prosumer.

        Args:
            source (Distributor): The source distributor.
            target (Prosumer): The target prosumer.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """

        if replay_mode:
            # Generate power consumption, production and update the net
            random_consumption = target.replay_generate_consumption(timestep)
            random_generation = target.replay_generate_production(timestep)
            
            # Determine how much power the prosumer needs
            power_needed = target.net_power
            # Prosumer first uses stored energy
            # target.consume(power_needed)

            # Any remaining power needed is pulled from the distributor
            remaining_power_needed = target.net_power
            if remaining_power_needed > 0 and source.available_power > 0:                
                power_to_receive = min(remaining_power_needed, source.available_power)
                target.receive(power_to_receive, source.name)
                source.available_power -= power_to_receive 
                target.received_power = power_to_receive  # Track received power
            else:
                if source.available_power == 0:
                    # target._net_power = 0
                    
                    # Even there is no power available, we still send a receive 
                    # signal with zero power to the prosumer this makes the
                    #  prosumer to log what was net_power_before, if we don't do 
                    # this, the net_power_before won't be logged for prosumers 
                    # that don't receive any power.
                    target.receive(0, source.name)
                target.received_power = 0  # No power received from distributor
                # target.distributor_name = ""
        else:
            # Generate power consumption, production and update the net
            random_consumption = target.generate_consumption()
            random_generation = target.generate_production()
            # Determine how much power the prosumer needs
            power_needed = target.net_power
            # Prosumer first uses stored energy
            # target.consume(power_needed)

            # Any remaining power needed is pulled from the distributor
            remaining_power_needed = target.net_power
            if remaining_power_needed > 0 and source.available_power > 0:
                print("IF CASE")
                print(f"Source name {source.name} available power {source.available_power}")
                print(f"Target name {target.name} net power {target.net_power}")
                print("-"*50)
                power_to_receive = min(remaining_power_needed, source.available_power)
                target.receive(power_to_receive, source.name)
                source.available_power -= power_to_receive 
                target.received_power = power_to_receive  # Track received power
            else:
                print("ELSE CASE")
                print(f"Source name {source.name} available power {source.available_power}")
                print(f"Target name {target.name} net power {target.net_power}")
                print("-"*50)
                if source.available_power == 0:
                    # target._net_power = 0
                    
                    # Even there is no power available, we still send a receive 
                    # signal with zero power to the prosumer this makes the
                    #  prosumer to log what was net_power_before, if we don't do 
                    # this, the net_power_before won't be logged for prosumers 
                    # that don't receive any power.
                    target.receive(0, source.name)
                target.received_power = 0  # No power received from distributor
                # target.distributor_name = ""
