from pyaspg.prosume.prosumer import Prosumer

class Household(Prosumer):
    """
    Class representing a household prosumer.
    """
    def __init__(self, name, storage_capacity=0):
        super().__init__(name, storage_capacity)
