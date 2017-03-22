#! /usr/bin/env ptython
# -*- coding: utf-8 -*-
"""
Data generation for GP.
Ernesto Costa, March 2012
Revised 1:  March 2014 (Python 3 version
Revision 2:  March 2015
Revision 3: March 2016
gen_data.py
"""

import matplotlib.pyplot as plt
import numpy as np
import os 

def data_creation(file_name,function,domain,numb_cases,*function_set):
    """
    domain = [...,(inf, sup),...], inf = starting value, sup = end value of each variable
    function_set = (...,(name_function, arity), ...)
    """
    with open(file_name,'w') as f_out:
        # Header
        header_base = str(len(domain)) + '\t' 
        header = header_base + ''.join([function_set[i][0] +'\t'+str(function_set[i][1])+'\t' for i in range(len(function_set))])[:-1] + '\n'
        f_out.write(header)
        
        # generate fitness cases
        cases = []
        for i in range(len(domain)):
            init = domain[i][0]
            end = domain[i][1]
            step = (end - init) / numb_cases
            data_x = np.arange(init,end,step)
            cases.append(data_x)
        inputs = list(zip(*cases))
        outputs = [function(*in_vector) for in_vector in inputs]
        # save to file
        for i in range(numb_cases):
            line = ''.join([str(val) + '\t' for val in inputs[i]]) + str(outputs[i]) + '\n'
            f_out.write(line)  
        f_out.close()


def plot_data(file_name, name,body,loc='best'):
    with open(file_name) as f_in:
        f_in = open(file_name)
        # read fitness cases
        data = f_in.readlines()[1:]
        f_in.close()
        # plot
        values_x = [float(line[:-1].split()[0]) for line in data]
        values_y = [float(line[:-1].split()[-1]) for line in data]
        plt.ylabel('Value')
        plt.xlabel('Input Values')
        plt.title(name)
        p = plt.plot(values_x,values_y,'r-o',label=str(body))
        plt.legend(loc= loc)
        plt.show()

  
def simbolic_regression_2(x):
    return x**2 + x + 1

def sphere(x,y):
    return x**2 + y**2

def sin_w(x):
    return np.sin(x)


def main_1():
    data_creation(prefix+'/data_sin.txt',sin_w,[(-3.14, 3.14)], 62, ('add_w',2),('sub_w',2), ('mult_w',2),('div_prot_w',2))
    plot_data(prefix+'/data_sin.txt','sin', 'sin(x)', 'upper right')
    
def main_2():
    data_creation(prefix+'/data_symb.txt',simbolic_regression_2,[(-1.0, 1.0)], 21, ('add_w',2),('sub_w',2), ('mult_w',2),('div_prot_w',2))
    plot_data(prefix+'/data_symb.txt','Symbolic Regression','x**2 + x + 1','lower right')

def main_3():
    data_creation(prefix+'/data_sphere.txt',sphere,[[-5,5],[-5,5]], 22, ('add_w',2),('sub_w',2), ('mult_w',2),('div_prot_w',2))
    plot_data(prefix+'/data_sphere.txt','Sphere','X**2 + Y**2', 'upper right')   
    
    
if __name__ == '__main__':
    # my file prefix
    prefix = os.path.dirname(os.path.realpath(__file__))
    #main_1()
    #main_2()
    main_3()
    
   

    
    
 