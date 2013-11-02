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
    def __init__(self, result_dir, pms_scenarios):
        self. result_dir = result_dir
        self.pms_scenarios = pms_scenarios
        self.file_list = []

    def get_experiments_file(self, scenario, patter='*'):
        self.file = None
        pattern = '{}-{}-*.csv'.format(patter, str(scenario))
        for file in os.listdir(dir):
            if fnmatch.fnmatch(file, pattern) and file not in self.file_list:
                self.file = file
        return self.file

    def load_csv_data(self, filename):
        self.data_file = open(self.result_dir + '/' + filename, 'rb')
        reader = csv.reader(self.data_file, delimiter='\t')
        reader.next()
        result = {}
        #physical_machines_count = []
        #virtual_machines_count = []
        result['physical_mahines_count'] = []
        result['virtual_mahines_count'] = []
        result['physical_machines_used'] = []
        result['physical_machines_suspended'] = []
        result['physical_machines_idle'] = []
        result['virtual_machines_placed'] = []
        result['virtual_machines_unplaced'] = []
        result['energy_consumed'] = []
        result['strategy'] = []
        result['start_time'] = []
        result['end_time'] = []
        result['elapsed_time'] = []
        for row in reader:
            #physical_machines_count.append(row[0])
            #virtual_machines_count.append(row[1])
            result['physical_mahines_count'].append(int(row[0]))
            result['virtual_mahines_count'].append(int(row[1]))
            result['physical_machines_used'].append(int(row[2]))
            result['physical_machines_suspended'].append(int(row[3]))
            result['physical_machines_idle'].append(int(row[4]))
            result['virtual_machines_placed'].append(int(row[5]))
            result['virtual_machines_unplaced'].append(int(row[6]))
            result['energy_consumed'].append(float(row[7]))
            result['strategy'].append(row[8])
            result['elapsed_time'].append(float(row[9]))
        return result

    def legend(self, title):
        trans = {}
        trans['EnergyUnawareStrategyPlacement'] = 'Energy unaware'
        trans['OpenOptStrategyPlacement'] = 'Iterated-KSP'
        trans['EvolutionaryComputationStrategyPlacement'] = 'Iterated-EC'
        return trans[title]

    def vms_ticks(self, vms):
        result = ['{0:03d}'.format(i) for i in vms]
        return result


    def save_fig(self, scenario, data_ref, data1, data2, x_aspect, y_aspect, x_title, y_title, title):
        #x1 = data_ref['physical_mahines_count']
        ##x1 = data_ref['virtual_mahines_count']
        #y1 = data_ref['virtual_machines_unplaced']
        #y2 = data_ref['virtual_machines_placed']
        #
        #x2 = data_ref['virtual_machines_placed']
        #
        #y3 = data_ref['physical_mahines_count']
        #y3 = data_ref['energy_consumed']
        
        #fig = plt.figure()            
        #plt.subplot(1,2,1)
        #plt.plot(x, y, 'r--')
        #plt.subplot(1,2,2)
        #plt.plot(y, x, 'g*-');
        #
        #fig.ax.set_xlabel("x")
        #fig.ax.set_ylabel("y")
        #fig.ax.set_title("title")

        #fig, ax = plt.subplots()
        #plt.subplot(2, 1, 1)
        #plt.grid(True)
        ##plt.fill(x1, y1, 'yo-', x1, y2, 'r', alpha=0.3)
        #plt.plot(x1, y1a, 'yo-', x1, y1b, 'r')
        ##plt.plot(x1, y1, 'yo-')
        #plt.title('Number of physical machines: {}'.format(scenario))
        #plt.ylabel('Damped oscillation')
        
        #plt.subplot(2, 1, 2
        
        x2 = data_ref[x_aspect]
        y2a = data_ref[y_aspect]
        y2b = data1[y_aspect]
        y2c = data2[y_aspect]
        
        fig, ax = plt.subplots()
        ax.plot(x2, y2a, color='red', ls='-', marker='.', label=self.legend(data_ref['strategy'][0]))
        ax.plot(x2, y2b, color='blue', ls='-', marker='o', label=self.legend(data1['strategy'][0]))
        ax.plot(x2, y2c, color='green', ls='-', marker='s', label=self.legend(data2['strategy'][0]))
        #ax.fill(y2a, y2b, alpha=0.3)
        ax.set_xlabel(x_title, fontsize=18)
        ax.set_ylabel(y_title, fontsize=18)
        ax.set_title(title + '(' + str(scenario) + ' hosts )')
        #ax.legend(loc=2); # upper left corner
        ax.xaxis.set_ticks(x2)
        pylab.xticks(x2, self.vms_ticks(x2), rotation='vertical', verticalalignment='top')
        
        
        #x = arange(0, 2, 0.01)
        #y1 = sin(2*pi*x)
        #y2 = sin(4*pi*x) + 2
        ax = fig.gca()

        p = fill_between(ax, x2, y2a, y2b, facecolor='g')
        p.set_alpha(0.2)
        
        p = fill_between(ax, x2, y2b, y2c, facecolor='b')
        p.set_alpha(0.2)
        
        #plt.gca().ax.locator_params(axis='y',nbins=len(y2a))
        #formatter = plt.gca().get_xaxis().get_major_formatter()
        #plt.gca().set_minor_formatter(formatter)
        
        #ax.yaxis.grid(True, which='major')
        #ax.yaxis.grid(True, which='minor')
        #ax.grid(True, which='both')
        #ax.grid(True)
        plt.grid(True)
        box = ax.get_position()
        #ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax.set_position([box.x0, box.y0 + box.height * 0.2,
            box.width, box.height * 0.8])

        # Put a legend below current axis
        #ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=False, ncol=5)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
            fancybox=True, shadow=False, ncol=5)
        
        plt.savefig(self.result_dir + '/' + str(scenario) + '-' +
            title + '.png')
        #return plt.savefig(self.result_dir + '/' + str(scenario) +
        #                   x_title + ' vs ' + y_title + '.png')

    def create_comparison_graph(self):
        for scenario in self.pms_scenarios:
            reference = self.get_experiments_file(scenario, 'EnergyUnaware*')
            method1 = self.get_experiments_file(scenario, 'OpenOpt*')
            method2 = self.get_experiments_file(scenario, 'EvolutionaryComputation*')
            data_ref = self.load_csv_data(reference)
            data1 = self.load_csv_data(method1)
            data2 = self.load_csv_data(method2)
            
            x1 = data_ref['virtual_mahines_count']
            y1a = data_ref['virtual_machines_placed']
            y1b = data1['virtual_machines_unplaced']
            
            x2 = data_ref['virtual_mahines_count']
            y2a = data_ref['energy_consumed']
            y2b = data1['energy_consumed']
            y2c = data2['energy_consumed']
            #x_title = 'Number of VMs'
            #y_title = 'Energy consumed (Watts)'
            #title = 'Energy consumption comparison'
            self.save_fig(scenario, data_ref, data1, data2,
                'virtual_mahines_count', 'energy_consumed',
                'Number of VMs', 'Energy consumed (Watts)',
                'Energy consumption comparison')
            
            self.save_fig(scenario, data_ref, data1, data2,
                'virtual_mahines_count', 'elapsed_time',
                'Number of VMs', 'Time (seconds)',
                'Time comparison')
            
            self.save_fig(scenario, data_ref, data1, data2,
                'virtual_mahines_count', 'physical_machines_used',
                'Number of VMs', 'No. physical machines used',
                'Used physical machines comparison')
            
            self.save_fig(scenario, data_ref, data1, data2,
                'virtual_mahines_count', 'physical_machines_suspended',
                'Number of VMs', 'No. physical machines suspended',
                'Suspended physical machines comparison')
            
            self.save_fig(scenario, data_ref, data1, data2,
                'virtual_mahines_count', 'physical_machines_idle',
                'Number of VMs', 'No. physical machines idle',
                'Idle physical machines comparison')
            
            self.save_fig(scenario, data_ref, data1, data2,
                'virtual_mahines_count', 'virtual_machines_placed',
                'Number of VMs', 'No. virtual machines placed',
                'Placed VMs comparison')
            
            self.save_fig(scenario, data_ref, data1, data2,
                'virtual_mahines_count', 'virtual_machines_unplaced',
                'Number of VMs', 'No. virtual machines not placed',
                'Unplaced VMs comparison')
            
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
            
            #plt.show()
            #subplot(1,2,2)
            #plot(y, x, 'g*-');
#        method2 = self.get_experiments_files('EnergyUnaware*')

if __name__ == '__main__':
    gg = GraphGenerator(dir, pms_scenarios)
    gg.create_comparison_graph()

