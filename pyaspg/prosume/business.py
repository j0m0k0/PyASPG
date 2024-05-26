from pyaspg.prosume.prosumer import Prosumer

class Business(Prosumer):
    """
    Class representing a business prosumer.
    """
    def __init__(self, name, storage_capacity=0):
        super().__init__(name, storage_capacity)
