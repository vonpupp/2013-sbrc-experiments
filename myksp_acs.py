import json
import lib.tracegen.tracegen as tracegen
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
#                  'weight': 1.5*(cos(i)+1)**2,
                  'weight': 1,
                  'cpu': t[0],
                  'mem': t[1],
                  'disk': t[2],
                  'net': t[3],
                  'n': 1
             }) for i,t in islice(enumerate(trace), 200)]

def add_constraint(values, constraint):
    return values[constraint] < 99
  
def add_constraints(values, constraint_list):
    return [add_constraint(values, constraint) for constraint in constraint_list]

def gen_costraints(constraint_list):
    global constraints
    constraints = lambda values: (add_constraints(values, constraint_list))

# ---

@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    # Check the constraints.
    print('candidate: {}'.format(candidate))
    print('args: {}'.format(args))
#    values = list(candidate)
    #from pudb import set_trace; set_trace()
#    values_sum = sum([trail.value for trail in candidate])
#    print('values_sum: {}'.format(values_sum))
#    return values_sum
    return 100
    #constraint_bounds = [-2, -4]
    #constraint_coefficients = [[-3, -3, 1, 2, 3], [-5, -3, -2, -1, 1]]
    #constraints = [sum([c * v for c, v in zip(coeff, candidate)]) for coeff in constraint_coefficients]
    #print constraints
    #failed_constraints = 0
    #for constraint, bound in zip(constraints, constraint_bounds):
        #if constraint > bound:
            #failed_constraints += 1

    ## Now calculate the fitness. Depending on the computational time,
    ## failed constraints may cause us to just skip this part.
    #coefficients = [8, 2, 4, 7, 5]
    #fitness = 0
    #for c, v in zip(coefficients, candidate):
        #fitness += c * v

    ## Now, punish the candidate for any failed constraints. For the current
    ## problem, the largest (i.e., worst) value for any candidate is 26, so
    ## we'll make sure that our constraint penalty is larger than that.
    ## (We'll make it an order of magnitude larger at 100.)
    #return failed_constraints * 100 + fitness


def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    gen_vms()
#    items = [(7,369), (10,346), (11,322), (10,347), (12,348), (13,383),
#             (8,347), (11,364), (8,340), (8,324), (13,365), (12,314),
#             (13,306), (13,394), (7,326), (11,310), (9,400), (13,339),
#             (5,381), (14,353), (6,383), (9,317), (6,349), (11,396),
#             (14,353), (9,322), (5,329), (5,386), (5,382), (4,369),
#             (6,304), (10,392), (8,390), (8,307), (10,318), (13,359),
#             (9,378), (8,376), (11,330), (9,331)]

    problem = inspyred.benchmarks.Knapsack(15, items, duplicates=False)
    ac = inspyred.swarm.ACS(prng, problem.components)
    ac.terminator = inspyred.ec.terminators.generation_termination
    final_pop = ac.evolve(problem.constructor,
#                          problem.evaluator,
                          evaluator=my_evaluator,
                          maximize=problem.maximize,
#                          maximize=False,
                          pop_size=50,
                          max_generations=50,
                         )

#final_pop = optimizer.evolve(generator=my_generator,
#                             evaluator=my_evaluator,
#                             pop_size=2,
#                             maximize=False,
#                             bounder=inspyred.ec.DiscreteBounder([0, 1]),
#                             max_evaluations=10,
#                             tournament_size=2,
#                             mutation_rate=0.1,
#                             num_elites=1,
#                             num_inputs=5)

    if display:
        best = max(ac.archive)
        print('Best Solution: {0}: {1}'.format(str(best.candidate),
                                               best.fitness))
	# Best Solution: [(5, 386), (6, 383), (4, 369)]: 1138
    return ac

if __name__ == '__main__':
    main(display=True)
