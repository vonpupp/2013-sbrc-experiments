from random import Random
from time import time
import math
import inspyred


@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    # Check the constraints.
    print('candidate: {}'.format(candidate))
    print('args: {}'.format(args))
    values = list(candidate)
#    from pudb import set_trace; set_trace()
#    print('type(values): {}'.format(type(values)))
    values_sum = sum([trail.value for trail in candidate])
    print('values_sum: {}'.format(values_sum))
    return values_sum
#    print('values: {}'.format(values))
#    total_weight = sum([value for id, value in candidate])
#    return True
#    print('total_weight: {}'.format(total_weight))
#    return total_weight
#    return 100
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

    items = [(1,369), (1,346), (1,322), (1,347), (1,348), (1,383),
             (1,347), (1,364), (1,340), (1,324), (1,365), (1,314),
             (1,306), (1,394), (1,326), (1,310), (1,400), (1,339),
             (1,381), (1,353), (1,383), (1,317), (1,349), (1,396),
             (1,353), (1,322), (1,329), (1,386), (1,382), (1,369),
             (1,304), (1,392), (1,390), (1,307), (1,318), (1,359),
             (1,378), (1,376), (1,330), (1,331)]

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
