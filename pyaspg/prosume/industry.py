from pyaspg.prosume.prosumer import Prosumer

class Industry(Prosumer):
    """
    Class representing an industrial prosumer.
    """
    def __init__(self, name, storage_capacity=0):
        super().__init__(name, storage_capacity)
