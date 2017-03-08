"""
mapColoring.py
Authors:  , Sebastian Rehfeldt, 
"""

#Todo: add names

from sea import *
from utils import *
from math import sqrt
from sets import Set
import os 

# interface
# from file to coordinates

def readData(file):
    """ From a TSP format file return the matrix of coordinates."""
    map = {}
    mappingDict = []
    with  open(file) as f:
	
        data = f.readlines()
        for line in data:
            words = line.split()

            #map will be our graph - it is a dictionary with a country as key and lists of neighbors as values
            #it is a map because we want to get neighbors for a given country efficiently
            map[words[1]] = words[3:]

            #our individuals will be representated by an array containing integers
            #mappingDict is used to map a color on a specific index to a country name
            mappingDict.append(words[1])
    
    f.closed
    return map, mappingDict


# fitness
def merit(map,mappingDict):
    def merit_(indiv):
        return evaluate(phenotype(indiv,map,mappingDict))
    return merit_

def phenotype(genotype,map,mappingDict):
    """ Return ther phenotype."""
    # I decided to use also a dictionary here for the phenotype to get the neighbors efficiently in the evaluate function
    pheno = {}
    for ind, color in enumerate(genotype):
        pheno[mappingDict[ind]] =(color,map[mappingDict[ind]]) 

    return pheno

def evaluate(countries):
    #Todo: Implement our approach
    num_countries = len(countries)
    num_color, num_violations = getColorsAndViolations(countries)

    #Todo: experimentation is need here
    alpha = 1
    beta = 1

    #this value should be high
    #this value decreases with number of colors used (this is really bad and is factored stronger than the number of violations)
    #this value decreases with number of violations
    #we can drop the num_countries, but I like to have positive numbers for the fitness value :)
    fitnessValue = num_countries - alpha*num_color - beta*num_violations

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





if __name__ == '__main__':
    """Creates all data structures given the data file"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    map, mappingDict  = readData(dir_path+'/countries.rawData')

    #just for testing phenotype function
    #print(phenotype([1,0,0,0,0,0,0,0],map,mappingDict))
    
    my_merit = merit(map,mappingDict)
    size_cromo = len(mappingDict)

    #I decided to store this in variables instead of using the values in the function call so that the values are the same for each function call below
    cross_function = one_point_cross
    muta_function = muta_rand
    prob_muta = 0.05
    prob_cross = 0.9
    tour_num = 3
    elite_percentage = 0.1
    numb_generations = 30
    size_pop = 20

    #better use the one below
    #best = sea(numb_generations,size_pop, size_cromo, prob_muta,  prob_cross,tour_sel(tour_num),cross_function,muta_function,sel_survivors_elite(elite_percentage), my_merit)
    
    #use this for getting a plot for a single run
    best, stat, stat_average = sea_for_plot(numb_generations,size_pop, size_cromo, prob_muta,  prob_cross,tour_sel(tour_num),cross_function,muta_function,sel_survivors_elite(elite_percentage), my_merit)
    display_stat_1(stat,stat_average)  
    
    #used for printing information about best individual
    #works with both sea functions
    print(phenotype(best[0],map,mappingDict))
    print("Fitness: "+str(best[1]))
    print("Colors: "+str(getColorsAndViolations(phenotype(best[0],map,mappingDict))[0]))
    print("Violations: "+str(getColorsAndViolations(phenotype(best[0],map,mappingDict))[1]))
    
    #boa, best_average = run(5,numb_generations,size_pop, size_cromo, prob_muta,  prob_cross,tour_sel(tour_num),cross_function,muta_function,sel_survivors_elite(elite_percentage), my_merit)
    #display_stat_n(boa,best_average)
