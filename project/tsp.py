"""
tsp_2017.py
Sebastian Rehfeldt, April 2017
Based on Ernesto Costa, February 2017
"""

from sea_tsp import *
from utils import *
from math import sqrt
from copy import deepcopy

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

    sorted_geno = sorted(genotype,reverse=True)
    #TODO find a smarter way for that
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
    for i in range(number_of_cities-1):
        j = (i + 1) % number_of_cities
        distance += distmat[tour[i], tour[j]]
    distance += distmat[0,tour[number_of_cities-1]]

    return distance


def getTour(coordinates,distmat):
    
    my_fitness = fitness(distmat)
    size_cromo = len(coordinates)-1 # as the starting and ending point is fixed
    
    #geno = [0.4,0.7,0.4]
    #print(phenotype(geno))
    #print(evaluate(phenotype(geno),distmat))
    #should be 0,2,1,3,0 and dist should be 109.68....

    #parameters follow Golomb Ruler paper EC8 from theoretical work
    generations = 100
    population = 100
    prob_muta = 0.25
    prob_cross = 0.75
    sigma = 0.1

    best = sea(generations,population, size_cromo, prob_muta, sigma, prob_cross,tour_sel(5),two_points_cross,muta_float_gaussian,sel_survivors_elite(0.1), my_fitness)
    pheno = phenotype(best[0])
    print(pheno)
    #print(min(pheno)) #should be 1
    #print(max(pheno)) #should be length -1
    #print(len(set(pheno))) #should be as the one above
    print(best[1]) #should be low

    return pheno, best[1]
    
