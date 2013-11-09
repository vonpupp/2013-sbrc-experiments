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
SummarizeData :: Data summarizer
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


#from distsim.model.tracefilter import TraceFilter
import distsim.analysis.summarizedata as sd
import distsim.analysis.csvloader as csvl
import distsim.analysis.plotdata as plot


def summarize_file(fname):
    s = sd.SummarizeData('/home/afu/2013-sbrc-experiments/results')
    best, worst, average = s.load_pm_scenario(fname)
    s.csv_write()

if __name__ == "__main__":
    #'planetlab-workload-traces/20110409/146-179_surfsnel_dsl_internl_net_root',
    #'planetlab-workload-traces/20110409/host4-plb_loria_fr_uw_oneswarm',
    #'planetlab-workload-traces/20110420/plgmu4_ite_gmu_edu_rnp_dcc_ufjf',
    #
    #'planetlab-workload-traces/20110309/planetlab1_fct_ualg_pt_root',
    #'planetlab-workload-traces/20110325/host3-plb_loria_fr_inria_omftest',
    #'planetlab-workload-traces/20110412/planetlab1_georgetown_edu_nus_proxaudio',
    #
    #'planetlab-workload-traces/20110306/planetlab1_dojima_wide_ad_jp_princeton_contdist',
    #'planetlab-workload-traces/planetlab-selected/planetlab-20110409-filtered_planetlab1_s3_kth_se_sics_peerialism',
    #'planetlab-workload-traces/20110322/planetlab-wifi-01_ipv6_lip6_fr_inria_omftest'
    #trace = '146-179_surfsnel_dsl_internl_net_root'
    #algorithm = 'EnergyUnawareStrategyPlacement'
    #scenario = '020'
    
    
    trace_scenarios = [
        '146-179_surfsnel_dsl_internl_net_root',
        #'host4-plb_loria_fr_uw_oneswarm',
        #'plgmu4_ite_gmu_edu_rnp_dcc_ufjf',
        #
        #'planetlab1_fct_ualg_pt_root',
        #'host3-plb_loria_fr_inria_omftest',
        #'planetlab1_georgetown_edu_nus_proxaudio',
        #
        #'planetlab1_dojima_wide_ad_jp_princeton_contdist',
        #'planetlab-20110409-filtered_planetlab1_s3_kth_se_sics_peerialism',
        #'planetlab-wifi-01_ipv6_lip6_fr_inria_omftest'
    ]
    algorithm_scenarios = [
        'EnergyUnawareStrategyPlacement',
        'OpenOptStrategyPlacement',
        'EvolutionaryComputationStrategyPlacement'
    ]
    host_scenarios = range(10, 110, 10)
    simulation_scenarios = range(1, 31)
    
    result_dir = '/home/afu/2013-sbrc-experiments/results'
    for trace in trace_scenarios:
        for host in host_scenarios:
            per_algoritm_summary = {}
            for algorithm in algorithm_scenarios:
                fname = 'simulation-' + trace + '-' + algorithm + '-' + str(host).zfill(3)
                print('processing {}...'.format(fname))
                d = sd.SummarizeData(result_dir)
                d.load_pm_scenario(fname)
                per_algoritm_summary[algorithm] = d
                d.csv_write()
            p = plot.GraphGenerator(per_algoritm_summary, result_dir)
            p.plot_all(host, trace)
        
    #fname = 'simulation-146-179_surfsnel_dsl_internl_net_root-EnergyUnawareStrategyPlacement-020'
    #summarize_file(fname)
    #
    #fname = 'simulation-146-179_surfsnel_dsl_internl_net_root-OpenOptStrategyPlacement-020'
    #summarize_file(fname)
    #
    #fname = 'simulation-146-179_surfsnel_dsl_internl_net_root-EvolutionaryComputationStrategyPlacement-020'
    #summarize_file(fname)
    
    #feu = 'simulation-146-179_surfsnel_dsl_internl_net_root-EnergyUnawareStrategyPlacement-020-best'
    #fksp = 'simulation-146-179_surfsnel_dsl_internl_net_root-OpenOptStrategyPlacement-020-best'
    #fec = 'simulation-146-179_surfsnel_dsl_internl_net_root-EvolutionaryComputationStrategyPlacement-020-best'
    #data_eu = csvl.CSVLoader(feu)
    #data_ksp = csvl.CSVLoader(fksp)
    #data_ec = csvl.CSVLoader(fec)
    #p = plot.GraphGenerator(data_eu, data_ksp, data_ec)
    #p.plot_all()
    #print('done')
