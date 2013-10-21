import inspyred
import random
import time

# https://groups.google.com/d/msg/inspyred/AYh4wL064Tk/BUHRQd40AiYJ
#Hi Aaron Garrett, 
#
# I really appreciate for your help. I have a complicated constrained  linear programming problem, and I extract a simple example as:
# 
#Min z=8*x1+2*x2+ 4*x3+7*x4 + 5*x5
#
#  subject to
#  -3*x1-3*x2+x3+2*x4+3*x5 <= -2
#  -5*x1-3*x2-2*x3-x4+x5 <= -4
#  xj =0 or 1
#
#could you give me some codes to solve it using some tools in the Inspyred package?
#Thanks in advance! 

def my_generator(random, args):
    size = args.get('num_inputs', 3)
    print('size: {}'.format(size))
    result = [random.choice([0, 1]) for i in range(size)]
    print('my_generator: {}'.format(result))
    return result

@inspyred.ec.evaluators.evaluator
def my_evaluator_(candidate, args):
    print('candidate: {}'.format(candidate))
    print('args: {}'.format(args))

@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    # Check the constraints.
    constraint_bounds = [-2, -4]
    constraint_coefficients = [[-3, -3, 1, 2, 3], [-5, -3, -2, -1, 1]]
    constraints = [sum([c * v for c, v in zip(coeff, candidate)]) for coeff in constraint_coefficients]
    print('constraints: {}'.format(constraints))
    failed_constraints = 0
    for constraint, bound in zip(constraints, constraint_bounds):
        if constraint > bound:
            failed_constraints += 1
            
    # Now calculate the fitness. Depending on the computational time, 
    # failed constraints may cause us to just skip this part.
    coefficients = [8, 2, 4, 7, 5]
    fitness = 0
    for c, v in zip(coefficients, candidate):
        fitness += c * v
    
    # Now, punish the candidate for any failed constraints. For the current
    # problem, the largest (i.e., worst) value for any candidate is 26, so
    # we'll make sure that our constraint penalty is larger than that.
    # (We'll make it an order of magnitude larger at 100.)
    return failed_constraints * 100 + fitness


prng_seed = int(time.time())
prng = random.Random()
prng.seed(prng_seed)
optimizer = inspyred.ec.GA(prng)
optimizer.selector = inspyred.ec.selectors.tournament_selection
#optimizer.selector = inspyred.ec.selectors.rank_selection   # <--- This is the GA's default selection scheme.
optimizer.terminator = inspyred.ec.terminators.evaluation_termination
optimizer.observer = inspyred.ec.observers.stats_observer
final_pop = optimizer.evolve(generator=my_generator,
                             evaluator=my_evaluator,
                             pop_size=2,
                             maximize=False,
                             bounder=inspyred.ec.DiscreteBounder([0, 1]),
                             max_evaluations=10,
                             tournament_size=2,
                             mutation_rate=0.1,
                             num_elites=1,
                             num_inputs=5)

final_pop.sort(reverse=True)
print(final_pop[0])
