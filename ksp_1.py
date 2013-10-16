#!/usr/bin/python
import json
'''
Simplest OpenOpt KSP example;
requires FuncDesigner installed.
For some solvers limitations on time, cputime, "enough" value, basic GUI features are available.
See http://openopt.org/KSP for more details
'''
from openopt import *
from numpy import sin, cos


def jformat(json_data):
    return json.dumps(json_data, sort_keys=True,
                      indent=4, separators=(',', ': '))

N = 15

items = [{'name': 'item %d' % i,'weight': 1.5*(cos(i)+1)**2, 'volume': 2*sin(i) + 3, 'n':  1} for i in range(N)]
#'volume': 2*sin(i) + 3, 'n':  1 if i < N/3 else 2 if i < 2*N/3 else 3} for i in range(N)]
items = [
    {'name': 'item 0', 'weight': 1, 'volume': 2, 'n':  1},
    {'name': 'item 1', 'weight': 2, 'volume': 2, 'n':  1},
    {'name': 'item 2', 'weight': 3, 'volume': 2, 'n':  1},
    {'name': 'item 3', 'weight': 4, 'volume': 2, 'n':  1},
    {'name': 'item 4', 'weight': 5, 'volume': 2, 'n':  1},
    {'name': 'item 5', 'weight': 6, 'volume': 2, 'n':  1},
    {'name': 'item 6', 'weight': 7, 'volume': 2, 'n':  1},
    {'name': 'item 7', 'weight': 8, 'volume': 2, 'n':  1},
    {'name': 'item 8', 'weight': 9, 'volume': 2, 'n':  1},
    {'name': 'item 9', 'weight': 10, 'volume': 2, 'n':  1},
]

constraints = lambda values: values['volume'] < 10

p = KSP('weight', items, constraints = constraints)
r = p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/KSP for other solvers
#Solver:   Time Elapsed = 0.73 	CPU Time Elapsed = 0.55
#objFunValue: 27.389749 (feasible, MaxResidual = 0)

print(r.xf) # {'item 131': 2, 'item 18': 1, 'item 62': 2, 'item 87': 1, 'item 43': 1}
# pay attention that Python indexation starts from zero: item 0, item 1 ...
# if fields 'name' are absent, you'll have list of numbers instead of Python dict

print items
#volume = items[0]['volume']

volume = 0
weight = 0
for item in r.xf:
    print item
    i = int(item.split()[1])
    volume += items[i]['volume']
    weight += items[i]['weight']
#   print('item: {}: '.format(i))
#    print('item: {}: {}'.format(i, jformat(items[i])))

#print r.xf
#t = sum(r.xf['weight'])
print('volume: {}'.format(volume))
print('weight: {}'.format(weight))
