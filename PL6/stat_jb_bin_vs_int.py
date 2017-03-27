"""
Based on
stat_2016_alunos.py

"""

from stat_alunos import *
import sys
import os.path
import re

def load_jb_runs_out(filename):
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

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " JBRUNS_BIN_OUT JBRUNS_INT_OUT")
        sys.exit(1)

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    
    data1 = load_jb_runs_out(filename1)
    data2 = load_jb_runs_out(filename2)

    print("------- Binary data: -------")
    print_describe_data(describe_data(data1))

    print("\nKolgomorov-Smirnov: ")
    print(test_normal_ks(data1))
    
    print("\nShapiro-Wilk: ")
    print(test_normal_sw(data1))
    
    #print("Test of equal variance: ")
    #print(levene(data1))

    print("\n------- Integer data: -------")
    print_describe_data(describe_data(data2))

    print("\nKolgomorov-Smirnov: ")
    print(test_normal_ks(data2))
    
    print("\nShapiro-Wilk: ")
    print(test_normal_sw(data2))
    
    #print("Test of equal variance: ")
    #print(levene(data2))

    histogram(data1, 'Binary Representation', 'Fitness', 'Count' , bins=10)
    histogram_norm(data1, 'Binary Representation','Fitness','Count' )

    histogram(data2, 'Integer Representation','Fitness','Count' )
    histogram_norm(data2, 'Integer Representation','Fitness','Count' )

    box_plot([data1,data2],['Binary','Integer'])

    print("\nwilcoxon -> non parametric, two samples, dependent")
    print(wilcoxon(data1,data2))

    print("\nt_test_dep -> parametric, two samples, dependent")
    print(t_test_dep(data1,data2))
