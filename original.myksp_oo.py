#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import json
from openopt import *
import lib.tracegen.tracegen as tracegen
from itertools import islice
import uuid
from operator import attrgetter


def jformat(json_data):
    return json.dumps(json_data, sort_keys=True,
                      indent=4, separators=(',', ': '))

items = []
vms_list = []
constraints = None
hosts = 10

class VirtualMachine(dict):
    __count__ = 0
    def __init__(self, cpu, mem, disk, net):
        #id = uuid.uuid1()
        self.value = {}
        self.id = '%d' % VirtualMachine.__count__
        self.value['weight'] = 1
        self.value['cpu'] = cpu
        self.value['mem'] = mem
        self.value['disk'] = disk
        self.value['net'] = net
        self.value['n'] = 1
        VirtualMachine.__count__ += 1

    def __str__(self):
        result = 'VM{}({}, {}, {}, {})'.format(
            self.id,
            self.value['cpu'], self.value['mem'],
            self.value['disk'], self.value['net'])
        return result

    def __getitem__(self, attribute):
        # http://stackoverflow.com/questions/5818192/getting-field-names-reflectively-with-python
        # val = getattr(ob, attr)
        if type(attribute) is str:
            ob = self.value
            #result = getattr(ob, attribute)
            result = ob[attribute]
            #result = attrgetter(attribute)
#            print('getitem: attribute:{}, value:{}'.format(attribute, result))
            return result
        else:
            print('getitem: attribute is not a string, is:{}, value:{}'.format(type(attribute), attribute))


class VMManager:
    def __init__(self):
        tg = tracegen.TraceGenerator()
        trace = tg.gen_trace()
        self.items = [VirtualMachine(t[0], t[1], t[2], t[3])
                          for i, t in islice(enumerate(trace), 288)]
        self.vms_list = [VirtualMachine(t[0], t[1], t[2], t[3])
                          for i, t in islice(enumerate(trace), 288)]

    def get_item_index(id):
        result = -1
        i = 0
        found = False
        while i < len(self.vms_list) and not found:
            item = self.vms_list[i]
            j = item['name'] #int(item['name'].split()[1])
#           print('  get_item_index={} j={}'.format(id, j))
            found = j == id
            if found:
                result = i
            i += 1
        return result

    def get_item_values(id):
        result = self.get_item_index(id)
        if result is not -1:
            result = self.vms_list[result]
        else:
            result = None
        return result

    def items_remove(remove_list):
        for to_delete in remove_list:
            i = get_item_index(to_delete)
            if i is not -1:
                del items[i]

    def __str__(self):
        result = ''
        for item in self.items:
            result += str(item) + ', '
        return result

    def __getitem__(self, attribute):
        return self.items[attribute]

class PhysicalMachine:
    count = 0
    def __init__(self):
        name = 'PM %d' % self.count,
        vms = []

    def used_cpu(self):
        pass
    def used_mem(self):
        pass
    def used_disk(self):
        pass
    def used_net(self):
        pass

    def consumed_power(self):
        pass

class PMManager:
    def __init__(self):
        pass

    def __str__(self):
        pass

def gen_costraint(self, values, constraint):
    return values.value[constraint] < 99

def add_constraints(self, values, constraint_list):
    return [self.add_constraint(values, constraint) for constraint in constraint_list]

class OpenOptStrategyPlacement:
    def __init__(self, items, hosts):
        self.constraints = None
        self.items = items
        self.hosts = hosts
        self.gen_costraints(['cpu', 'mem', 'disk', 'net'])
#        self.gen_costraints(['cpu'])

#    def gen_costraint(self, values, constraint):
#        return values.value[constraint] < 99

#    def add_constraints(self, values, constraint_list):
#        return [self.add_constraint(values, constraint) for constraint in constraint_list]

    def gen_costraints(self, constraint_list):
        self.constraints = lambda values: (add_constraints(values, constraint_list))

    def get_openopt_vms(self, items_list):
        result = []
        for item in items_list:
            # i = int(item.split()[1])
            result += [item]
        return result

    def solve_host(self):
        #print(list(self.items))
#        print(self.items[0])
#        print(self.constraints)
        p = KSP('weight', self.items, constraints = self.constraints)
        result = p.solve('glpk', iprint = -1)
        print result.xf
        return result
#        return 10

    def items_remove(remove_list):
        global items
        for to_delete in remove_list:
            i = get_item_index(to_delete)
            if i is not -1:
                del items[i]

    def solve_hosts(self):
        placement = []
        for host in range(hosts):
            vms = self.solve_host()
            ids = self.get_openopt_vms(vms.xf)
            print('HOST: {} ({})'.format(host, ids))
            #print('HOST: {} ({})'.format(host, items_str('VMs', vms.xf)))
            placement.append(ids)
            if vms is not None:
                #print_results(vms)
#                print('solve_hosts: {}'.format(map(get_item_index, vms.xf)))
#                print_items('vms', vms.xf)
                items_remove(vms.xf)
#             print('items: {}'.format(items))
        #TODO: Assing to host
        return placement

class AntColonyStrategyPlacement:
    pass

class Manager:
    def __init__(self, strategy):
        self.vmm = VMManager()
        self.pmm = PMManager()
        self.strategy = strategy
#    items = gen_vms()
#    vms_list = gen_vms()
#    gen_costraints(['cpu', 'mem', 'disk', 'net'])
#    placement = solve_hosts()
#    print placement
#    power = calculate_placement_power(placement)
#    print('TOTAL POWER: {} WATTS'.format(power))

    def assign_vm_host(self, vm, host):
        pass

    def unplaced_vms(self):
        pass

    def placed_vms(self):
        pass

def gen_vms():
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
    return items

def add_constraint(values, constraint):
    # http://stackoverflow.com/questions/5818192/getting-field-names-reflectively-with-python
    # val = getattr(ob, attr)
    return values[constraint] < 99

def add_constraints(values, constraint_list):
    return [add_constraint(values, constraint) for constraint in constraint_list]

def gen_costraints(constraint_list):
    global constraints
    constraints = lambda values: (add_constraints(values, constraint_list))

def get_item_values(id):
    result = get_item_index(id)
    if result is not -1:
        result = vms_list[result]
    else:
        result = None
    return result

def get_item_index(id):
    result = -1
    i = 0
    found = False
    while i < len(vms_list) and not found:
        item = vms_list[i]
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
    placement = []
    for host in range(hosts):
        vms = solve_host()
        ids = get_openopt_vms(vms.xf)
        print('HOST: {} ({})'.format(host, ids))
        #print('HOST: {} ({})'.format(host, items_str('VMs', vms.xf)))
        placement.append(ids)
        if vms is not None:
            print_results(vms)
            #sorted_vms = sort(vms.xf)
#            print('solve_hosts: {}'.format(map(get_item_index, vms.xf)))
#            print_items('vms', vms.xf)
            items_remove(vms.xf)
#        print('items: {}'.format(items))
    return placement

def get_openopt_vms(items_list):
    result = []
    for item in items_list:
        # i = int(item.split()[1])
        result += [item]
    return result

def print_results(r):
    #print(r.xf)
    cpu = mem = disk = net = 0
    weight = 0
    for item in r.xf:
        #i = int(item.split()[1])
        v = get_item_values(item)
        print('  {}, values: ({})'.format(item, v))
        cpu += v['cpu']
        mem += v['mem']
        disk += v['disk']
        net += v['net']
        weight += v['weight']
#        print('item: {}: '.format(i))
#        print('item: {}: {}'.format(i, jformat(items[i])))

    #print r.xf
    #t = sum(r.xf['weight'])
    print('  cpu: {}'.format(cpu))
    print('  mem: {}'.format(mem))
    print('  disk: {}'.format(disk))
    print('  net: {}'.format(net))
    print('  weight: {}'.format(weight))

def cpu_power(cpu):
    # P(cpu) = P_idle + (P_busy - P_idle) x cpu
    p_idle = 114.0
    p_busy = 250.0
    result = p_idle + (p_busy - p_idle) * cpu/100
    return result

def get_cpu(host):
    result = 0
    for vm_id in host:
        #result += calculate_vm_power(vm)
        print('  vm_id: {}'.format(vm_id))
        vm_idx = get_item_index(vm_id)
        print('  vm_idx: {}'.format(vm_idx))
        vm = vms_list[vm_idx]
        print('  vm: {}'.format(vm))
        cpu = vm['cpu']
        print('  cpu: {}'.format(vm['cpu']))
        result += cpu
        print('  result: {}'.format(result))
    return result

def calculate_placement_power(placement):
    result = 0.0
    for host in placement:
        #result += calculate_host_power(host)
        host_power = cpu_power(get_cpu(host))
        result += host_power
        print('HOST POWER: {}'.format(host_power))
    return result

def my_multi_bpp_place():
    global items
    global vms_list
    items = gen_vms()
    vms_list = gen_vms()
#    gen_costraints(['cpu'])
#    gen_costraints(['net'])
#    gen_costraints(['net', 'cpu'])
    gen_costraints(['cpu', 'mem', 'disk', 'net'])
#    r = solve_host()
    placement = solve_hosts()
    print placement
    power = calculate_placement_power(placement)
    print('TOTAL POWER: {} WATTS'.format(power))
#    print_results(r)


if __name__ == "__main__":
#    vmm = VMManager()
#    strategy = OpenOptStrategyPlacement(vmm, 2)
#    m = Manager(strategy)
    
    m = Manager()
    m.strategy = OpenOptStrategyPlacement(288, 288)
    m.solve_hosts()
    p = m.calculate_power_consumed()
    h = m.calculate_physical_hosts_used()
    h = m.calculate_physical_hosts_idle()
    t = m.calculate_time_elapsed()
    
#    m = Manager()
#    m.strategy = NoEnergyAwareStrategyPlacement(288, 288)
#    m.solve_hosts()
#    m.calculate_placement_power()
#    h = m.calculate_physical_hosts_number()
    
    print(m)
    print(m.vmm.items)
    for vm in vmm.items:
#        print('{}'.format(vm.value['cpu']))
#        print('{}'.format(vm.value['n']))
        #print('{}'.format(vm['mem']))
        #print('{}'.format(vm['disk']))
        #print('{}'.format(vm['net']))
        pass
#    placement = strategy.solve_host()
    placement = strategy.solve_hosts()
    #my_multi_bpp_place()
