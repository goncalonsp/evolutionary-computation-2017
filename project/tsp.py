"""
tsp_2017.py
Sebastian Rehfeldt, April 2017
Based on Ernesto Costa, February 2017
"""

from sea_tsp import *
from utils import *
from copy import deepcopy
from config import get_config

# fitness
def fitness(distmat):
    def fitness_(indiv):
        return evaluate(phenotype(indiv),distmat)
    return fitness_

def phenotype(genotype):
    """ Return the phenotype which is the tour."""
    # phenotype is a permutation of integers higher than 1 where each integer represents a city
    # the values are higher than 0 as the first city is fixed to the first city with index 0
    #   for example [0, 1, 4, 6, 2, 3, 5, 7, 9, 8] 
    #
    # this function interprets a random key representation
    # the genotype will be a list of values in range [0,1]
    #
    # first values are sorted in descending order
    # then original positions of these values form permutation

    sorted_geno = sorted(genotype,reverse=True)
    #TODO find a more performant way for that
    #TODO maybe also consider distance to previous city for the interpretation phase (selection of order)
    genoTemp = deepcopy(genotype)
    pheno = []
    for val in sorted_geno:
        index = genoTemp.index(val)
        pheno.append(index+1)

        genoTemp[index] = 2 #this is necessary in the case that random values are duplicated
    return pheno


def evaluate(tour,distmat):
    number_of_cities = len(tour)
    distance = distmat[0,tour[0]] #distance from fixed starting point to first city of tour
    #TODO consider also where items are available
    #cities with high valued and heavy items should be in the end of the tour
    for i in range(number_of_cities-1):
        j = (i + 1) % number_of_cities
        distance += distmat[tour[i], tour[j]]
    distance += distmat[0,tour[number_of_cities-1]]

    return distance

def select_best_k_tours(population,k):
    population.sort(key=itemgetter(1),reverse=False)

    tours = []
    fitnessValues = []
    
    i = 0
    while len(tours)<k and i<len(population):
        #add to tours if this tour is not already in best tours
        pop = population[i][0]
        if(not pop in tours):
            tours.append(pop)
            fitnessValues.append(population[i][1])

        i += 1

    return tours, fitnessValues

def getTours(distmat, configs, ntours):

    my_fitness = fitness(distmat)
    size_cromo = distmat.shape[0]-1 # as the starting and ending point is fixed
    
    #geno = [0.4,0.7,0.4]
    #print(phenotype(geno))
    #print(evaluate(phenotype(geno),distmat))
    #should be 0,2,1,3,0 and dist should be 109.68....

    # The following calls to get_config will search the provided config file for each variable value
    # if no value is found or the config file is not specified each default value is assumed for each variable
    
    #parameters follow Golomb Ruler paper EC8 from theoretical work
    generations = get_config(configs, ['number_generations'], 100)
    population_size = get_config(configs, ['size_population'], 20)
    prob_muta = get_config(configs, ['mutation', 'probability'], 0.25)
    prob_cross = get_config(configs, ['crossover', 'probability'], 0.75)
    sigma = get_config(configs, ['mutation', 'sigma'], 0.1)
    tour_size = get_config(configs, ['tournament_size'], 5)
    elite_size = get_config(configs, ['elite_percentage'], 0.1)
    runs = get_config(configs, ['runs'], 5)

    tsp_development = get_config(configs, ['development'], False)
    tsp_plot_generations = get_config(configs, ['plot_generations'], True)

    bestTours = []

    if(tsp_development):
        if(tsp_plot_generations):
            best, population, stat, stat_average = sea_for_plot(generations,population_size, size_cromo, prob_muta, sigma, prob_cross,tour_sel(tour_size),two_points_cross,muta_float_gaussian,sel_survivors_elite(elite_size), my_fitness)
            display_stat_1(stat,stat_average)
            bestTours = select_best_k_tours(population, ntours)
        else:
            best, population = sea(generations,population_size, size_cromo, prob_muta, sigma, prob_cross,tour_sel(tour_size),two_points_cross,muta_float_gaussian,sel_survivors_elite(elite_size), my_fitness)
            bestTours = select_best_k_tours(population, ntours)

    else:
        best, best_average, tours = run(runs, generations,population_size, size_cromo, prob_muta, sigma, prob_cross,tour_sel(tour_size),two_points_cross,muta_float_gaussian,sel_survivors_elite(elite_size), my_fitness)
        display_stat_n(best,best_average)
        #append first best tour to bestTours to allow rest of program to run
        bestTours.append((phenotype(tours[0][0]),tours[0][1]))
    
    return bestTours
    
