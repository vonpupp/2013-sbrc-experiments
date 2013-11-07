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
import glob
import os


class SummarizeData():
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.data = []
        self.summary_list = {}

    def summarize(self):
        self.summary_list = {}
        for simulation in self.data:
            for attribute in simulation.keys():
                self.summary_list[attribute] += [simulation[attribute]]
        print self.summary_list


    def load_file(self, fname):
        self.fname = fname
        self.file_in = open(fname)
        self.reader = csv.DictReader(self.file_in, delimiter='\t')
        buffer = []
        for row in self.reader:
            buffer += [row]
#        fields = self.reader.fieldnames
#        data = {}
#        for line in self.reader:
#            for field in fields:
#                d = data.get(field)
#                if not d:
#                    try:
#                        data[field] = [float(line[field])]
#                    except:
#                        data[field] = [str(line[field])]
#                else:
#                    try:
#                        data[field].append(float(line[field]))
#                    except:
#                        data[field].append(str(line[field]))
        self.data.append(buffer)
        print buffer
        self.summarize()

    def load_all(self, pattern):
        self.files = glob.glob(os.path.join(self.working_dir, pattern))
        self.files = sorted(self.files)
        for file in self.files:
            self.load_file(file)

    def csv_write(self):
        f = self.filtered_data.keys()
        print f
        self.fname = 'eggs.csv'
        self.file_out = open(self.fname, mode='w')
        self.writer = csv.DictWriter(self.file_out, fieldnames=f, delimiter='\t')

        for column in self.filtered_data.keys():
            inverted_item = {}
            for value in self.filtered_data[column]:
                inverted_item[column] = value
                print inverted_item
                self.writer.writerow(inverted_item)
