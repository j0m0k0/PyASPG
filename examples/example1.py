from .src import Consumer, Generator, UtilityCompany



# Example usage
g1 = Generator("Generator 1", 100)
consumer1 = Consumer("Consumer 1", 50)
consumer2 = Consumer("Consumer 2", 30)

utility = UtilityCompany("Utility 1")
utility.add_generator(g1)
utility.add_consumer(consumer1)
utility.add_consumer(consumer2)

utility.distribute_power()
utility.report()