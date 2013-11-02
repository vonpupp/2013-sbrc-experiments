#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:
#
# Copyright 2013 Albert De La Fuente
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Distsim :: A VM distribution simulator
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


#import distsim.model.tracegen as tracegen
from distsim.model.simulator import Simulator
from distsim.strategies.energyunaware import EnergyUnawareStrategyPlacement
from distsim.strategies.iteratedksp import OpenOptStrategyPlacement
from distsim.strategies.iteratedec import EvolutionaryComputationStrategyPlacement
import time
from functools import wraps

#PROF_DATA = {}
#
#def profile(fn):
#    @wraps(fn)
#    def with_profiling(*args, **kwargs):
#        start_time = time.time()
#
#        ret = fn(*args, **kwargs)
#
#        elapsed_time = time.time() - start_time
#
#        if fn.__name__ not in PROF_DATA:
#            PROF_DATA[fn.__name__] = [0, []]
#        PROF_DATA[fn.__name__][0] += 1
#        PROF_DATA[fn.__name__][1].append(elapsed_time)
#
#        return ret
#
#    return with_profiling
#
#def print_prof_data():
#    for fname, data in PROF_DATA.items():
#        max_time = max(data[1])
#        avg_time = sum(data[1]) / len(data[1])
#        print "Function %s called %d times. " % (fname, data[0]),
#        print 'Execution time max: %.3f, average: %.3f' % (max_time, avg_time)
#
#def clear_prof_data():
#    global PROF_DATA
#    PROF_DATA = {}


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
    
    strategy = EnergyUnawareStrategyPlacement()
    s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)
    
    strategy = OpenOptStrategyPlacement()
    s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)

    strategy = EvolutionaryComputationStrategyPlacement()
    s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)
    
    print('done')