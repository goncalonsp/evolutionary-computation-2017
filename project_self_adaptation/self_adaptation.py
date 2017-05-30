"""
functions.py
Function optimization.
Based on Ernesto Costa's work, February 2016.
"""
__author__ = 'Gabriel Rodrigues & Gonçalo Pereira'
__date__ = 'May 2017'

from utils import *
from functions import *
from self_adapted_ea_float import *
import numpy as np

# Fitness
def merito(evaluate_func):
    def _merito(cromo):
        value_cromo = [gene[0] for gene in cromo]
        return evaluate_func(fenotipo(value_cromo))
    return _merito

def fenotipo(cromo):
    return cromo

if __name__ == '__main__':

    # ------------------------------------------- #
    # Note:                                       #
    # We are only studying minimization functions #
    # We are self adapting the value 'sigma'      #
    # ------------------------------------------- #

    n_runs = 10
    fitness = merito(de_jong_f4_eval) # Parameter: Evaluation function
    dimensionality = 10
    n_generations = 100
    size_pop = 100
    domain = [ RASTRIGIN_DOMAIN for _ in range(dimensionality) ]
    prob_muta = 0.01
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
    #     prob_cross, 
    #     sel_parents, 
    #     recombination, 
    #     mutation, 
    #     sel_survivors, 
    #     fitness
    # )

    # display(best_1, fenotipo)
    
    """ Single run, plot result, with statistics """
    # best_1, bests, average_pop, bests_sigma, average_sigma = sea_for_plot(
    #     n_generations, 
    #     size_pop, 
    #     domain, 
    #     prob_muta, 
    #     prob_cross, 
    #     sel_parents, 
    #     recombination, 
    #     mutation, 
    #     sel_survivors, 
    #     fitness
    # )
    # print("Best:")
    # print(best_1)
    # display_stat_1(bests, average_pop)
    # display_stat_1(bests_sigma, average_sigma, title='Evolution of sigma over generations', ylabel='Sigma')
    
    """ Multiple runs, plot results, with statistics """
    best_1, boa, bests_average, boa_sigma, bests_sigma_average = run (
        n_runs,
        n_generations, 
        size_pop,
        domain,
        prob_muta,
        prob_cross,
        sel_parents,
        recombination,
        mutation,
        sel_survivors, 
        fitness
    )

    display(best_1, fenotipo)
    display_stat_n(boa, bests_average)
    display_stat_n(boa_sigma, bests_sigma_average, title='Evolution of sigma over runs', ylabel='Sigma')