from abc import ABC, abstractmethod

# In a smart power grid, the connection types between components can be classified as follows:

# Generator to Transmitter: Typically, this is a Many-to-One relationship. Multiple generators (power plants) may connect to a transmission network, which channels the electricity over long distances.

# Transmitter to Substation: Many-to-One. The transmission network connects to various substations, which reduce the high transmission voltages to lower levels suitable for distribution.

# Substation to Distributor: One-to-Many. A substation feeds several distribution lines that deliver electricity to different geographical areas.

# Distributor to Prosumer: Many-to-Many. Distributors connect to multiple prosumers (consumers who also produce energy), and vice versa, especially in scenarios where prosumers can feed surplus energy back into the grid.

# Prosumer to Smart Meter: One-to-One. Each prosumer typically has a dedicated smart meter that monitors and manages electricity use and generation.

# Smart Meter to Aggregator: Many-to-One. Multiple smart meters (from various prosumers) connect to an aggregator that compiles and analyzes data from many sources to manage demand, supply, and pricing more efficiently.

# Aggregator to Utility: One-to-One or Many-to-One, depending on the structure. An aggregator can feed data directly to a single utility or multiple utilities, facilitating broader grid management and decision-making.

# Utility to Control Center: One-to-One. The utility company connects to a control center, which uses the data from utilities to monitor, control, and optimize the operation of the entire power grid.


class BaseHandler(ABC):
    def __init__(self, relation_type='one-to-one'):
        self.relation_type = relation_type

    @abstractmethod
    def handle_connection(self, source, target, parameters, timestep, replay_mode):
        pass
