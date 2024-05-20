class Consumer:
    def __init__(self, name, demand):
        self.name = name
        self.demand = demand  # in MW
        self.consumption = 0  # Current consumption in MW

    def consume_power(self, supply):
        self.consumption = min(self.demand, supply)
        return self.consumption