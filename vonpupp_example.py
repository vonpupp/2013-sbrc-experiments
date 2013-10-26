from random import Random
from time import time
import math
import inspyred
import lib.tracegen.tracegen as tracegen
import itertools


def gen_vms():
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
             }) for i,t in itertools.islice(enumerate(trace), 288)]
    return items

'''    
def fake_gen_vms(random):
    items = [(i, {
                  'name': 'item %d' % i,
                  'weight': 1,
                  'cpu': random.randint(1, 50),
                  'mem': random.randint(1, 50),
                  'disk': random.randint(1, 50),
                  'net': random.randint(1, 50),
                  'n': 1
             }) for i in range(288)]
    return items
'''

def my_generator(random, args):
    items = args['items']
    return [random.choice([0]*99 + [1]) for _ in range(len(items))]

@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    items = args['items']
    totals = {}
    for metric in ['weight', 'cpu', 'mem', 'disk', 'net']:
        totals[metric] = sum([items[i][1][metric] for i, c in enumerate(candidate) if c == 1])
    constraints = [max(0, totals[c] - 99) for c in ['cpu', 'mem', 'disk', 'net']]
    fitness = totals['weight'] - sum(constraints)
    return fitness


if __name__ == '__main__':
    prng = Random()
    prng.seed(time())

#    items = fake_gen_vms(prng)  # gen_vms()
    items = gen_vms()
    #print(items)
    #raw_input('...')
    
    psize = 50
    tsize = 25
    evals = 2500
    
    ea = inspyred.ec.EvolutionaryComputation(prng)
    ea.selector = inspyred.ec.selectors.tournament_selection
    ea.variator = [inspyred.ec.variators.n_point_crossover, inspyred.ec.variators.bit_flip_mutation]
    ea.replacer = inspyred.ec.replacers.generational_replacement
    ea.observer = inspyred.ec.observers.stats_observer
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    final_pop = ea.evolve(my_generator, my_evaluator,
                          bounder=inspyred.ec.DiscreteBounder([0, 1]),
                          maximize=True,
                          pop_size=psize,
                          tournament_size=tsize,
                          num_selected=psize,
                          num_crossover_points=1,
                          num_elites=1,
                          max_evaluations=evals,
                          items=items)

    best = max(final_pop)
    print(best.fitness)
    print(', '.join(['item {}'.format(i) for i, c in enumerate(best.candidate) if c == 1]))
    totals = {}
    for metric in ['weight', 'cpu', 'mem', 'disk', 'net']:
        totals[metric] = sum([items[i][1][metric] for i, c in enumerate(best.candidate) if c == 1])
    print(totals)

