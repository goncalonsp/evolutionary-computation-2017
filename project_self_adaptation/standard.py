"""
functions.py
Function optimization.
Based on Ernesto Costa's work, February 2016.
"""
__author__ = 'Gabriel Rodrigues & Gonçalo Pereira'
__date__ = 'May 2017'

from utils import *
from functions import *
from sea_float import *
import numpy as np

# Fitness
def merito(evaluate_func):
    def _merito(indiv):
        return evaluate_func(fenotipo(indiv))
    return _merito

def fenotipo(indiv):
    return indiv

if __name__ == '__main__':

    # ------------------------------------------- #
    # Note:                                       #
    # We are only studying minimization functions #
    # ------------------------------------------- #

    n_runs = 10
    fitness = merito(rastrigin_eval) # Parameter: Evaluation function
    dimensionality = 10
    n_generations = 250
    size_pop = 100
    domain = [ RASTRIGIN_DOMAIN for _ in range(dimensionality) ]
    prob_muta = 0.01
    sigma = [ 0.6 for _ in range(dimensionality) ] # The sigma values can be set individually like so: [0.5,0.8,1.0]. It must respect the dimensionality
    prob_cross = 0.9
    sel_parents = tour_sel(3) # Parameter: tournament size
    recombination = cross(0.3) # Parameter: alpha
    mutation = muta_float_gaussian
    sel_survivors = sel_survivors_elite(0.1) # Parameter: elite ratio

    """ Single run, console result, no statistics """
    # best_1 = sea_float(
    #     n_generations, 
    #     size_pop, 
    #     domain, 
    #     prob_muta, 
    #     sigma, 
    #     prob_cross, 
    #     sel_parents, 
    #     recombination, 
    #     mutation, 
    #     sel_survivors, 
    #     fitness
    # )

    # display(best_1, fenotipo)
    
    """ Single run, plot result, with statistics """
    # best_1, bests, average_pop = sea_for_plot(
    #     n_generations, 
    #     size_pop, 
    #     domain, 
    #     prob_muta, 
    #     sigma, 
    #     prob_cross, 
    #     sel_parents, 
    #     recombination, 
    #     mutation, 
    #     sel_survivors, 
    #     fitness
    # )

    # print(best_1)
    # display_stat_1(bests, average_pop)
    
    """ Multiple runs, plot results, with statistics """
    best_1, boa, best_average = run (
        n_runs,
        n_generations, 
        size_pop,
        domain,
        prob_muta,
        sigma,
        prob_cross,
        sel_parents,
        recombination,
        mutation,
        sel_survivors, 
        fitness
    )

    display(best_1, fenotipo)
    display_stat_n(boa, best_average)