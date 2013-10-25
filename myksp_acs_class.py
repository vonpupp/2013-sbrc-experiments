import json
import lib.tracegen.tracegen as tracegen
import lib.inspyredksp.kspmultirestr as myksp
from itertools import islice
from random import Random
from time import time
import math
import inspyred

def jformat(json_data):
    return json.dumps(json_data, sort_keys=True,
                      indent=4, separators=(',', ': '))

items = []
constraints = None
hosts = 10

def gen_vms():
    global items
    tg = tracegen.TraceGenerator()
    trace = tg.gen_trace()
    items = [(i, {
                  'name': 'item %d' % i,
                  'weight': 1,
                  'cpu': t[0],
                  'mem': t[1],
                  'disk': t[2],
                  'net': t[3],
                  'n': 1
             }) for i,t in islice(enumerate(trace), 288)]

def add_constraint(values, constraint):
    return values[constraint] < 99
  
def add_constraints(values, constraint_list):
    return [add_constraint(values, constraint) for constraint in constraint_list]

def gen_costraints(constraint_list):
    global constraints
    constraints = lambda values: (add_constraints(values, constraint_list))

# ---

def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    gen_vms()

    problem = myksp.Knapsack(100, items, duplicates=False)
    ac = inspyred.swarm.ACS(prng, problem.components)
    ac.terminator = inspyred.ec.terminators.generation_termination
    final_pop = ac.evolve(problem.constructor,
                          problem.evaluator,
                          maximize=problem.maximize,
                          pop_size=50,
                          max_generations=50,
                         )

    if display:
        best = max(ac.archive)
        print('Best Solution: {0}: {1}'.format(str(best.candidate),
                                               best.fitness))
    return ac

if __name__ == '__main__':
    main(display=True)
