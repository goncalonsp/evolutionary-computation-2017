"""
functions.py
Examples for function optimizattion.
Ernesto Costa, February 2016
"""

__author__ = 'Ernesto Costa'
__date__ = 'February 2016'


from utils import *
from sea_float import *
import numpy as np


# Fitness
def merito(indiv):
    return evaluate(fenotipo(indiv))

def fenotipo(indiv):
    return indiv


def evaluate(x):
    """Rastrigin: Rely on numpy arrays."""
    A = 10
    w = np.array(x)
    y = A*len(w)+sum( (w**2 - A* np.cos(2*np.pi*w)) )
    return y



if __name__ == '__main__':
    """WARNING: you should adapt to your case!!!"""
    prefix = '/Users/ernestojfcosta/tmp/'
    domain = [[-5.12,5.12],[-5.12,5.12], [-5.12,5.12]]
    sigma = [0.5,0.8,1.0]

    #best_1 = sea_float(250, 100,domain,0.01,sigma,0.9,tour_sel(3),cross(0.3),muta_float_gaussian,sel_survivors_elite(0.1), merito)
    #display(best_1,fenotipo)
    
    #best_1,best,average_pop = sea_for_plot(250, 100,domain,0.33,sigma,0.9,tour_sel(3),cross(0.5),muta_float_gaussian,sel_survivors_elite(0.1), merito)
    #display_stat_1(best,average_pop)
    #print(best_1)
    
    #boa,best_average = run(10,250, 100,domain,0.01,sigma,0.9,tour_sel(3),cross(0.3),muta_float_gaussian,sel_survivors_elite(0.1), merito)
    #######sea_for_plot(numb_generations,size_pop, domain, prob_mut,sigma,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func)
    boa,best_average = run(10,250, 100,domain,0.1,sigma,0.9,tour_sel(3),cross(0.5),muta_float_gaussian,sel_survivors_elite(0.05), merito)
    display(boa,fenotipo)
    print(min(boa))
    display_stat_n(boa,best_average)