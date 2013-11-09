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


#import collections
import numpy as np
#import scipy.stats as stats
import csv
import glob
import os


class SummarizeData():
    def __init__(self, working_dir):
        self.working_dir = working_dir
#        self.simulation_counter = 0
        self.data = []
#        self.data[self.simulation_counter] = []
        self.summary_list = {}

    def remap_data(self):
        self.summary_list = []
        repetitions = len(self.data)
        scenarios = len(self.data[0])
        for scenario in range(scenarios):
            d = {}
            for id_repetition, repetition in enumerate(self.data):
                data = repetition[scenario]
#                for id_scenario, scenario in enumerate(repetition):
                #d = dict(l[id_scenario])
                for attribute in data.keys():
                    value = data[attribute]
                    try:
                        #obj = self.summary_list[attribute]
                        #TODO: Research on how to improve this part, smelly code
                        try:
                            d[attribute] += [float(value)]
                        except:
                            d[attribute] += [str(value)]
                    except:
                        try:
                            d[attribute] = [float(value)]
                        except:
                            d[attribute] = [str(value)]
            self.summary_list.append(d)
        print self.summary_list
        
    def map_column(self, scenario, column, selector):
        return selector(scenario[column])
        #return map(selector, l)
    
    def worst_best_medium(self, scenario, column, bselector, wselector, mselector):
        worst_case = self.worst_case[len(self.worst_case)-1]
        worst_case[column] = self.map_column(scenario, column, wselector)
        #self.worst_case += worst_case
        
        best_case = self.best_case[len(self.best_case)-1]
        best_case[column] = self.map_column(scenario, column, bselector)
        #self.best_case += best_case
        
        medium_case = self.medium_case[len(self.medium_case)-1]
        medium_case[column] = self.map_column(scenario, column, mselector)
        #self.medium_case += medium_case
        
        #self.best_case.append()[c] = self.map_column(scenario, column, bselector)
        #self.medium_case.append()[c] = self.map_column(scenario, column, mselector)
    
    def first_item(self, l):
        return l[0]
        
    def summarize_data(self):
        self.worst_case = []
        self.best_case = []
        self.medium_case = []
        for scenario in self.summary_list:
            self.worst_case.append({})
            self.best_case.append({})
            self.medium_case.append({})
            self.worst_best_medium(scenario, '#PM', min, max, np.mean)
            self.worst_best_medium(scenario, '#VM', max, min, np.mean)
            self.worst_best_medium(scenario, '#PM-U', max, min, np.mean)
            self.worst_best_medium(scenario, '#PM-S', max, min, np.mean)
            self.worst_best_medium(scenario, '#PM-I', min, max, np.mean)
            self.worst_best_medium(scenario, '#VM-P', max, min, np.mean)
            self.worst_best_medium(scenario, 'VM-U', min, max, np.mean)
            self.worst_best_medium(scenario, 'KW', min, max, np.mean)
            self.worst_best_medium(scenario, 'strategy', self.first_item, self.first_item, self.first_item)
            self.worst_best_medium(scenario, 'T', min, max, np.mean)

    def load_file(self, fname):
        self.fname = fname
        self.file_in = open(fname)
        self.reader = csv.DictReader(self.file_in, delimiter='\t')
        self.data.append([])
        simulation_counter = len(self.data)-1
        self.data[simulation_counter] = []
        for row in self.reader:
            self.data[simulation_counter] += [row]
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
        #self.data += [buffer]
        #self.simulation_counter += 1
        #print buffer

    def load_all(self, pattern):
        self.files = glob.glob(os.path.join(self.working_dir, pattern+'*.csv'))
        self.files = sorted(self.files)
        for file in self.files:
            self.load_file(file)
        self.remap_data()
        self.summarize_data()
        print 'ok'

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
