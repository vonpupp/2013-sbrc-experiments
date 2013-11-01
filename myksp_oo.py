#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

#import json
import random
import uuid
from itertools import islice
import operator
import datetime
import csv
import pickle
import copy

import lib.tracegen.tracegen as tracegen
from openopt import *
import inspyred


class VirtualMachine(dict):
    __count__ = 0
    def __init__(self, id, cpu, mem, disk, net):
        #id = uuid.uuid1()
        self.value = {}
        self.id = '%d' % id #VirtualMachine.__count__
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
            result = ob[attribute]
            return result
        else:
            print('getitem: attribute is not a string, is:{}, value:{}'.format(type(attribute), attribute))


class VMManager:
    def __init__(self, trace_file, total_vm):
        tg = tracegen.TraceGenerator(trace_file)
        trace = tg.gen_trace()
        self.items = []
        for t in islice(enumerate(trace), total_vm):
            self.items += [VirtualMachine(t[0], t[1][0], t[1][1], t[1][2], t[1][3])]

    def get_item_index(self, id):
        result = -1
        i = 0
        found = False
        while i < len(self.items) and not found:
            item = self.items[i]
            j = item.id
            found = j == id.id
            if found:
                result = i
            i += 1
        return result

    def get_item_values(self, id):
        result = self.get_item_index(id)
        if result is not -1:
            result = self.items[result]
        else:
            result = None
        return result

    def items_remove(self, remove_list):
        for to_delete in remove_list:
            i = self.get_item_index(to_delete)
            if i is not -1:
                del self.items[i]

    def __str__(self):
        result = 'VMPool['
        for item in self.items:
            result += str(item) + ', '
        result += ']'
        return result


class PhysicalMachine:
    __count__ = 0
    def __init__(self, id):
        self.id = '%d' % id # self.__count__
        self.vms = []
        self.startup_machine()
        PhysicalMachine.__count__ += 1
        
    def startup_machine(self):
        self.cpu = 15
        self.mem = 15
        self.disk = self.net = 0
        self.suspended = False

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
        if self.suspended:
            state = 'sus'
        else:
            state = 'run'
        result = 'PM[{}-{}/{}]({}, {}, {}, {}) | [{}/{}]'.format(
            self.id,
            state,
            self.estimate_consumed_power(),
            self.cpu,
            self.mem,
            self.disk,
            self.net,
            len(self.vms),
            self.vms_to_str())
        return result
    
    def suspend(self):
        self.suspended = True
        self.cpu = 0
        self.mem = 0
        self.disk = 0
        self.net = 0
        
    def wol(self):
        self.startup_machine()
    
    def estimate_consumed_power(self):
        if self.suspended:
            result = 5
        else:
            # P(cpu) = P_idle + (P_busy - P_idle) x cpu
            p_idle = 114.0
            p_busy = 250.0
            result = p_idle + (p_busy - p_idle) * self.cpu/100
            #if self.vms != []:
            #    p_idle = 114.0
            #    p_busy = 250.0
            #    result = p_idle + (p_busy - p_idle) * self.cpu/100
            #else:
            #    pass
        return result

class PMManager:
    def __init__(self, total_pm):
        self.items = [PhysicalMachine(i)
                          for i in range(total_pm)]

    def __str__(self):
        result = 'PMPool['
        for item in self.items:
            result += str(item) + ', '
        result += ']'
        return result

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

class EnergyUnawareStrategyPlacement:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.vmm = None
        self.pmm = None
        self.gen_costraints(['cpu', 'mem', 'disk', 'net'])

    def gen_costraints(self, constraint_list):
        self.constraints = lambda values: (
            add_constraints(values, constraint_list)
        )
    
    def check_constraints(self, item_list):
        total_cpu = sum(map(operator.itemgetter('cpu'), item_list))
        total_mem = sum(map(operator.itemgetter('mem'), item_list))
        total_disk = sum(map(operator.itemgetter('disk'), item_list))
        total_net = sum(map(operator.itemgetter('net'), item_list))
        return (total_cpu < 100) and (total_mem < 100) and \
            (total_disk < 100) and (total_net < 100)

    def get_vm_objects(self, items_list):
        return items_list
      
    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items

    def solve_host(self):
        result = []
        items_list = []
        more = True
        #tmp = self.vmm.items.copy()
        tmp = copy.deepcopy(self.vmm.items)
        done = False
        while not done:
            index = random.randrange(len(tmp))
            vm = tmp.pop(index)
            more = self.check_constraints(items_list + [vm])
            if more:
                #result += [vm.id]
                result += [vm]
                items_list += [vm]
            else:
                tmp.append(vm)
            done = not more or (len(tmp) == 0)
        return result


class OpenOptStrategyPlacement:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.vmm = None
        self.pmm = None
        #self.items_count = items_count
        #self.hosts_count = hosts_count
        self.gen_costraints(['cpu', 'mem', 'disk', 'net'])

    def gen_costraints(self, constraint_list):
        self.constraints = lambda values: (
            add_constraints(values, constraint_list)
        )

    def get_vm_objects(self, items_list):
        result = []
        for item in items_list.xf:
            result += [self.vmm.items[item]]#get_item_values(item)]
        return result
      
    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items

    def solve_host(self):
        p = KSP('weight', self.items, constraints = self.constraints)
        result = p.solve('glpk', iprint = -1)
        return result


def my_generator(random, args):
    items = args['items']
    #print items
    return [random.choice([0]*99 + [1]) for _ in range(len(items))]

@inspyred.ec.evaluators.evaluator
def my_evaluator(candidate, args):
    items = args['items']
    totals = {}
    for metric in ['weight', 'cpu', 'mem', 'disk', 'net']:
        totals[metric] = sum([items[i][1][metric] for i, c in enumerate(candidate) if c == 1])
    constraints = [max(0, totals[c] - 99) for c in ['cpu', 'mem', 'disk', 'net']]
    fitness = totals['weight'] - sum(constraints)
    #print fitness
    return fitness

class EvolutionaryComputationStrategyPlacement:
    def __init__(self):
        self.constraints = None
        self.items = None
        self.itemstuples = None
        self.vmm = None
        self.pmm = None
        #self.gen_costraints(['cpu', 'mem', 'disk', 'net'])

    def gen_vms(self):
        self.itemstuples = [(i, {
                      'name': 'item %d' % i,
                      'weight': 1,
                      'cpu': vm.value['cpu'],
                      'mem': vm.value['mem'],
                      'disk': vm.value['disk'],
                      'net': vm.value['net'],
                      'n': 1
                 }) for i, vm in enumerate(self.items)]
        return self.itemstuples

    #def check_constraints(self, item_list):
    #    total_cpu = sum(map(operator.itemgetter('cpu'), item_list))
    #    total_mem = sum(map(operator.itemgetter('mem'), item_list))
    #    total_disk = sum(map(operator.itemgetter('disk'), item_list))
    #    total_net = sum(map(operator.itemgetter('net'), item_list))
    #    return (total_cpu < 100) and (total_mem < 100) and \
    #        (total_disk < 100) and (total_net < 100)
    #
    def get_vm_objects(self, items_list):
        result = []
        for item in items_list:
            result += [self.vmm.items[item]]#get_item_values(item)]
        return result
      
    def set_vmm(self, vmm):
        self.vmm = vmm
        self.items = self.vmm.items

    def solve_host(self):
        prng = random.Random()
        prng.seed(time.time())
        
        itemstuples = self.gen_vms()
        
        psize = 50
        tsize = 25
        evals = 2500
        
        ea = inspyred.ec.EvolutionaryComputation(prng)
        ea.selector = inspyred.ec.selectors.tournament_selection
        ea.variator = [inspyred.ec.variators.n_point_crossover, inspyred.ec.variators.bit_flip_mutation]
        ea.replacer = inspyred.ec.replacers.generational_replacement
        #ea.observer = inspyred.ec.observers.stats_observer
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
                              items=itemstuples
                              )
    
        best = max(final_pop)
        result = [i for i, c in enumerate(best.candidate) if c == 1]
        return result


class Manager:
    def __init__(self):
        self.placement = []
        self.total_pm = 0
        self.total_vm = 0
        self.vmm = None
        self.pmm = None
        self.strategy = None

    def set_vm_count(self, trace_file, total_vm):
        self.total_vm = total_vm
        self.vmm = VMManager(trace_file, total_vm)

    def set_pm_count(self, total_pm):
        self.total_pm = total_pm
        self.pmm = PMManager(total_pm)
        
    def set_strategy(self, strategy):
        self.strategy = strategy
        self.strategy.set_vmm(self.vmm)
        self.strategy.pmm = self.pmm
      
    def place_vms(self, vms, host):
        i = 0
        while i < len(vms):
            vm = vms[i]
            host.place_vm(vm)
            print('{}'.format(host))
            i += 1
        self.vmm.items_remove(vms)

    def placed_vms(self):
        result = 0
        for host in self.pmm.items:
            result += len(host.vms)
        return result
      
    def unplaced_vms(self):
        return self.total_vm - self.placed_vms()
      
    def solve_hosts(self):
        for host in self.pmm.items:
            if self.vmm.items != []:
                solution = self.strategy.solve_host()
                vms = self.strategy.get_vm_objects(solution)
                if vms is not None:
                    self.place_vms(vms, host)
            else:
                if not isinstance(self.strategy, EnergyUnawareStrategyPlacement):
                    host.suspend()
                print(host)
        
    def calculate_power_consumed(self):
        result = 0
        for host in self.pmm.items:
            result += host.estimate_consumed_power()
        return result
    
    def calculate_physical_hosts_used(self):
        result = 0
        for host in self.pmm.items:
            if host.vms != []:
                result += 1
        return result
    
    def calculate_physical_hosts_suspended(self):
        result = 0
        for host in self.pmm.items:
            if host.suspended:
                result += 1
        return result
    
    def calculate_physical_hosts_idle(self):
        result = 0
        for host in self.pmm.items:
            if host.vms == [] and not host.suspended:
                result += 1
        return result

import time
from functools import wraps

PROF_DATA = {}

def profile(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        start_time = time.time()

        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time

        if fn.__name__ not in PROF_DATA:
            PROF_DATA[fn.__name__] = [0, []]
        PROF_DATA[fn.__name__][0] += 1
        PROF_DATA[fn.__name__][1].append(elapsed_time)

        return ret

    return with_profiling

def print_prof_data():
    for fname, data in PROF_DATA.items():
        max_time = max(data[1])
        avg_time = sum(data[1]) / len(data[1])
        print "Function %s called %d times. " % (fname, data[0]),
        print 'Execution time max: %.3f, average: %.3f' % (max_time, avg_time)

def clear_prof_data():
    global PROF_DATA
    PROF_DATA = {}

class Simulator:
    def __init__(self):
        self.results = []
        self.writer = None
    
    def csv_write_simulation(self, fout):
        self.out_file = open(fout, 'wb')
        #out_file = open(fout, 'a+')
        
        self.writer = csv.writer(self.out_file, delimiter='\t')
        header = ['#PM', '#VM',
                  '#PM-U', '#PM-S', '#PM-I',
                  '#VM-P', 'VM-U',
                  'KW',
                  'strategy',
                  #'ST', 'ET',
                  'T']
        self.writer.writerow(header)
        
    def csv_append_scenario(self, scenario):
        #for r in self.results:
        r = self.results[scenario]
        self.writer.writerow([r['physical_mahines_count'], r['virtual_mahines_count'],
              r['physical_machines_used'],
              r['physical_machines_suspended'],
              r['physical_machines_idle'],
              r['virtual_machines_placed'], r['virtual_machines_unplaced'],
              r['energy_consumed'],
              r['strategy'].__class__.__name__,
              #r['start_time'], r['end_time'],
              r['elapsed_time']])
        
    def csv_close_simulation(self):
        self.out_file.close()
        
    def pickle_writer(self, fout):
        try:
            out_file = open(fout, 'wb')
            pickle.dump(self.results, out_file)
        except:
            pass
        
    def simulate_scenario(self, strategy, trace_file, pms, vms):
        result = {}
        result['start_time'] = time.time()
        result['manager'] = m = Manager()
        result['physical_mahines_count'] = pms
        m.set_pm_count(pms)
        result['virtual_mahines_count'] = vms
        m.set_vm_count(trace_file, vms)
        result['strategy'] = strategy
        m.set_strategy(strategy)
        m.solve_hosts()
        result['placement'] = m.pmm
        result['energy_consumed'] = m.calculate_power_consumed()
        result['physical_machines_used'] = m.calculate_physical_hosts_used()
        result['physical_machines_idle'] = m.calculate_physical_hosts_idle()
        result['physical_machines_suspended'] = m.calculate_physical_hosts_suspended()
        result['virtual_machines_placed'] = m.placed_vms()
        result['virtual_machines_unplaced'] = m.unplaced_vms()
        result['end_time'] = time.time()
        result['elapsed_time'] = result['end_time'] - result['start_time']
        self.results.append(result)
        return len(self.results)-1

    def simulate_strategy(self, strategy, trace_file, pms_scenarios, vms_scenarios):
        stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S')
        #strategy = EnergyUnawareStrategyPlacement()
        for pms in pms_scenarios:
            self.csv_write_simulation('results/{}-{}-{}.csv'.format(strategy.__class__.__name__, pms, stamp))
            for vms in vms_scenarios:
                scenario = self.simulate_scenario(strategy, trace_file, pms, vms)
                self.csv_append_scenario(scenario)
            self.csv_close_simulation()
        self.pickle_writer('results/pickle-{}.pkl'.format(stamp))

if __name__ == "__main__":
    pms = 2
    vms = 10
    s = Simulator()
    
    trace_file = 'planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_ yale_p4p'
    #pms_scenarios = [144] #range(10, 110, 10)
    #vms_scenarios = range(16, 304, 16)
    
    pms_scenarios = [72] #range(10, 110, 10)
    vms_scenarios = range(16, 160, 16)
    
    #pms_scenarios = range(20, 50, 10)
    #vms_scenarios = range(16, 64, 16)
    
    #strategy = EnergyUnawareStrategyPlacement()
    #s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)
    
    #strategy = OpenOptStrategyPlacement()
    #s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)

    strategy = EvolutionaryComputationStrategyPlacement()
    s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)
    
    vms = 10
    
# OpenOpt
#15793.08
#81
#19
#4.81501793861
#
# Inspyred
#15684.08
#80
#20
#37.2569041252
