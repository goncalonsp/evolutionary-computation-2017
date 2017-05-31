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

from argparse import ArgumentParser
import config

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

    parser = ArgumentParser(
        description='Evolutionary Computation solver for function minimization.'
        )

    parser.add_argument(
        '-c', '--config', type=open,
        help='Configurations file. If not provided defaults will be used!')

    args = parser.parse_args()

    # Load configuration file
    configs = config.read_config(args.config)

    # The following calls to get_config will search the provided config file for each variable value
    # if no value is found or the config file is not specified each default value is assumed for each variable
    # "locals()[]"" will get the function by reflection using the function name as key
    n_generations = config.get_config(configs, ['number_generations'], 100)
    size_pop = config.get_config(configs, ['size_population'], 100)
    tour_size = config.get_config(configs, ['tournament_size'], 3)
    elite_size = config.get_config(configs, ['elite_percentage'], 0.1)
    n_runs = config.get_config(configs, ['runs'], 10)

    problem_function = locals()[ config.get_config(configs, ['problem_function'], "rastrigin_eval") ] 

    prob_muta = config.get_config(configs, ['mutation', 'probability'], 0.01)
    mutation_function = locals()[ config.get_config(configs, ['mutation', 'function'], "muta_float_gaussian") ] 

    prob_cross = config.get_config(configs, ['crossover', 'probability'], 0.9)
    cross_alpha = config.get_config(configs, ['crossover', 'alpha'], 0.3)
    cross_function = locals()[ config.get_config(configs, ['crossover', 'function'], "cross") ] 
    recombination_function = cross_function(cross_alpha) # Parameter: alpha

    development = config.get_config(configs, ['development'], False)
    plot_generations = config.get_config(configs, ['plot_generations'], True)

    dimensionality = config.get_config(configs, ['dimensionality'], 10)
    domain_range = config.get_config(configs, ['domain'], RASTRIGIN_DOMAIN)
    
    sigma_value = config.get_config(configs, ['mutation','sigma'], 0.6)

    if isinstance(domain_range,list):
        if isinstance(domain_range[0],list):
            # the list length is used instead of the variable "dimensionality"
            domain = domain_range
        else:
            domain = [ domain_range for _ in range(dimensionality) ]
    else:
        raise ValueError('Invalid domain value passed. Please either pick a list of floats or a list of lists of floats!')
    
    if isinstance(sigma_value, float):
        # The sigma values can be set individually like so: [0.5,0.8,1.0]. 
        # It must respect the dimensionality
        sigma = [ sigma_value for _ in range(dimensionality) ] 
    elif isinstance(sigma_value, list):
        # the list length is used instead of the variable "dimensionality"
        sigma = sigma_value
    else:
        raise ValueError('Invalid sigma value passed. Please either pick a float or a list of floats!')
    
    fitness = merito(problem_function) # Parameter: Evaluation function
    sel_parents = tour_sel(tour_size) # Parameter: tournament size
    sel_survivors = sel_survivors_elite(elite_size) # Parameter: elite ratio

    """ Single run, console result, no statistics """
    # best_1 = sea_float(
    #     n_generations, 
    #     size_pop, 
    #     domain, 
    #     prob_muta, 
    #     sigma, 
    #     prob_cross, 
    #     sel_parents, 
    #     recombination_function, 
    #     mutation_function, 
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
    #     recombination_function, 
    #     mutation_function, 
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
        recombination_function,
        mutation_function,
        sel_survivors, 
        fitness
    )

    display(best_1, fenotipo)
    display_stat_n(boa, best_average)