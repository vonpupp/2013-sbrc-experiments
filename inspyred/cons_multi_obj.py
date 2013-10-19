import inspyred
import random
import time

def my_generator(random, args):
    size = args.get('num_inputs', 3)
    return [random.choice([0, 1]) for i in range(size)]

@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    # Check the constraints.
    constraint_bounds = [-2, -4]
    constraint_coefficients = [[-3, -3, 1, 2, 3], [-5, -3, -2, -1, 1]]
    constraints = [sum([c * v for c, v in zip(coeff, candidate)]) for coeff in constraint_coefficients]
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
