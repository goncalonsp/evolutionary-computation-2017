"""
ttp_2017.py
Gonçalo Pereira, April 2017
"""
import os
import sea_ttp
from utils import *
from read_ttp_file import readFile
from argparse import ArgumentParser
import math
import config
from random import shuffle, randint

import sea_tsp_permutation as sea_tsp

# to change representation easily
from tsp import phenotype_from_permutation as phenotype_tsp
from tsp import evaluate as evaluate_tsp
from kp import phenotype as phenotype_kp
from kp import evaluate as evaluate_kp

import kp
import tsp

def fitness(distmat, cityItems, itemsList, params):
    """
    distmat 
        is a matrix of distances, size N*N (N number of cities), 
        where distmat[a][b] is the distance between city a and city b
    cityItems  
        is a dictionary where, size N-1 (N number of cities),
        where the key is the city number, range [1;N-1]
        where the value an array of tuples, each representing an item
        each tuple contains 2 values, profit and weight
    itemsList
        is an array, of size I (I number of Items), where
        items[i][0] is the profit of item i
        items[i][1] is the weight of item i
        items[i][2] is the city where item i is located
    params
        is a dictionary with, as an example
        max_speed: 1.0
        edge_weight_type: CEIL_2D
        kp_data_type: [bounded, strongly, corr]
        renting_rate: 5.61
        number_of_items: 279
        problem_name: a280-TTP
        kp_capacity: 25936.0
        min_speed: 0.1
        dimension: 280
    """
    def fitness_(indiv):
        quali = evaluate(phenotype(indiv))
        return quali
    return fitness_

def phenotype(indiv):
    """
    from a tuple of 2 genotypes (tour and plan) 
    to a tuple of 2 phenotypes (tour and plan)
    """
    phenoTour = phenotype_tsp(indiv[0])
    phenoPlan = phenotype_kp(indiv[1])
    return (phenoTour, phenoPlan)

def evaluate(pheno):
    phenoTour = pheno[0]
    phenoPlan = pheno[1]

    totalValuePlan = evaluate_kp(phenoPlan, itemsList, params)

    time = calc_time(pheno, distmat, cityItems, itemsList, params)

    # calculate the profit
    rent = params['renting_rate']

    return totalValuePlan - (rent * time)

def calc_time(pheno, distmat, cityItems, itemsList, params):
    phenoTour = pheno[0]
    phenoPlan = pheno[1]
    nCities = len(phenoTour)

    totalCapacity = params['kp_capacity']
    vmax = params['max_speed']
    vmin = params['min_speed']

    # plan that will be updated as we follow the tour calculating the time
    tempPlan = list(phenoPlan)

    # calculate the time from the last to the first city
    currentWeight = kp.calc_weight(tempPlan, itemsList)
    currentWeight = (totalCapacity if currentWeight > totalCapacity else currentWeight)
    velocity = vmax - currentWeight * (vmax - vmin) / totalCapacity
    time = distmat[0, phenoTour[nCities-1]] / velocity
    
    # calculate the time for all other cities in reverse
    for i in range(nCities-1, 0, -1):

        # update the plan since we are calculating the time from city i-1 to city i
        # and the item in city i of the tour has not yet been picked
        destinationCity = phenoTour[i]
        # for each item from the city
        for item in cityItems[str(destinationCity)]:
            # remove the item index from the plan
            itemIdx = item[2]
            if itemIdx in tempPlan: tempPlan.remove(itemIdx)
        
        # calculate the time from city i-1 to city i of the tour
        currentWeight = kp.calc_weight(tempPlan, itemsList)
        currentWeight = (totalCapacity if currentWeight > totalCapacity else currentWeight)
        velocity = vmax - currentWeight * (vmax - vmin) / totalCapacity
        time += distmat[phenoTour[i-1], phenoTour[i]] / velocity

    # from the starting point to the first city in the tour
    # no items have been picked, no impact on velocity
    time += distmat[0, phenoTour[0]]

    return time

# EA Custom functions!
# population generation with custom knowledge about the problem!
def gera_pop_ttp_random(fitness_fnc_kp):
    def gera_pop(size_pop, size_cromo):
        return [(gera_indiv_random(size_cromo, fitness_fnc_kp),0) for i in range(size_pop)]
    
    return gera_pop

def gera_pop_ttp_heuristic(shortest_cities, fitness_fnc_kp):
    def gera_pop(size_pop,size_cromo):
        starting_points = list(range(1,size_cromo[0]))
        shuffle(starting_points)
        starting_points = starting_points[:size_pop]

        return [(gera_indiv_heuristic(size_cromo, fitness_fnc_kp, starting_points.pop(0)),0) for i in range(size_pop)]

    return gera_pop

def gera_indiv_random(size_cromo, fitness_fnc_kp):
    return (sea_tsp.gera_indiv(size_cromo[0]), kp.gera_kp_indiv(size_cromo[1], fitness_fnc_kp))

def gera_indiv_heuristic(size_cromo, fitness_fnc_kp, start):
    return (tsp.dist_heuristic_tsp_indiv_generation(start, shortest_cities, size_cromo[0]), kp.gera_kp_indiv(size_cromo[1], fitness_fnc_kp))


if __name__ == '__main__':

    parser = ArgumentParser(
        description='Evolutionary Computation solver for the TTP Problem.')

    parser.add_argument(
        'INPUT', type=str,
        help='ttp file to be read.')

    parser.add_argument(
        '-c', '--config', type=open,
        help='Configurations file. If not provided defaults will be used!')

    args = parser.parse_args()

    # Load configuration file
    configs = config.read_config(args.config)

    # The following calls to get_config will search the provided config file for each variable value
    # if no value is found or the config file is not specified each default value is assumed for each variable
    # "locals()[]"" will get the function by reflection using the function name as key
    generations = config.get_config(configs, ['number_generations'], 100)
    population_size = config.get_config(configs, ['size_population'], 20)
    tsp_init_pop = config.get_config(configs, ['tsp', 'initial_pop'], "heuristic")
    
    prob_muta_tsp = config.get_config(configs, ['tsp', 'mutation', 'probability'], 0.25)
    prob_cross_tsp = config.get_config(configs, ['tsp', 'crossover', 'probability'], 0.75)
    prob_muta_kp = config.get_config(configs, ['kp', 'mutation', 'probability'], 0.25)
    prob_cross_kp = config.get_config(configs, ['kp', 'crossover', 'probability'], 0.75)
    prob_muta = (prob_muta_tsp, prob_muta_kp)
    prob_cross = (prob_cross_tsp, prob_cross_kp)

    tour_size = config.get_config(configs, ['tournament_size'], 5)
    elite_size = config.get_config(configs, ['elite_percentage'], 0.1)
    runs = config.get_config(configs, ['runs'], 5)

    development = config.get_config(configs, ['development'], False)
    plot_generations = config.get_config(configs, ['plot_generations'], True)
    
    # Read the file
    print("===================Instance==============")
    print(args.INPUT)
    distmat, cityItems, itemsList, shortest_cities, params = readFile(args.INPUT);

    # Define EA parameters
    size_cromo = (distmat.shape[0]-1, len(itemsList)) # as the starting and ending point is fixed
    my_fitness = fitness(distmat, cityItems, itemsList, params)
    sea = sea_ttp.sea
    sea_for_plot = sea_ttp.sea_for_plot
    run = sea_ttp.run
    crossover = sea_ttp.cross_operator
    mutation = sea_ttp.muta_operator
    tour_selection = sea_ttp.tour_sel(tour_size)
    sel_survivors = sea_ttp.sel_survivors_elite(elite_size)

    if tsp_init_pop == "random":
        gen_population = gera_pop_ttp_random(kp.fitness(itemsList, params))
    else:
        gen_population = gera_pop_ttp_heuristic(shortest_cities, kp.fitness(itemsList, params))

    args = [generations, population_size, size_cromo, prob_muta, prob_cross, tour_selection, crossover, mutation, sel_survivors, my_fitness, gen_population]

    if(development):
        if(plot_generations):
            best, population, stat, stat_average = sea_for_plot(*args)
            
            display_stat_1(stat,stat_average)
        else:
            best, population = sea(*args)

    else:
        best, best_average, tours = run(runs, *args)

        if(plot_generations):
            display_stat_n(best,best_average)

        print("\n===================BEST OF ALL RUNS==============")
        best = tours[0]
        for tour in tours:
            if tour[1] > best[1]:
                best = tour

    tour = phenotype_tsp(best[0][0])
    length = evaluate_tsp(tour, distmat)
    plan = phenotype_kp(best[0][1])
    weight = kp.calc_weight(plan, itemsList)
    profit = evaluate_kp(plan, itemsList, params)
    time = calc_time((tour, plan), distmat, cityItems, itemsList, params)
    objective = profit - time*params["renting_rate"]

    """             OUTPUT             """
    print("\n\n===================TOUR==============")
    print(tour)
    print("\n===================LENGTH==============")
    print(length) #linkern length is around 2613 (using MATLAB code for a280)

    print("\n\n===================Plan==============")
    print(plan)
    print("\n===================Weight==============")
    print(weight)

    print("\n\n===================Objective==============")
    print("Profit   : "+str(profit))
    print("Time     : "+str(time))
    print("Rent     : "+str(params["renting_rate"]))
    print("Objective: "+str(objective))
