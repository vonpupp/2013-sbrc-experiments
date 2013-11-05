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
hosts = 10

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

def get_item_values(index):
    result = get_item_index(index)
    if result is not -1:
        result = items[result]
    else:
        result = None
    return result
	  
def get_item_index(id):
    result = -1
    i = 0
    found = False
    while i < len(items) and not found:
        item = items[i]
        j = item['name'] #int(item['name'].split()[1])
#        print('  get_item_index={} j={}'.format(id, j))
        found = j == id
        if found:
            result = i
        i += 1
    return result
  
#def get_item_id(value):
#    result = -1
#    item = items[value]
#    result = int(item['name'].split()[1])
#    return result

def items_remove(remove_list):
    global items
    for to_delete in remove_list:
        i = get_item_index(to_delete)
        if i is not -1:
            del items[i]

def solve_host():
    global items
    global constraints
#    print constraints
    p = KSP('weight', list(items), constraints = constraints)
    result = p.solve('glpk', iprint = -1)
    #print('INDEX: {}'.format(map(get_item_index, [12, 4])))
    return result

def solve_hosts():
    for host in range(hosts):
        vms = solve_host()
        if vms is not None:
            print_results(vms)
            #sorted_vms = sort(vms.xf)
#            print('solve_hosts: {}'.format(map(get_item_index, vms.xf)))
            print_items('vms', vms.xf)
            items_remove(vms.xf)
#        print('items: {}'.format(items))

def print_items(caption, items_list):
    to_print = []
    for item in items_list:
        i = int(item.split()[1])
        to_print += [i]
    print('{}: {}'.format(caption, to_print))

def print_results(r):
    #print(r.xf)
    cpu = mem = disk = net = 0
    weight = 0
    for item in r.xf:
        i = int(item.split()[1])
        v = get_item_values(item)
        print('{}, values: ({})'.format(item, v))
        cpu += v['cpu']
        mem += v['mem']
        disk += v['disk']
        net += v['net']
        weight += v['weight']
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
#r = solve_host()
solve_hosts()
#print_results(r)