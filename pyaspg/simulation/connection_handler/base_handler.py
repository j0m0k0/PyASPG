from abc import ABC, abstractmethod


class BaseHandler(ABC):
    def __init__(self, relation_type='one-to-one'):
        self.relation_type = relation_type

    @abstractmethod
    def handle_connection(self, source, target, parameters, timestep):
        pass
