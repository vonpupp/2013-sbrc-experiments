#!/usr/bin/python
# vim:ts=4:sts=4:sw=4:et:wrap:ai:fileencoding=utf-8:

import fnmatch
import os
import csv
import matplotlib.pyplot as plt
from matplotlib import pylab 
#from matplotlib.font_manager import FontProperties
from matplotlib.patches import Polygon

dir = 'results'
pms_scenarios = [72] #range(10, 110, 10)


def fill_between(ax, x, y1, y2, **kwargs):
    # add x,y2 in reverse order for proper polygon filling
    verts = zip(x,y1) + [(x[i], y2[i]) for i in range(len(x)-1,-1,-1)]
    poly = Polygon(verts, **kwargs)
    ax.add_patch(poly)
    ax.autoscale_view()
    return poly

class GraphGenerator:
    def __init__(self, data, result_dir):
        self.data = data
        self.result_dir = result_dir
        self.vms_scenarios = self.data.itervalues().next().vms_scenarios
        self.file_list = []

    #def get_experiments_file(self, scenario, patter='*'):
    #    self.file = None
    #    pattern = '{}-{}-*.csv'.format(patter, str(scenario))
    #    for file in os.listdir(dir):
    #        if fnmatch.fnmatch(file, pattern) and file not in self.file_list:
    #            self.file = file
    #    return self.file

    def legend(self, title):
        trans = {}
        trans['EnergyUnawareStrategyPlacement'] = 'Energy unaware'
        trans['OpenOptStrategyPlacement'] = 'Iterated-KSP'
        trans['EvolutionaryComputationStrategyPlacement'] = 'Iterated-EC'
        return trans[title]

    def vms_ticks(self, vms):
        result = ['{0:03d}'.format(i) for i in vms]
        return result


    def save_fig(self, hosts_scenario, trace_file, case,
                 data_ref, data1, data2,
                 x_aspect, y_aspect,
                 x_title, y_title, title):
        x2 = map(int, self.remap_data(data_ref, x_aspect))
        y2a = self.remap_data(data_ref, y_aspect)
        y2b = self.remap_data(data1, y_aspect)
        y2c = self.remap_data(data2, y_aspect)
        
        #x2 = data_ref[x_aspect]
        #y2a = data_ref[y_aspect]
        #y2b = data1[y_aspect]
        #y2c = data2[y_aspect]
        
        fig, ax = plt.subplots()
        #self.remap_data(data_ref, 'strategy')
        ax.plot(x2, y2a, color='red', ls='-', marker='.', label=self.legend(data_ref[0]['strategy']))
        ax.plot(x2, y2b, color='blue', ls='-', marker='o', label=self.legend(data1[0]['strategy']))
        ax.plot(x2, y2c, color='green', ls='-', marker='s', label=self.legend(data2[0]['strategy']))
        #ax.fill(y2a, y2b, alpha=0.3)
        ax.set_xlabel(x_title, fontsize=18)
        ax.set_ylabel(y_title, fontsize=18)
        ax.set_title(title + ' (' + str(hosts_scenario) + ' hosts)')
        #ax.legend(loc=2); # upper left corner
        ax.xaxis.set_ticks(x2)
        pylab.xticks(x2, self.vms_ticks(x2), rotation='vertical', verticalalignment='top')
        
        ax = fig.gca()

        p = fill_between(ax, x2, y2a, y2b, facecolor='g')
        p.set_alpha(0.2)
        
        p = fill_between(ax, x2, y2b, y2c, facecolor='b')
        p.set_alpha(0.2)
        
        plt.grid(True)
        box = ax.get_position()
        #ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax.set_position([box.x0, box.y0 + box.height * 0.2,
            box.width, box.height * 0.8])

        # Put a legend below current axis
        #ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=False, ncol=5)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=False, ncol=5)
        
        plt.savefig(self.result_dir + '/figure-' + trace_file +
            str(hosts_scenario).zfill(3) + '-' +
            case + '-' + title + '.png')
        #return plt.savefig(self.result_dir + '/' + str(scenario) +
        #                   x_title + ' vs ' + y_title + '.png')
    
    def save_fig_cases(self):
        self.save_fig(
            self.hosts_scenario,
            self.trace_file,
            'best',
            self.data_eu.best_case,
            self.data_ksp.best_case,
            self.data_ec.best_case,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
            )
        
        self.save_fig(
            self.hosts_scenario,
            self.trace_file,
            'worst',
            self.data_eu.worst_case,
            self.data_ksp.worst_case,
            self.data_ec.worst_case,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
            )
                
        self.save_fig(
            self.hosts_scenario,
            self.trace_file,
            'average',
            self.data_eu.average_case,
            self.data_ksp.average_case,
            self.data_ec.average_case,
            self.x_key, self.y_key,
            self.x_title, self.y_title,
            self.title,
            )
    
    def remap_data(self, list_dict, key):
        l = {}
        for item in list_dict:
            try:
                l += [item[key]]
            except:
                l = [item[key]]
        return l
        
    def plot_all(self, hosts_scenario, trace_file):
        #reference = self.get_experiments_file(scenario, 'EnergyUnawareStrategyPlacement')
        #method1 = self.get_experiments_file(scenario, 'OpenOptStrategyPlacement')
        #method2 = self.get_experiments_file(scenario, 'EvolutionaryComputationStrategyPlacement')
        #data_ref = self.load_csv_data(reference)
        #data1 = self.load_csv_data(method1)
        #data2 = self.load_csv_data(method2)
        #
        #x1 = data_ref['virtual_mahines_count']
        #y1a = data_ref['virtual_machines_placed']
        #y1b = data1['virtual_machines_unplaced']
        
        self.hosts_scenario = hosts_scenario
        self.trace_file = trace_file
        
        self.data_eu = self.data['EnergyUnawareStrategyPlacement']
        self.data_ksp = self.data['OpenOptStrategyPlacement']
        self.data_ec = self.data['EvolutionaryComputationStrategyPlacement']
        
        self.x_key = '#VM'
        self.y_key = 'KW'
        self.x_title = 'Number of VMs'
        self.y_title = 'Energy consumed (Watts)',
        self.title = 'Energy consumption comparison'
        
        self.save_fig_cases()

        self.x_key = '#VM'
        self.y_key = 'T'
        self.x_title = 'Number of VMs'
        self.y_title = 'Time (seconds)',
        self.title = 'Time comparison'
        
        self.save_fig_cases()
        
        #x2 = self.vms_scenarios
        
        #y2a = self.remap_data(data_eu.average_case, 'KW')
        #y2b = self.remap_data(data_ksp.average_case, 'KW')
        #y2c = self.remap_data(data_ec.average_case, 'KW')
        #self.save_fig(
        #    hosts_scenario,
        #    trace_file,
        #    'best',
        #    data_eu.best_case,
        #    data_ksp.best_case,
        #    data_ec.best_case,
        #    '#VM', 'KW',
        #    'Number of VMs', 'Energy consumed (Watts)',
        #    'Energy consumption comparison',
        #    )
        #
        #self.save_fig(
        #    hosts_scenario,
        #    trace_file,
        #    'worst',
        #    data_eu.worst_case,
        #    data_ksp.worst_case,
        #    data_ec.worst_case,
        #    '#VM', 'KW',
        #    'Number of VMs', 'Energy consumed (Watts)',
        #    'Energy consumption comparison',
        #    )
        #        
        #self.save_fig(
        #    hosts_scenario,
        #    trace_file,
        #    'average',
        #    data_eu.average_case,
        #    data_ksp.average_case,
        #    data_ec.average_case,
        #    '#VM', 'KW',
        #    'Number of VMs', 'Energy consumed (Watts)',
        #    'Energy consumption comparison',
        #    )
        #
        #self.save_fig(scenario, data_ref, data1, data2,
        #    'virtual_mahines_count', 'physical_machines_used',
        #    'Number of VMs', 'No. physical machines used',
        #    'Used physical machines comparison')
        #
        #self.save_fig(scenario, data_ref, data1, data2,
        #    'virtual_mahines_count', 'physical_machines_suspended',
        #    'Number of VMs', 'No. physical machines suspended',
        #    'Suspended physical machines comparison')
        #
        #self.save_fig(scenario, data_ref, data1, data2,
        #    'virtual_mahines_count', 'physical_machines_idle',
        #    'Number of VMs', 'No. physical machines idle',
        #    'Idle physical machines comparison')
        #
        #self.save_fig(scenario, data_ref, data1, data2,
        #    'virtual_mahines_count', 'virtual_machines_placed',
        #    'Number of VMs', 'No. virtual machines placed',
        #    'Placed VMs comparison')
        #
        #self.save_fig(scenario, data_ref, data1, data2,
        #    'virtual_mahines_count', 'virtual_machines_unplaced',
        #    'Number of VMs', 'No. virtual machines not placed',
        #    'Unplaced VMs comparison')
        
        #result['physical_mahines_count'].append(int(row[0]))
        #result['virtual_mahines_count'].append(int(row[1]))
        #result['physical_machines_used'].append(int(row[2]))
        #result['physical_machines_suspended'].append(int(row[3]))
        #result['physical_machines_idle'].append(int(row[4]))
        #result['virtual_machines_placed'].append(int(row[5]))
        #result['virtual_machines_unplaced'].append(int(row[6]))
        #result['energy_consumed'].append(float(row[7]))
        #result['strategy'].append(row[8])
        #result['elapsed_time'].append(float(row[9]))
        
#        method2 = self.get_experiments_files('EnergyUnaware*')

if __name__ == '__main__':
    gg = GraphGenerator(dir, pms_scenarios)
    gg.create_comparison_graph()

