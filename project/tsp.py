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
    #phenotype is a permutation of integers higher than 1 where each integer represents a city
    #the values are higher than 0 as the first city is fixed to the first city with index 0
    #it interprets the random key representation
    #first values are sorted in decending order
    #then original positions of these values form permutation

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


def getTours(coordinates,distmat):

    my_fitness = fitness(distmat)
    size_cromo = len(coordinates)-1 # as the starting and ending point is fixed
    
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

    if(config.tsp_development):
        pass
        #TODO plot results to estimate needed #generations
        #TODO run multiple times to find good parameters
    else:
        tours, fitnessValues = sea(generations,population, size_cromo, prob_muta, sigma, prob_cross,tour_sel(tour_size),two_points_cross,muta_float_gaussian,sel_survivors_elite(elite_size), my_fitness)

    bestTours = []
    for i in range(len(tours)):
        bestTours.append((phenotype(tours[i]),fitnessValues[i]))

    return bestTours
    
