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

from argparse import ArgumentParser
import config

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
    cross_function = locals()[ config.get_config(configs, ['crossover', 'function'], "heuristical_cross") ] 
    recombination_function = cross_function(cross_alpha) # Parameter: alpha

    development = config.get_config(configs, ['development'], False)
    plot_generations = config.get_config(configs, ['plot_generations'], True)

    dimensionality = config.get_config(configs, ['dimensionality'], 10)
    domain_range = config.get_config(configs, ['domain'], RASTRIGIN_DOMAIN)
    
    sigma_domain = config.get_config(configs, ['mutation','sigma_domain'], 0.6)

    if not isinstance(domain_range,list):
        raise ValueError('Invalid domain value passed. Please choose a list of floats!')
    if not isinstance(sigma_domain,list):
        raise ValueError('Invalid sigma domain value passed. Please choose a list of floats!')

    domain = [ (domain_range, sigma_domain) for _ in range(dimensionality) ]
        
    
    fitness = merito(problem_function) # Parameter: Evaluation function
    sel_parents = tour_sel(tour_size) # Parameter: tournament size
    sel_survivors = sel_survivors_elite(elite_size) # Parameter: elite ratio

    """ Single run, console result, no statistics """
    # best_1 = sea_float(
    #     n_generations, 
    #     size_pop, 
    #     domain, 
    #     prob_muta, 
    #     prob_cross, 
    #     sel_parents, 
    #     recombination_function, 
    #     mutation_function, 
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
    #     recombination_function, 
    #     mutation_function, 
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
        recombination_function,
        mutation_function,
        sel_survivors, 
        fitness
    )

    display(best_1, fenotipo)
    display_stat_n(boa, bests_average)
    display_stat_n(boa_sigma, bests_sigma_average, title='Evolution of sigma over runs', ylabel='Sigma')