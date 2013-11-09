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
TraceAnalizer :: A VM trace analyzer
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


#from distsim.model.tracefilter import TraceFilter
import distsim.analysis.summarizedata as sd


if __name__ == "__main__":
    s = sd.SummarizeData('/home/afu/2013-sbrc-experiments/results')
    s.load_all('simulation-146-179_surfsnel_dsl_internl_net_root-EnergyUnawareStrategyPlacement-010-')
    print('done')
