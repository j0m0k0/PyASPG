# Created 2002
# Environment in simpy: Event loop
# Process : Task
# Event: Promise / Future
# Resource: Semaphore

# Core idea is to use python generators
# Simpy has two environments: Environment and RealtimeEnvironment
# Environment: As fast as possible
# RealtimeEnvironment: Synchrnoized with wall-clock time
# Also you can create other costum environments if you want

# Simpy events
# env.timeout : let time pass

# Simpy processes
# are events too
# processes can also be interrupted: .interrupt(...)
# condition events: Wait for eventA or eventB or ... using or, and operators

# Simpy has 3 types of resources defined
# Shared Resources
# There is a queue that manages a resource

# Priority resources (preemptive)
# Important processes can kick a resource out of another resource 

# Container: Stores continuous amount of something (e.g., water)

 # simpy.io : event-driven networking library, useful for simulating communications over TCP

 # simpy has no external dependency
 
import simpy

def clock(env, name, tick):
    while True:
        yield env.timeout(tick)

env = simpy.Environment()
env.process(clock(env, 'fast', 0.5))
env.process(clock(env, 'slow', 1))

env.run(until=2)
