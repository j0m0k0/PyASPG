# utility_to_control_handler.py
from pyaspg.simulation.connection_handler import BaseHandler
from pyaspg.utils import log_me

@log_me
class UtilityToControlHandler(BaseHandler):
    def handle_connection(self, source, target, params, timestep, replay_mode, attacked):
        """
        Handle the connection between a utility company and a control system.

        Args:
            source (UtilityCompany): The source utility company.
            target (ControlSystem): The target control system.
            params (dict): Additional parameters for the connection.
            timestep (int): The current timestep in the simulation.
        """
        # print(f"UtilityToControlHandler--> {source.received_data=}")
        # if not replay_mode:
        data = {
            'timestep': timestep,            
            'total_consumption': sum(d['total_consumption'] for d in source.received_data),
            'total_production': sum(d['total_production'] for d in source.received_data),
            'total_stored_energy': sum(d['total_stored_energy'] for d in source.received_data),
            'total_net_power': sum(d['total_net_power'] for d in source.received_data),
            'utility_name': source.name
        }

        target.receive_data(data)
        # else:
            # target.replay_receive_data(timestep)
