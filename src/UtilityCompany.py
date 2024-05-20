class UtilityCompany:
    def __init__(self, name):
        self.name = name
        self.generators = []
        self.consumers = []

    def add_generator(self, generator):
        self.generators.append(generator)

    def add_consumer(self, consumer):
        self.consumers.append(consumer)

    def distribute_power(self):
        total_demand = sum(consumer.demand for consumer in self.consumers)
        total_supply = sum(plant.generate_power(total_demand) for plant in self.generators)
        
        for consumer in self.consumers:
            consumer.consume_power(total_supply / len(self.consumers))

    def report(self):
        print(f"Utility Company: {self.name}")
        for plant in self.generators:
            print(f"  Power Plant: {plant.name}, Output: {plant.output} MW")
        for consumer in self.consumers:
            print(f"  Consumer: {consumer.name}, Consumption: {consumer.consumption} MW")
