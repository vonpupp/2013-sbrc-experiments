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


from distsim.managers.simmanager import Simulator
from distsim.model.traceanalize import TraceAnalize
import argparse


def get_default_arg(default_value, arg):
    if arg is None:
        return default_value
    else:
        return arg

if __name__ == "__main__":
    ta = TraceAnalize('planetlab-workload-traces/merkur_planetlab_haw-hamburg_de_yale_p4p')
    data = ta.analyze()
    print data

#    if not os.path.exists(output_path):
#        os.makedirs(output_path)
    print('done')
