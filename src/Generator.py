class Generator:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity  # in MW
        self.output = 0  # Current output in MW

    def generate_power(self, demand):
        self.output = min(self.capacity, demand)
        return self.output