"""
tsp_2017.py
Sebastian Rehfeldt, April 2017
Based on Ernesto Costa, February 2017
"""

from sea_tsp import *
from utils import *
from copy import deepcopy
import config

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

    if config.tsp_interpretation == "simple":
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

    if config.tsp_fitness == "distance":
        return distance


def getTours(distmat):

    my_fitness = fitness(distmat)
    size_cromo = distmat.shape[0]-1 # as the starting and ending point is fixed
    
    #geno = [0.4,0.7,0.4]
    #print(phenotype(geno))
    #print(evaluate(phenotype(geno),distmat))
    #should be 0,2,1,3,0 and dist should be 109.68....

    #parameters follow Golomb Ruler paper EC8 from theoretical work
    generations = config.generations
    population = config.population
    prob_muta = config.prob_muta
    prob_cross = config.prob_cross
    sigma = config.sigma
    tour_size = config.tour_size
    elite_size = config.elite_size

    bestTours = []

    if(config.tsp_development):
        best, stat, stat_average = sea_for_plot(generations,population, size_cromo, prob_muta, sigma, prob_cross,tour_sel(tour_size),two_points_cross,muta_float_gaussian,sel_survivors_elite(elite_size), my_fitness)
        if(config.tsp_plot_generations):
            display_stat_1(stat,stat_average)
            bestTours.append((phenotype(best[0]),best[1]))
        else:
            best, best_average, tours = run(config.tsp_runs,generations,population, size_cromo, prob_muta, sigma, prob_cross,tour_sel(tour_size),two_points_cross,muta_float_gaussian,sel_survivors_elite(elite_size), my_fitness)
            display_stat_n(best,best_average)
            #append first best tour to bestTours to allow rest of program to run
            bestTours.append((phenotype(tours[0][0]),tours[0][1]))
        
    else:
        tours, fitnessValues = sea(generations,population, size_cromo, prob_muta, sigma, prob_cross,tour_sel(tour_size),two_points_cross,muta_float_gaussian,sel_survivors_elite(elite_size), my_fitness)
        
        for i in range(len(tours)):
            bestTours.append((phenotype(tours[i]),fitnessValues[i]))

    return bestTours
    
