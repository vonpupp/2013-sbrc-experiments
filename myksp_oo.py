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
constraints = None

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
                  'n': 1
             } for i,t in islice(enumerate(trace), 200)]

def add_constraint(values, constraint):
    return values[constraint] < 99
  
def add_constraints(values, constraint_list):
    return [add_constraint(values, constraint) for constraint in constraint_list]

def gen_costraints(constraint_list):
    global constraints
    constraints = lambda values: (add_constraints(values, constraint_list))

def solve1():
    global items
    global constraints
    print constraints
    p = KSP('weight', items, constraints = constraints)
    return p.solve('glpk', iprint = 0)
    
def print_results(r):
    print(r.xf)
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
#        print('item: {}: '.format(i))
#        print('item: {}: {}'.format(i, jformat(items[i])))

    #print r.xf
    #t = sum(r.xf['weight'])
    print('cpu: {}'.format(cpu))
    print('mem: {}'.format(mem))
    print('disk: {}'.format(disk))
    print('net: {}'.format(net))
    print('weight: {}'.format(weight))


gen_vms()
#gen_costraints(['cpu'])
#gen_costraints(['net'])
#gen_costraints(['net', 'cpu'])
gen_costraints(['cpu', 'mem', 'disk', 'net'])
r = solve1()
print_results(r)