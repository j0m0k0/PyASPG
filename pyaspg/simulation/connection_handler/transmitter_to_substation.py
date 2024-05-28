from pyaspg.simulation.connection_handler import BaseHandler

class TransmitterToSubstationHandler(BaseHandler):
    def handle_connection(self, source, target, parameters, timestep):
        output_power = source.output_power
        target.receive(output_power)
