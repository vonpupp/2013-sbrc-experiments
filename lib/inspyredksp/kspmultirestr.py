import copy
from inspyred import swarm
from inspyred import ec
from inspyred.benchmarks import Benchmark
from inspyred.ec import emo
from inspyred.ec import selectors
import itertools
import math
import random

class Knapsack(Benchmark):
    """Defines the Knapsack benchmark problem.
    
    This class defines the Knapsack problem: given a set of items, each
    with a weight and a value, find the set of items of maximal value
    that fit within a knapsack of fixed weight capacity. This problem 
    assumes that the ``items`` parameter is a list of (weight, value) 
    tuples. This problem is most easily defined as a maximization problem,
    where the total value contained in the knapsack is to be maximized.
    However, for the evolutionary computation (which may create infeasible
    solutions that exceed the knapsack capacity), the fitness is either
    the total value in the knapsack (for feasible solutions) or the
    negative difference between the actual contents and the maximum 
    capacity of the knapsack.

    If evolutionary computation is to be used, then the ``generator`` 
    function should be used to create candidates. If ant colony 
    optimization is used, then the ``constructor`` function creates 
    candidates. The ``evaluator`` function performs the evaluation for 
    both types of candidates.
    
    Public Attributes:
    
    - *capacity* -- the weight capacity of the knapsack
    - *items* -- a list of (weight, value) tuples corresponding to the
      possible items to be placed into the knapsack
    - *components* -- the set of ``TrailComponent`` objects constructed
      from the ``items`` parameter
    - *duplicates* -- Boolean value specifying whether items may be 
      duplicated in the knapsack (i.e., False corresponds to 0/1 Knapsack)
    - *bias* -- the bias in selecting the component of maximum desirability
      when constructing a candidate solution for ant colony optimization 
      (default 0.5)
    
    """
    def __init__(self, capacity, items, duplicates=False):
        Benchmark.__init__(self, len(items))
        self.capacity = capacity
        self.items = items
        self.components = [swarm.TrailComponent((item[0]), value=item[1]['cpu']) for item in items]
        self.duplicates = duplicates
        self.bias = 0.5
        if self.duplicates:
            max_count = [self.capacity // item[0] for item in self.items]
            self.bounder = ec.DiscreteBounder([i for i in range(max(max_count)+1)])
        else:
            self.bounder = ec.DiscreteBounder([0, 1])
        self.maximize = True
        self._use_ants = False
    
    def generator(self, random, args):
        """Return a candidate solution for an evolutionary computation."""
        if self.duplicates:
            max_count = [self.capacity // item[0] for item in self.items]
            return [random.randint(0, m) for m in max_count]
        else:
            return [random.choice([0, 1]) for _ in range(len(self.items))]
    
    def constructor(self, random, args):
        """Return a candidate solution for an ant colony optimization."""
        self._use_ants = True
        candidate = []
        while len(candidate) < len(self.components):
            # Find feasible components
            feasible_components = []
            if len(candidate) == 0:
                feasible_components = self.components
            else:
                #remaining_capacity = self.capacity - sum([c.element for c in candidate])
                remaining_capacity = self.capacity - sum([c.value for c in candidate])
                if self.duplicates:
                    feasible_components = [c for c in self.components if c.element <= remaining_capacity]
                else:
                    feasible_components = [c for c in self.components if c not in candidate and c.element <= remaining_capacity]
            if len(feasible_components) == 0:
                break
            else:
                # Choose a feasible component
                if random.random() <= self.bias:
                    next_component = max(feasible_components)
                else:
                    next_component = selectors.fitness_proportionate_selection(random, feasible_components, {'num_selected': 1})[0]
                candidate.append(next_component)
        return candidate
    
    def evaluator(self, candidates, args):
        """Return the fitness values for the given candidates."""
        fitness = []
        if self._use_ants:
            for candidate in candidates:
                total = 0
                for c in candidate:
                    total += c.value
                fitness.append(total)
        else:
            for candidate in candidates:
                total_value = 0
                total_weight = 0
                for c, i in zip(candidate, self.items):
                    total_weight += c * i[0]
                    total_value += c * i[1]
                if total_weight > self.capacity:
                    fitness.append(self.capacity - total_weight)
                else:
                    fitness.append(total_value)
        return fitness
