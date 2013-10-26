#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import json
from openopt import *
import lib.tracegen.tracegen as tracegen
from itertools import islice
import uuid
from operator import attrgetter
import timeit


class VirtualMachine(dict):
    __count__ = 0
    def __init__(self, cpu, mem, disk, net):
        id = uuid.uuid1()
        self.value = {}
        self.id = '%d' % VirtualMachine.__count__
        #self.id = str(id)[4:8] #'%d' % VirtualMachine.__count__
        self.value['weight'] = 1
        self.value['cpu'] = cpu
        self.value['mem'] = mem
        self.value['disk'] = disk
        self.value['net'] = net
        self.value['n'] = 1
        self.value['placed'] = 0
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
    def __init__(self, total_vm):
        tg = tracegen.TraceGenerator()
        trace = tg.gen_trace()
        self.items = [VirtualMachine(t[0], t[1], t[2], t[3])
                          for i, t in islice(enumerate(trace), total_vm)]
        self.vms_list = [VirtualMachine(t[0], t[1], t[2], t[3])
                          for i, t in islice(enumerate(trace), total_vm)]

    def get_item_index(self, id):
        result = -1
        i = 0
        found = False
        while i < len(self.items) and not found:  # TODO: vms_list
            item = self.items[i]
            j = item.id #int(item['name'].split()[1])
#           print('  get_item_index={} j={}'.format(id, j))
            found = j == id.id
            if found:
                result = i
            i += 1
        return result

    def get_item_values(self, id):
        result = self.get_item_index(id)
        if result is not -1:
            result = self.items[result]  # TODO: vms_list
        else:
            result = None
        return result

    def items_remove(self, remove_list):
        for to_delete in remove_list:
            i = self.get_item_index(to_delete)
            #self.items.remove(to_delete)
            if i is not -1:
                del self.items[i]
                #value = self.items[i]
                #self.items.remove(value)

    def __str__(self):
        result = 'VMPool['
        for item in self.items:
            result += str(item) + ', '
        result += ']'
        return result

#    def __getitem__(self, attribute):
#        return self.items[attribute]

class PhysicalMachine:
    __count__ = 0
    def __init__(self):
        self.id = '%d' % self.__count__
        self.vms = []
        self.cpu = self.mem = 0
        self.disk = self.net = 0
        PhysicalMachine.__count__ += 1

    def consumed_power(self):
        pass
    
    def place_vm(self, vm):
        self.vms.append(vm)
        vm.value['placed'] = 1
        self.cpu = self.mem = 0
        self.disk = self.net = 0
        for vm in self.vms:
            self.cpu += vm.value['cpu']
            self.mem += vm.value['mem']
            self.disk += vm.value['disk']
            self.net += vm.value['net']
    
    def vms_to_str(self):
        result = ''
        for vm in self.vms:
            result += str(vm) + ', '
        return result
    
    def __str__(self):
        result = 'PM[{}/{}]({}, {}, {}, {}) | [{}]'.format(
            self.id,
            len(self.vms),
            self.cpu,
            self.mem,
            self.disk,
            self.net,
            self.vms_to_str())
        return result

class PMManager:
    def __init__(self, total_pm):
        self.items = [PhysicalMachine()
                          for i in range(total_pm)]

    def __str__(self):
        pass

def gen_costraint(self, values, constraint):
    return values.value[constraint] < 99

def add_constraints(self, values, constraint_list):
    return [self.add_constraint(values, constraint) for constraint in constraint_list]

def add_constraint(values, constraint):
    # http://stackoverflow.com/questions/5818192/getting-field-names-reflectively-with-python
    # val = getattr(ob, attr)
    return values[constraint] < 99

def add_constraints(values, constraint_list):
    return [add_constraint(values, constraint) for constraint in constraint_list]

#def gen_costraints(constraint_list):
#    global constraints
#    constraints = lambda values: (add_constraints(values, constraint_list))

class OpenOptStrategyPlacement:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.vmm = None
        self.pmm = None
        #self.items_count = items_count
        #self.hosts_count = hosts_count
        self.gen_costraints(['cpu', 'mem', 'disk', 'net'])
#        self.gen_costraints(['cpu'])

#    def gen_costraint(self, values, constraint):
#        return values.value[constraint] < 99

#    def add_constraints(self, values, constraint_list):
#        return [self.add_constraint(values, constraint) for constraint in constraint_list]

    def gen_costraints(self, constraint_list):
        self.constraints = lambda values: (
#                                      values['cpu'] < 100,
#                                      values['mem'] < 100,
#                                      values['disk'] < 100,
#                                      values['net'] < 100,
#                                      values['placed'] == 0,
#                                      values['nItems'] <= 10,
#                                      values['nItems'] >= 5
#            values['placed'] < 1,
            add_constraints(values, constraint_list)
        )

    def get_vm_objects(self, items_list):
        #print('get_vm_objects self.vmm.items: {}'.format(self.vmm))
        #print('get_vm_objects self.items: {}'.format(self.items))
        #print('get_vm_objects items_list: {}'.format(items_list.xf))
        result = []
        #test = self.vmm.get_item_values('5')
        for item in items_list.xf:
            # i = int(item.split()[1])
            result += [self.vmm.items[item]]#get_item_values(item)]
            #print('result: {}'.format(result))
        return result
      
    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items
        #print('OpenOptStrategyPlacement set_vmm: {}'.format(self.vmm))

    def solve_host(self):
        #print(list(self.items))
        #print(self.items[0])
#        print(self.constraints)
        p = KSP('weight', self.items, constraints = self.constraints)
        result = p.solve('glpk', iprint = -1)
        #print('solve_host result: {}'.format(result.xf))
        #print('solve_host result: {}'.format(result.xf[0]))
        return result
#        return 10

#    def items_remove(remove_list):
#        global items
#        for to_delete in remove_list:
#            i = get_item_index(to_delete)
#            if i is not -1:
#                del items[i]

class Manager:
    def __init__(self):
        self.placement = []
        self.total_pm = 0
        self.total_vm = 0
        self.vmm = None
        self.pmm = None
        self.strategy = None
#    items = gen_vms()
#    vms_list = gen_vms()
#    gen_costraints(['cpu', 'mem', 'disk', 'net'])
#    placement = solve_hosts()
#    print placement
#    power = calculate_placement_power(placement)
#    print('TOTAL POWER: {} WATTS'.format(power))

    def set_vm_count(self, total_vm):
        self.total_vm = total_vm
        self.vmm = VMManager(total_vm)
        #print('1 Manager self.vmm: {}'.format(self.vmm))

    def set_pm_count(self, total_pm):
        self.total_pm = total_pm
        self.pmm = PMManager(total_pm)
        
    def set_strategy(self, strategy):
        self.strategy = strategy
        self.strategy.set_vmm(self.vmm)
        #self.strategy.vmm = self.vmm
        #self.strategy.items = self.vmm.items
        self.strategy.pmm = self.pmm
      
    def place_vms(self, vms, host):
        #host.vms = vms
        i = 0
        while i < len(vms):
            #vm = self.vmm.items[i]
            vm = vms[i]
            host.place_vm(vm)
            print('{}'.format(host))
            #self.vmm.items.remove(vm)
            i += 1
        self.vmm.items_remove(vms)
#        for vm in vms:
#            host.place_vm(vm)
            #vm.value['placed'] = 1
            #self.vmm.items.remove(vm)
            #print('left: {}'.format(self.vmm))
            #vm.value['placed'] = int(host.id)

    def placed_vms(self):
        pass
      
    def unplaced_vms(self):
        pass
      
#    def remove_placed_vms(self):
#        for vm in self.vmm.items:
#            if vm.value['placed'] == 1:
#                self.vmm.items.remove(vm)

    def solve_hosts(self):
        #placement = []
        for host in self.pmm.items: #range(self.total_pm):
            solution = self.strategy.solve_host()
            #print('solution: {}'.format(solution.xf))
            #print('Manager self.vmm: {}'.format(self.vmm))
            vms = self.strategy.get_vm_objects(solution)
            #placement.append(vms)
            if vms is not None:
                self.place_vms(vms, host)
                #print('assignment: {}'.format(host))
                #print('left: {}'.format(self.vmm))
                #self.remove_placed_vms()
        #return placement

    def calculate_power_consumed(self):
        pass

if __name__ == "__main__":
#    vmm = VMManager()
#    strategy = OpenOptStrategyPlacement(vmm, 2)
#    m = Manager(strategy)
    
    
    m = Manager()
    #m.set_trace_file('blabla')
    m.set_pm_count(2)
    m.set_vm_count(288)
    s = OpenOptStrategyPlacement()
    m.set_strategy(s)
    m.solve_hosts()
    #p = m.calculate_power_consumed()
#    uh = m.calculate_physical_hosts_used()
#    ih = m.calculate_physical_hosts_idle()
#    t = m.calculate_time_elapsed()
    
#    m = Manager()
#    m.strategy = NoEnergyAwareStrategyPlacement(288, 288)
#    m.solve_hosts()
#    m.calculate_placement_power()
#    h = m.calculate_physical_hosts_number()
    
#    print(m)
#    print(m.vmm.items)
#    for vm in vmm.items:
#        print('{}'.format(vm.value['cpu']))
#        print('{}'.format(vm.value['n']))
        #print('{}'.format(vm['mem']))
        #print('{}'.format(vm['disk']))
        #print('{}'.format(vm['net']))
#        pass
#    placement = strategy.solve_host()
#    placement = strategy.solve_hosts()
    #my_multi_bpp_place()
