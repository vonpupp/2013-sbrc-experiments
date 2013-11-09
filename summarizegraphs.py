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
SummarizeGraphs :: A graphics summarization tool
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


#from distsim.model.tracefilter import TraceFilter
import distsim.analysis.csvloader as csvl
import distsim.analysis.plotdata as plot

def plot_files(feu, fksp, fec):
    path = '/home/afu/2013-sbrc-experiments/results'
    data_eu = csvl.CSVLoader(path + '/' + feu)
    data_ksp = csvl.CSVLoader(path + '/' + fksp)
    data_ec = csvl.CSVLoader(path + '/' + fec)
    l = [data_eu, data_ksp, data_ec]
    p = plot.GraphGenerator('/home/afu/2013-sbrc-experiments/results', l)
    p.plot_all()

if __name__ == "__main__":
    feu = 'simulation-146-179_surfsnel_dsl_internl_net_root-EnergyUnawareStrategyPlacement-020-best.csv'
    fksp = 'simulation-146-179_surfsnel_dsl_internl_net_root-OpenOptStrategyPlacement-020-best.csv'
    fec = 'simulation-146-179_surfsnel_dsl_internl_net_root-EvolutionaryComputationStrategyPlacement-020-best.csv'
    plot_files(feu, fksp, fec)
    #data_eu = csvl.CSVLoader(feu)
    #data_ksp = csvl.CSVLoader(fksp)
    #data_ec = csvl.CSVLoader(fec)
    #p = plot.GraphGenerator(data_eu, data_ksp, data_ec)
    #p.plot_all()
    print('done')
