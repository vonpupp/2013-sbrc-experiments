#!/usr/bin/env python
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
Trace Generator Model
"""
__version__ = "0.1"
__author__  = "Albert De La Fuente"


import collections
import numpy as np
import scipy.stats as stats
import csv


class TraceFilter():
    def __init__(self, fname):
        self.fname = fname
        self.file_in = open(fname)
        self.reader = csv.DictReader(self.file_in, delimiter='\t')
        fields = self.reader.fieldnames
        data = {}
        for line in self.reader:
            for field in fields:
                d = data.get(field)
                if not d:
                    try:
                        data[field] = [float(line[field])]
                    except:
                        data[field] = [str(line[field])]
                else:
                    try:
                        data[field].append(float(line[field]))
                    except:
                        data[field].append(str(line[field]))
        self.data = data

    def by_mean(self):
        column = self.data['std']
        print column
        min = np.amin(column)
        max = np.amax(column)
        mean = np.mean(column)
        print('min={}, max={}, mean={}'.format(min, max, mean))
