"""
Based on
stat_2016_alunos.py 
by Ernesto Costa

Adapted by Gonçalo Pereira
"""

import os.path
import re
from stat_lib import *

from argparse import ArgumentParser

def load_stats_file(filename):
    data_raw = np.loadtxt(filename, usecols=(1))
    return data_raw

def data_to_numpy(data1, data2):
    data = []
    for i in range(len(data1)):
        data.append([data1[i], data2[i]])
    return data

def print_describe_data(desc):
    basic = 'Min: %s\nMax: %s\nMean: %s\nMedian: %s\nMode: %s\nVar: %s\nStd: %s'
    other = '\nSkew: %s\nKurtosis: %s\nQ25: %s\nQ50: %s\nQ75: %s'
    all_ = basic + other
    print(all_ % (desc[0],desc[1],desc[2],desc[3],desc[4],desc[5],desc[6],desc[7],desc[8],desc[9],desc[10],desc[11]))

def is_a_directory(string_arg):
    if not os.path.isdir(string_arg):
        msg = "The given argument '%r' is not a directory!" % string_arg
        raise argparse.ArgumentTypeError(msg)
    return string_arg

def analyse_results(experiments, results):
    # results will be an array of numpy arrays
    #print(results)

    for i in range(len(experiments)):
        experiment = experiments[i]
        result = results[i]
        print("\n\nAnalysing experiment '{}' ...\n".format(experiment))
        print_describe_data(describe_data(result))

        print("\nKolgomorov-Smirnov: ")
        print(test_normal_ks(result))

        print("\nShapiro-Wilk: ")
        print(test_normal_sw(result))

        #print("Test of equal variance: ")
        #print(levene(data1))

        histogram_norm(result, experiment,'Fitness','Count' , bins=10)

    box_plot(results,experiments)

    # print("\nwilcoxon -> non parametric, two samples, dependent")
    # print(wilcoxon(data1,data2))

    # print("\nt_test_dep -> parametric, two samples, dependent")
    # print(t_test_dep(data1,data2))

if __name__ == '__main__':
    experiments = ['standard', 'self_adaptation', 'self_adaptation_2']
    experiments_files = [experiment + '.stats' for experiment in experiments]

    parser = ArgumentParser(
        description='Statistical analysis tool for function minimization solvers.'
    )
    parser.add_argument(    
        'experiments', type=is_a_directory,
        help='Directory where the experiments are. Will walk trees downwards executing in every leaf.')
    args = parser.parse_args()

    for dirpath, dirnames, filenames in os.walk(args.experiments):
        if not dirnames:
            # Test if the directory has the required *.stats files and they are not empty!
            files_are_present = [True for fname in experiments_files if fname in filenames and os.path.getsize(os.path.join(dirpath, fname)) > 0]
            files_are_present = len(files_are_present) == len(experiments_files)
            
            if files_are_present:
                # Read all statistics from all files
                results_values = [get_data(os.path.join(dirpath, fname)) for fname in experiments_files]
                # Analyse those results
                analyse_results(experiments, results_values)
