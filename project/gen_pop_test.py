"""
gen_pop_test.py
A script file made to easily test the impact
of different generation population algorithms
for TSP in the objective function for TTP.

Gabriel Rodrigues, May 2017
Based on Sebastian Rehfeldt's ttp.py
"""

import os
from read_ttp_file import readFile
from argparse import ArgumentParser
import math
import tsp
import sea_tsp_permutation as sea
import kp
import config
from config import get_config
import numpy as np
from ttp import calculateObjectiveValue


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Evolutionary Computation solver for the TTP Problem.'
        )

    parser.add_argument(
        'INPUT', type=str,
        help='ttp file to be read.')

    parser.add_argument(
        '-c', '--config', type=open,
        help='Configurations file. If not provided defaults will be used!')

    args = parser.parse_args()

    # Load configuration file
    configs = config.read_config(args.config)
    
    #TODO verify the solution on toy example from paper "The travelling thief problem: the first ..."

    folder = os.path.dirname(os.path.realpath(__file__))
    
    # Read the file
    print("===================Instance==============")
    print(args.INPUT)
    distmat, cityItems, itemsList, shortest_cities, params = readFile(args.INPUT);
    size_cromo = distmat.shape[0]-1 # as the starting and ending point is fixed
    population_size = get_config(configs['tsp'], ['size_population'], 20)
    fitness_func = tsp.fitness_permutation(distmat)

    gen_pop = tsp.value_heuristic_pop_generation(distmat, items)
    value_heuristic_pop = gen_pop(population_size, size_cromo)
    random_pop = sea.gera_pop(population_size, size_cromo)

    value_heuristic_pop = [(indiv[0], fitness_func(indiv[0])) for indiv in value_heuristic_pop]
    random_pop = [(indiv[0], fitness_func(indiv[0])) for indiv in random_pop]

    print("\n\n===================Tour length==============")

    print("Value Heuristic population best fitness: {}".format( sea.best_pop(value_heuristic_pop)[1]))
    print("Value Heuristic population average fitness: {}".format( sea.average_pop(value_heuristic_pop)))
    print("Random population best fitness: {}".format( sea.best_pop(random_pop)[1]))
    print("Random population average fitness: {}".format( sea.average_pop(random_pop)))


    heuristic_pop_kp = np.empty(population_size, dtype=float)
    random_pop_kp = np.empty(population_size, dtype=float)
    for idx in range(population_size):
        plan = kp.getPackingPlan(items, value_heuristic_pop[idx][0], distmat, params)
        profit, time, objective = calculateObjectiveValue(value_heuristic_pop[idx][0],plan,distmat,params)
        heuristic_pop_kp[idx] = objective

        plan = kp.getPackingPlan(items, random_pop[idx][0], distmat, params)
        profit, time, objective = calculateObjectiveValue(random_pop[idx][0],plan,distmat,params)
        random_pop_kp[idx] = objective

    print("\n\n===================Objective fitness==============")

    print("Value Heuristic population best fitness: {}".format( np.amax(heuristic_pop_kp) ))
    print("Value Heuristic population average fitness: {}".format( np.mean(heuristic_pop_kp) ))
    print("Random population best fitness: {}".format( np.amax(random_pop_kp) ))
    print("Random population average fitness: {}".format( np.mean(random_pop_kp) ))

