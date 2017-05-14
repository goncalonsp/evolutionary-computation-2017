"""
sea_bin.py
A very simple EA for float representation.
Ernesto Costa, March 2015 & February 2016
Adjusted by Sebastian Rehfeldt
Adjusted by Gonçalo Pereira
"""

from random import random,randint, sample, gauss, shuffle
from operator import itemgetter
from tsp import dist_heuristic_tsp_indiv_generation

import sea_tsp_permutation as sea_tsp
import sea_bin_2016_visual as sea_kp

# Simple Evolutionary Algorithm     
def sea(numb_generations,size_pop, size_cromo, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func):
    # initialize population: indiv = (cromo,fit)
    population = gen_pop_func(size_pop, size_cromo)
    # evaluate population
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]
    for i in range(numb_generations):
        # parents selection
        mate_pool = sel_parents(population)
    # Variation
    # ------ Crossover
        parents = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            children = recombination(indiv_1,indiv_2, prob_cross)
            parents.extend(children) 
        # ------ Mutation
        descendants = []
        for cromo,fit in parents:
            new_indiv = mutation(cromo,prob_mut)
            descendants.append((new_indiv,fitness_func(new_indiv)))
        # New population
        population = sel_survivors(population,descendants)
        # Evaluate the new population
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]   

    """
    return: the best individual found
            the population of the final generation
    """
    return best_pop(population), population

def sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func):
    # initialize population: indiv = (cromo,fit)
    population = gen_pop_func(size_pop, size_cromo)
    # evaluate population
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]

    stat = [best_pop(population)[1]]
    stat_aver = [average_pop(population)]

    for i in range(numb_generations):
        # parents selection
        mate_pool = sel_parents(population)
    # Variation
    # ------ Crossover
        parents = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            children = recombination(indiv_1,indiv_2, prob_cross)
            parents.extend(children) 
        # ------ Mutation
        descendants = []
        for cromo,fit in parents:
            new_indiv = mutation(cromo,prob_mut)
            descendants.append((new_indiv,fitness_func(new_indiv)))
        # New population
        population = sel_survivors(population,descendants)
        # Evaluate the new population
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]   

        stat.append(best_pop(population)[1])
        stat_aver.append(average_pop(population))

        #print(population)
        #input("Continue...")

    """
    return: the best individual found
            the population of the final generation
            the best individual from each generation
            the average individual from each generation
    """
    return best_pop(population), population, stat, stat_aver

def run(numb_runs,numb_generations,size_pop, domain, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func):
    statistics = []
    bestTours = []
    for i in range(numb_runs):
        best, population, stat_best, stat_aver = sea_for_plot(numb_generations,size_pop, domain, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func)
        bestTours.append(best)
        statistics.append(stat_best)
        print("{}%".format( (i+1)*100/numb_runs ))
    stat_gener = list(zip(*statistics))
    best = [max(g_i) for g_i in stat_gener] # maximization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return best,aver_gener,bestTours
    

# Initialize population
def gera_pop(size_pop,size_cromo, shortest_cities,tsp_init_pop):
    starting_points = list(range(1,size_cromo))
    shuffle(starting_points)
    starting_points = starting_points[:size_pop]

    return [(gera_indiv(size_cromo,starting_points.pop(0),shortest_cities,tsp_init_pop),0) for i in range(size_pop)]

def gera_indiv(size_cromo,start, shortest_cities,tsp_init_pop):
    if tsp_init_pop == "random":
        indiv = (sea_tsp.gera_indiv(size_cromo), sea_kp.gera_indiv(size_cromo))
    else:
        indiv = (dist_heuristic_tsp_indiv_generation(start,shortest_cities,size_cromo), sea_kp.gera_indiv(size_cromo))
    return indiv

# Variation operators: mutation     
def muta_operator(indiv, prob_muta):
    # indiv is a tuple = (indiv_tsp, indiv_kp)
    # prob_muta is a tuple = (prob_muta_tsp, prob_muta_kp)
    muta_indiv_tsp = sea_tsp.muta_permutation(indiv[0], prob_muta[0])
    muta_indiv_kp = sea_kp.muta_bin(indiv[1], prob_muta[1])
    return (muta_indiv_tsp, muta_indiv_kp)

# Variation Operators :Crossover
def cross_operator(indiv_1, indiv_2, prob_cross):
    cross_indiv_tsp = sea_tsp.cycle_crossover((indiv_1[0][0],0), (indiv_2[0][0],0), prob_cross[0])
    cross_indiv_kp = sea_kp.uniform_cross((indiv_1[0][1],0), (indiv_2[0][1],0), prob_cross[1])
    return (((cross_indiv_tsp[0][0], cross_indiv_kp[0][0]),0), ((cross_indiv_tsp[1][0], cross_indiv_kp[1][0]),0))

# Parents Selection: tournament
def tour_sel(t_size):
    def tournament(pop):
        size_pop= len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = one_tour(pop,t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def one_tour(population,size):
    """Maximization Problem. Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]


# Survivals Selection: elitism
def sel_survivors_elite(elite):
    def elitism(parents,offspring):
        size = len(parents)
        comp_elite = int(size* elite)
        offspring.sort(key=itemgetter(1), reverse=True)
        parents.sort(key=itemgetter(1), reverse=True)
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism


# Auxiliary
    
def best_pop(population):
    population.sort(key=itemgetter(1),reverse=True)
    return population[0]

def average_pop(population):
    return sum([fit for cromo,fit in population])/len(population)

