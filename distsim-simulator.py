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
2013 SBRC Simulations
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


import argparse
import os

def get_default_arg(default_value, arg):
    if arg is None:
        return default_value
    else:
        return arg

if __name__ == "__main__":
    seu = 1
    sksp = 1
    sec = 1

    eu_params = ''
    ksp_params = ''
    ec_params = ''
    if seu == 1:
        eu_params = '-seu 1'
    if sksp == 1:
        ksp_params = '-sksp 1'
    if sec == 1:
        ec_params = '-sec 1'

    trace_scenarios = [
        'planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root',
        'planetlab-workload-traces/20110409/host4-plb_loria_fr_uw_oneswarm',
        'planetlab-workload-traces/20110420/plgmu4_ite_gmu_edu_rnp_dcc_ufjf',

        'planetlab-workload-traces/20110309/planetlab1_fct_ualg_pt_root',
        'planetlab-workload-traces/20110325/host3-plb_loria_fr_inria_omftest',
        'planetlab-workload-traces/20110412/planetlab1_georgetown_edu_nus_proxaudio',

        'planetlab-workload-traces/20110306/planetlab1_dojima_wide_ad_jp_princeton_contdist',
        'planetlab-workload-traces/planetlab-selected/planetlab-20110409-filtered_planetlab1_s3_kth_se_sics_peerialism',
        'planetlab-workload-traces/20110322/planetlab-wifi-01_ipv6_lip6_fr_inria_omftest'
    ]

    host_scenarios = range(10, 110, 10)
    simulation_scenarios = range(1, 31)

    for trace in trace_scenarios:
        for host in host_scenarios:
            for simulation in simulation_scenarios:
                command = 'python distsim.py -t {} -o {} -pm {} -vma 16 -vmo 304 -vme 16 {} {} {}'\
                        .format(trace, 'results', host, eu_params, ksp_params, ec_params)
                os.system(command)
                
            #for algorithm...
            #    sumarize trace
                
    # ./ distsim.py -h 72 -vma 16 -vmo 304 -vme 16
    #   -t planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_ yale_p4p
    #   -o results/72-bla
    # ./ simuplot.py
#    parser = argparse.ArgumentParser(description='A VM distribution/placement simulator.')
#    parser.add_argument('-pm', '--pmcount', help='Number of physical machines', required=False)
#    parser.add_argument('-vma', '--vmstart', help='Start number of VMs (def: 16)', required=False)
#    parser.add_argument('-vmo', '--vmstop', help='Stop number of VMs (def: 304)', required=False)
#    parser.add_argument('-vme', '--vmstep', help='Increment step number of VMs (def: 16)', required=False)
#    parser.add_argument('-t', '--vmtrace', help='Full path to trace file', required=True)
#    parser.add_argument('-o', '--output', help='Output path', required=True)
#    parser.add_argument('-seu', '--simeu', help='Simulate Energy Unaware', required=False)
#    parser.add_argument('-sksp', '--simksp', help='Simulate Iterated-KSP', required=False)
#    parser.add_argument('-sec', '--simec', help='Simulate Iterated-EC', required=False)
#    args = parser.parse_args()

#    pmcount = int(get_default_arg(72, args.pmcount))
#    vmstart = int(get_default_arg(16, args.vmstart))
#    vmstop = int(get_default_arg(304, args.vmstop))
#    vmstep = int(get_default_arg(16, args.vmstep))
#    trace_file = get_default_arg('planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_yale_p4p', args.vmtrace)
#    output_path = get_default_arg('results/path', args.output)
#    simulate_eu = bool(get_default_arg(0, args.simeu))
#    simulate_ksp = bool(get_default_arg(0, args.simksp))
#    simulate_ec = bool(get_default_arg(0, args.simec))

#    s = Simulator()

#    pms_scenarios = [pmcount]
#    vms_scenarios = range(vmstart, vmstop, vmstep)

    #pms_scenarios = range(20, 50, 10)
    #vms_scenarios = range(16, 64, 16)

#    if simulate_eu:
#        from distsim.strategies.energyunaware import EnergyUnawareStrategyPlacement
#        strategy = EnergyUnawareStrategyPlacement()
#        s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)

#    if simulate_ksp:
#        from distsim.strategies.iteratedksp import OpenOptStrategyPlacement
#        strategy = OpenOptStrategyPlacement()
#        s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)

#    if simulate_ec:
#        from distsim.strategies.iteratedec import EvolutionaryComputationStrategyPlacement
#        strategy = EvolutionaryComputationStrategyPlacement()
#        s.simulate_strategy(strategy, trace_file, pms_scenarios, vms_scenarios)

    print('done')
