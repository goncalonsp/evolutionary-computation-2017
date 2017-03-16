"""
mapColoring.py
Authors:  , Sebastian Rehfeldt, 
"""

#Todo: add names

from sea import *
from utils import *
from math import sqrt
from multiprocessing import Pool
import os 
import argparse
import json

# interface
# from file to coordinates

def readData(file):
    """ From a Mac Coloring format file return the graph representation."""
    """
    file contents will be in the form of:
        Country: PT     Neighbors: SP
        Country: SP     Neighbors: PT FR
        Country: FR     Neighbors: SP BE LU SW IT
        Country: BE     Neighbors: FR HO LU
        Country: LU     Neighbors: FR BE
        Country: SW     Neighbors: FR IT
        Country: IT     Neighbors: FR SW
        Country: HO     Neighbors: BE
    """
    neighbors = {}
    mappingDict = []
    with  open(file) as f:
	
        data = f.readlines()
        for line in data:
            words = line.split()

            # neighbors will be our graph - it is a dictionary with a country as key and lists of neighbors as values
            # it is a map because we want to get neighbors for a given country efficiently
            #       example: {'PT': ['SP'], 'SP': ['PT', 'FR'], ... }
            neighbors[words[1]] = words[3:]

            # our individuals will be represented by an array containing integers
            # mappingDict is used to map a color on a specific index to a country name
            #       example: ['PT', 'SP', 'FR', ... ]
            mappingDict.append(words[1])
    
    f.closed
    return neighbors, mappingDict


# fitness
def merit(map,mappingDict):
    def merit_(indiv):
        return evaluate(phenotype(indiv,map,mappingDict))
    return merit_

def phenotype(genotype,neighbors,mappingDict):
    """ Return ther phenotype."""
    # I decided to use also a dictionary here for the phenotype to get the neighbors efficiently in the evaluate function
    #       example: { 'PT': (1, ['ES']), 'ES': (3, ['PT', 'FR']), ... }
    pheno = {}
    for ind, color in enumerate(genotype):
        pheno[mappingDict[ind]] = (color,neighbors[mappingDict[ind]]) 

    return pheno

def evaluate(countries):
	# The argument "countries" is the phenotype of the individual
    # Todo: Implement our approach
    num_countries = len(countries)
    num_color, num_violations = getColorsAndViolations(countries)
    value_color_sum = getColorsValueSum(countries)

    # Todo: experimentation is needed here
    alpha = 2
    beta = 2

    # sum of colors will decrease fitness
    charlie = 0.2

    # this value should be high
    # this value decreases with number of colors used (this is really bad and is factored stronger than the number of violations)
    # this value decreases with number of violations
    # we can drop the num_countries, but I like to have positive numbers for the fitness value :)
    fitnessValue = num_countries - alpha*num_color - beta*num_violations - charlie*value_color_sum

    return fitnessValue



def getColorsAndViolations(countries):
    colors = set()
    num_violations = 0

    for country in countries:
        color, neighbors = countries[country]
        colors.add(color)

        for neighbor in neighbors:
            if(color == countries[neighbor][0]):
                num_violations = num_violations+1

    num_colors = len(colors)
    num_violations = num_violations/2
    return num_colors, num_violations

def getColorsValueSum(countries):
    colors = set()
    value_color_sum = 0


    for country in countries:
        color, neighbors = countries[country]
        value_color_sum = value_color_sum +color


    return value_color_sum

def get_config(config, keys, default):
    if not keys: return config
    if not config: return default
    
    if isinstance(config,dict):
        if keys[0] in config: 
            return get_config(config[keys[0]], keys[1:], default)
    if isinstance(config,list):
        if len(config) >= keys[0]:
            return get_config(config[keys[0]], keys[1:], default)

    return default


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solves the Map Coloring problem using the Simple Evolutionary Algorithm.'
        )
    parser.add_argument(
        'inputfile',
        help='A file in Map Coloring format.')
    parser.add_argument(
        '-r', '--runs', type=int, nargs='?',
        help='Number of separate algorithm runs for statistical analysis.')
    parser.add_argument(
        '-p', '--plot', action='store_true',
        help='Turns on plotting capabilities.')
    parser.add_argument(
        '-s', '--save', action='store_true',
        help='Saves plots into files.')
    parser.add_argument(
        '-c', '--config', type=open,
        help='Config file for the SEA Algorithm.')
    args = parser.parse_args()
    #print(args) # Uncomment this line to debug the arguments

    # Load configuration file
    config = (json.load(args.config) if args.config else None)
    #print(config) # Uncomment this line to debug the arguments
        
    # Creates all data structures given the data file
    neighbors, mappingDict = readData(args.inputfile)

    # just for testing phenotype function
    # print(phenotype([1,0,0,0,0,0,0,0],neighbors,mappingDict))
    
    my_merit = merit(neighbors,mappingDict)
    size_cromo = len(mappingDict)

    # I decided to store this in variables instead of using the values in the 
    # function call so that the values are the same for each function call below
    # The following calls to get_config will search the provided config file for each variable value
    # if no value is found or the config file is not specified each default value is assumed for each variable
    cross_function = locals()[ get_config(config, ['crossover', 'function'], "one_point_cross") ] 
    # "locals()[]"" will get the function by reflection using the function name as key
    muta_function = locals()[ get_config(config, ['mutation', 'function'], "muta_rand") ]
    prob_muta = get_config(config, ['mutation', 'probability'], 0.05)
    prob_cross = get_config(config, ['crossover', 'probability'], 0.9)
    tour_num = get_config(config, ['tournament_size'], 3)
    elite_percentage = get_config(config, ['elite_percentage'], 0.1)
    numb_generations = get_config(config, ['number_generations'], 1000)
    size_pop = get_config(config, ['size_population'], 20)

    if args.runs == None:
        # Single run mode

        if not args.plot and not args.save:
            # Use this for running just the algorithm
            best = sea(numb_generations, size_pop, size_cromo, prob_muta, prob_cross, tour_sel(tour_num), cross_function, muta_function, sel_survivors_elite(elite_percentage), my_merit)

        else:
            # Use this for getting a plot for a single run
            best, stat, stat_average = sea_for_plot(numb_generations, size_pop, size_cromo, prob_muta, prob_cross, tour_sel(tour_num), cross_function, muta_function, sel_survivors_elite(elite_percentage), my_merit)
            if args.plot:
                display_stat_1(stat, stat_average)
            if args.save:
                file_name = 'stat_1_plot.png'
                print("Saved plot to file '" + file_name + "'.")
                save_stat_1(stat, stat_average, file_name)
            
        # Used for printing information about best individual
        print(phenotype(best[0],neighbors,mappingDict))
        print("Fitness: "+str(best[1]))
        print("Colors: "+str(getColorsAndViolations(phenotype(best[0],neighbors,mappingDict))[0]))
        print("Violations: "+str(getColorsAndViolations(phenotype(best[0],neighbors,mappingDict))[1]))
    
    else:
        boa, best_average = run(args.runs,numb_generations,size_pop, size_cromo, prob_muta,  prob_cross,tour_sel(tour_num),cross_function,muta_function,sel_survivors_elite(elite_percentage), my_merit)
        if args.plot: 
            display_stat_n(boa,best_average)
        if args.save:
            file_name = 'stat_n_plot.png'
            print("Saved plot to file '" + file_name + "'.")
            save_stat_n(boa, best_average, file_name)
