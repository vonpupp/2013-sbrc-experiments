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
import scipy as sp
import scipy.stats
#import scipy.stats as stats
import csv
import glob
import os

class SummarizeData():
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.data = []
        self.summary_list = {}

    def remap_data(self):
        self.summary_list = []
        repetitions = len(self.data)
        scenarios = len(self.data[0])
        for scenario in range(scenarios):
            d = {}
            for id_repetition, repetition in enumerate(self.data):
                data = repetition[scenario]
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
        #print self.summary_list
    
    def get_vms_scenarios(self):
        self.vms_scenarios = []
        for vms in self.summary_list:
            self.vms_scenarios += [int(vms['#VM'][0])]
    
    def map_column(self, scenario, column, selector):
        return selector(scenario[column])
        #return map(selector, l)
    
    def worst_best_medium(self, scenario, column, bselector, wselector, mselector):
        worst_case = self.worst_case[len(self.worst_case)-1]
        worst_case[column] = self.map_column(scenario, column, wselector)
        #test = scipy.stats.norm.interval(0.95, loc=mean, scale=std)
        try:
            worst_case[column + '-95'] = np.percentile(scenario[column], 95)
        except:
            worst_case[column + '-95'] = 0
        
        best_case = self.best_case[len(self.best_case)-1]
        best_case[column] = self.map_column(scenario, column, bselector)
        try:
            best_case[column + '-95'] = np.percentile(scenario[column], 95)
        except:
            best_case[column + '-95'] = 0
        
        average_case = self.average_case[len(self.average_case)-1]
        average_case[column] = self.map_column(scenario, column, mselector)
        try:
            average_case[column + '-95'] = np.percentile(scenario[column], 95)
        except:
            average_case[column + '-95'] = 0
    
    def first_item(self, l):
        return l[0]
        
    def summarize_attributes(self):
        self.worst_case = []
        self.best_case = []
        self.average_case = []
        for scenario in self.summary_list:
            self.worst_case.append({})
            self.best_case.append({})
            self.average_case.append({})
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
        self.file_in = open(fname, mode='r')
        self.reader = csv.DictReader(self.file_in, delimiter='\t', quoting=csv.QUOTE_NONE)
        self.data.append([])
        simulation_counter = len(self.data)-1
        self.data[simulation_counter] = []
        for row in self.reader:
            self.data[simulation_counter] += [row]

    def load_pm_scenario(self, pattern):
        self.pattern = pattern
        self.files = glob.glob(os.path.join(self.working_dir, pattern+'*.csv'))
        self.files = sorted(self.files)
        for file in self.files:
            self.load_file(file)
        self.remap_data()
        self.summarize_attributes()
        self.get_vms_scenarios()
        return self.best_case, self.worst_case, self.average_case
        #print 'ok'
        
    def summarize_trace(self, trace_file):
        pass

    def csv_write_summary(self, fname, fields, summarized_data):
        self.fname = fname
        self.file_out = open(self.fname, mode='w')
        self.writer = csv.DictWriter(self.file_out, fieldnames=fields, delimiter='\t', quoting=csv.QUOTE_NONE)
        
        headers = dict((n,n) for n in fields)
        self.writer.writerow(headers)
        for scenario in summarized_data:
            d = dict((k, str(v)) for k, v in scenario.items())
            self.writer.writerow(d)
        self.file_out.close()

    def csv_write(self):
        fields = self.best_case[0].keys()
        
        data = self.best_case
        fname = os.path.join(self.working_dir, self.pattern + '-best.csv')
        self.csv_write_summary(fname, fields, data)
        
        data = self.worst_case
        fname = os.path.join(self.working_dir, self.pattern + '-worst.csv')
        self.csv_write_summary(fname, fields, data)
        
        data = self.average_case
        fname = os.path.join(self.working_dir, self.pattern + '-average.csv')
        self.csv_write_summary(fname, fields, data)