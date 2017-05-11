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
    distmat, items, params = readFile(args.INPUT)
    size_cromo = distmat.shape[0]-1 # as the starting and ending point is fixed
    population_size = get_config(configs['tsp'], ['size_population'], 20)
    fitness_func = tsp.fitness_permutation(distmat)

    gen_pop = tsp.heuristic_pop_generation(distmat, items)
    heuristic_pop = gen_pop(population_size, size_cromo)
    random_pop = sea.gera_pop(population_size, size_cromo)

    heuristic_pop = [(indiv[0], fitness_func(indiv[0])) for indiv in heuristic_pop]
    random_pop = [(indiv[0], fitness_func(indiv[0])) for indiv in random_pop]

    print("\n\n===================Tour length==============")

    print("Heuristic population best fitness: {}".format( sea.best_pop(heuristic_pop)[1]))
    print("Heuristic population average fitness: {}".format( sea.average_pop(heuristic_pop)))
    print("Random population best fitness: {}".format( sea.best_pop(random_pop)[1]))
    print("Random population average fitness: {}".format( sea.average_pop(random_pop)))


    heuristic_pop_kp = np.empty(population_size, dtype=float)
    random_pop_kp = np.empty(population_size, dtype=float)
    for idx in range(population_size):
        plan = kp.getPackingPlan(items, heuristic_pop[idx][0], distmat, params)
        profit, time, objective = calculateObjectiveValue(heuristic_pop[idx][0],plan,distmat,params)
        heuristic_pop_kp[idx] = objective

        plan = kp.getPackingPlan(items, random_pop[idx][0], distmat, params)
        profit, time, objective = calculateObjectiveValue(random_pop[idx][0],plan,distmat,params)
        random_pop_kp[idx] = objective

    print("\n\n===================Objective fitness==============")

    print("Heuristic population best fitness: {}".format( np.amax(heuristic_pop_kp) ))
    print("Heuristic population average fitness: {}".format( np.mean(heuristic_pop_kp) ))
    print("Random population best fitness: {}".format( np.amax(random_pop_kp) ))
    print("Random population average fitness: {}".format( np.mean(random_pop_kp) ))

