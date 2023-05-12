import random
import simpy
from collections import defaultdict

RANDOM_SEED = 123
TOTAL_CUSTOMERS = 10
INTERARRIVAL_MEAN = 10 # time is unitless in simpy, but lets say its minutes
MIN_WAIT = 1
MAX_WAIT = 3

#create
def create_arrivals(env, customers, interarrival, server):
    for i in range(customers):
        c = entity(env, f'arrival {i+1}', server, serve_time=12)
        env.process(c)
        inter_time = random.expovariate(1.0/interarrival)
        yield env.timeout(inter_time)

def entity(env, name, server, serve_time):
    arrival = env.now
    print(f'{name} at {round(arrival, 2)}')

    with server.request() as serve:
        done_waiting = random.triangular(low=MIN_WAIT, high=MAX_WAIT)
        # wait for server or renege
        res = yield serve | env.timeout(done_waiting)
        wait = env.now - arrival

        if serve in res:
            print(f'{round(env.now, 2)}: {name} waited {round(wait, 2)}')
            processing_time = random.expovariate(1/serve_time)
            yield env.timeout(processing_time)
            print(f'{round(env.now, 2)}: {name} finished')
        else:
            print(f'{round(env.now, 2)}: {name} reneged after {round(wait, 2)}')

#process
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
server = simpy.Resource(env, capacity=1)
env.process(create_arrivals(env, TOTAL_CUSTOMERS, INTERARRIVAL_MEAN, server))
env.run()


