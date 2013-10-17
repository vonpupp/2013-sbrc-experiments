#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import json
from openopt import *
import lib.tracegen.tracegen as tracegen
from itertools import islice

def jformat(json_data):
    return json.dumps(json_data, sort_keys=True,
                      indent=4, separators=(',', ': '))

items = []
constraints = lambda values: (
                                      values['cpu'] < 99,
                                      values['mem'] < 100,
                                      values['disk'] < 100,
                                      values['net'] < 100,
#                                      values['nItems'] <= 10,
#                                      values['nItems'] >= 5
                                      # we could use lambda-func, e,g.
                                      # values['mass'] + 4*values['volume'] < 100
                             )
tg = tracegen.TraceGenerator()
trace = tg.gen_trace()
items = [{
              'name': 'item %d' % i,
#             'weight': 1.5*(cos(i)+1)**2,
              'weight': 1,
              'cpu': t[0],
              'mem': t[1],
              'disk': t[2],
              'net': t[3],
              'n':  1
         } for i,t in islice(enumerate(trace), 10)]


def gen_vms():
    global items
    tg = tracegen.TraceGenerator()
    trace = tg.gen_trace()
    items = [{
                  'name': 'item %d' % i,
#                  'weight': 1.5*(cos(i)+1)**2,
                  'weight': 1,
                  'cpu': t[0],
                  'mem': t[1],
                  'disk': t[2],
                  'net': t[3],
                  'n':  1
             } for i,t in enumerate(trace)]
#print items
#'cpu': 2*sin(i) + 3, 'n':  1 if i < N/3 else 2 if i < 2*N/3 else 3} for i in range(N)]
#items = [
#    {'name': 'item 0', 'weight': 1, 'cpu': 2, 'n':  1},
#    {'name': 'item 1', 'weight': 2, 'cpu': 2, 'n':  1},
#    {'name': 'item 2', 'weight': 3, 'cpu': 2, 'n':  1},
#    {'name': 'item 3', 'weight': 4, 'cpu': 2, 'n':  1},
#    {'name': 'item 4', 'weight': 5, 'cpu': 2, 'n':  1},
#    {'name': 'item 5', 'weight': 6, 'cpu': 2, 'n':  1},
#    {'name': 'item 6', 'weight': 7, 'cpu': 2, 'n':  1},
#    {'name': 'item 7', 'weight': 8, 'cpu': 2, 'n':  1},
#    {'name': 'item 8', 'weight': 9, 'cpu': 2, 'n':  1},
#    {'name': 'item 9', 'weight': 10, 'cpu': 2, 'n':  1},
#]

def cons_cpu():
#constraints = lambda values: values['cpu'] < 100
    constraints = lambda values: (
                                      values['cpu'] < 100,
#                                      values['mem'] < 100,
#                                      values['disk'] < 100,
#                                      values['net'] < 100,
#                                      values['nItems'] <= 10,
#                                      values['nItems'] >= 5
                                      # we could use lambda-func, e,g.
                                      # values['mass'] + 4*values['volume'] < 100
                                 )
    p = KSP('weight', items, constraints = constraints)
    return p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/KSP for other solvers

    
def cons_cpu_mem():
#constraints = lambda values: values['cpu'] < 100
    constraints = lambda values: (
                                      values['cpu'] < 100,
                                      values['mem'] < 100,
#                                      values['disk'] < 100,
#                                      values['net'] < 100,
#                                      values['nItems'] <= 10,
#                                      values['nItems'] >= 5
                                 )
    
def cons_cpu_mem_disk():
#constraints = lambda values: values['cpu'] < 100
    constraints = lambda values: (
                                      values['cpu'] < 100,
                                      values['mem'] < 100,
                                      values['disk'] < 100,
#                                      values['net'] < 100,
#                                      values['nItems'] <= 10,
#                                      values['nItems'] >= 5
                                 )
    
def cons_all():
#constraints = lambda values: values['cpu'] < 100
    constraints = lambda values: (
                                      values['cpu'] < 100,
                                      values['mem'] < 100,
                                      values['disk'] < 100,
                                      values['net'] < 100,
#                                      values['nItems'] <= 10,
#                                      values['nItems'] >= 5
                                 )


def solve1():
    #constraints = cons_cpu()
    global items
    global constraints
    p = KSP('weight', items, constraints = constraints)
    return p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/KSP for other solvers
    #Solver:   Time Elapsed = 0.73 	CPU Time Elapsed = 0.55
    #objFunValue: 27.389749 (feasible, MaxResidual = 0)

#r = solve1()
#cons_cpu()

p = KSP('weight', items, constraints = constraints)
r = p.solve('glpk', iprint = 0) # requires cvxopt and glpk installed, see http://openopt.org/KSP for other solvers

print(r.xf)
# pay attention that Python indexation starts from zero: item 0, item 1 ...
# if fields 'name' are absent, you'll have list of numbers instead of Python dict

#print items
#cpu = items[0]['cpu']

cpu = mem = disk = net = 0
weight = 0
for item in r.xf:
    i = int(item.split()[1])
    print('{}, values: {}'.format(item, items[i]))
    cpu += items[i]['cpu']
    mem += items[i]['mem']
    disk += items[i]['disk']
    net += items[i]['net']
    weight += items[i]['weight']
#   print('item: {}: '.format(i))
#    print('item: {}: {}'.format(i, jformat(items[i])))

#print r.xf
#t = sum(r.xf['weight'])
print('cpu: {}'.format(cpu))
print('mem: {}'.format(mem))
print('disk: {}'.format(disk))
print('net: {}'.format(net))
print('weight: {}'.format(weight))
