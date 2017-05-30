#! /usr/bin/env python

"""
sea_float.py
A very simple EA for float representation,
with the self-adaptation of the sigma parameter.
Based on Ernesto Costa's work, February 2016
Extended by Gabriel Rodrigues & Gonçalo Pereira
"""

__author__ = 'Ernesto Costa'
__date__ = 'February 2016'

import numpy as np
import matplotlib.pyplot as plt
from random import random, randint, uniform, sample, shuffle, gauss
from operator import itemgetter
from math import fabs

# For the statistics
def run(numb_runs,numb_generations,size_pop, domain, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    statistics = []
    statistics_sigma = []
    best_1 = [0,1000] # minimization

    for i in range(numb_runs):
        best, stat_best, stat_aver, stat_sigma, stat_aver_sigma = sea_for_plot(numb_generations, size_pop, domain, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func)
        statistics.append(stat_best)
        statistics_sigma.append(stat_sigma)
        if best_1[1] > best[1]: # minimization
            best_1 = best
        print("Percentage: " + str((i + 1)*100/numb_runs) + "%")

    stat_gener = list(zip(*statistics))
    stat_sigma_gener = list(zip(*statistics_sigma))
    boa = [min(g_i) for g_i in stat_gener] # minimization
    boa_sigma = [g_i[ stat_gener[i].index(boa[i]) ] for i,g_i in enumerate(stat_sigma_gener)]

    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    aver_sigma_gener = [sum(g_i)/len(g_i) for g_i in stat_sigma_gener]
    return best_1, boa, aver_gener, boa_sigma, aver_sigma_gener
    
def run_for_file(filename,numb_runs,numb_generations,size_pop, domain, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    with open(filename,'w') as f_out:
        for i in range(numb_runs):
            best = sea_float(numb_generations,size_pop, domain, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func)
            f_out.write(str(best[1])+'\n')


# Self-Adapted-Sigma [Float] Evolutionary Algorithm 
def sea_float(numb_generations,size_pop, domain, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    """
    initialize population: 
    population = [..., indiv, ...]
    indiv = ((..., (value_i, sigma_i), ...), fitness)
    domain = [...-,[inf_i, sup_i],...]
    """
    
    population = gera_pop(size_pop,domain)
    # evaluate population
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]
    for i in range(numb_generations):
    # parents selection
        mate_pool = sel_parents(population)
    # Variation
    # ------ Crossover
        parents = []
        for i in range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            children = recombination(indiv_1,indiv_2, prob_cross, domain)
            # print(children)
            parents.extend(children) 

    # ------ Mutation
        descendants = []
        for cromo,fit in parents:
            new_indiv = mutation(cromo,prob_mut, domain)
            descendants.append((new_indiv,fitness_func(new_indiv)))
    # New population
        population = sel_survivors(population,descendants)
    # Evaluate the new population
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]     
    return best_pop(population)

def sea_for_plot(numb_generations,size_pop, domain, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    # Initialize population: indiv = (cromo,fit)
    population = gera_pop(size_pop,domain)
    # evaluate population
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]
    
    # for statistics
    best_1 = best_pop(population)
    stat = [best_1[1]]
    stat_sigma = [average_sigma(best_1[0])]
    stat_aver = [average_pop(population)]
    stat_aver_sigma = [average_pop_sigma(population)]
    
    for i in range(numb_generations):
        # select parents
        mate_pool = sel_parents(population)
    # Variation
    # ------ Crossover
        parents = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            children = recombination(indiv_1,indiv_2, prob_cross, domain)
            parents.extend(children) 
    # ------ Mutation
        descendants = []
        for cromo,fit in parents:
            new_indiv = mutation(cromo,prob_mut,domain)
            descendants.append((new_indiv,fitness_func(new_indiv)))
    # New population
        population = sel_survivors(population,descendants)
    # Evaluate new population
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population] 
    
    # Statistics
        best_candidate = best_pop(population)
        if best_1[1] > best_candidate[1]:
            best_1 = best_candidate
        stat.append(best_candidate[1])
        stat_sigma.append(average_sigma(best_candidate[0]))
        stat_aver.append(average_pop(population))
        stat_aver_sigma.append(average_pop_sigma(population))
    
    return best_1, stat, stat_aver, stat_sigma, stat_aver_sigma


#Initialize population
def gera_pop(size_pop,domain):
    """
    Representation: ([ xi value, sigmai value ], fitness)
    """
    return [(gera_indiv_float(domain),0) for i in range(size_pop)]

def gera_indiv_float(domain):
    return [[uniform(domain[i][0],domain[i][1]), uniform(domain[i][0],domain[i][1])] for i in range(len(domain))]


# Variation operators: ------ > gaussian float mutation        
def muta_float_gaussian(indiv, prob_muta, domain):
    cromo = indiv[:]
    for i in range(len(cromo)):
        cromo[i][0] = muta_float_gene(cromo[i][0], prob_muta, domain[i], cromo[i][1])
        cromo[i][1] = muta_float_sigma_gene(cromo[i][1], prob_muta, domain[i])
    return cromo

def muta_float_gene(gene,prob_muta, domain_i, sigma_i):
    value = random()
    new_gene = gene
    if value < prob_muta:
        muta_value = gauss(0,sigma_i)
        new_gene = gene + muta_value
        if new_gene < domain_i[0]:
            new_gene = domain_i[0]
        elif new_gene > domain_i[1]:
            new_gene = domain_i[1]
    return new_gene

""" Sigma mutation with uniform distribution and domain based """
def muta_float_sigma_gene(sigma_gene, prob_muta, domain):
    value = random()
    new_sigma = sigma_gene
    if value < prob_muta:
        muta_value = uniform(domain[0], domain[1])
        new_sigma = fabs(sigma_gene + muta_value)
        if new_sigma < domain[0]:
            new_sigma = domain[0]
        elif new_sigma > domain[1]:
            new_sigma = domain[1]
    return new_sigma
    
# Variation Operators : Aritmetical  Crossover
def cross(alpha):
    def aritmetical_cross(indiv_1,indiv_2,prob_cross, domain):
        size = len(indiv_1[0])

        value = random()
        if value < prob_cross:
            cromo_1 = indiv_1[0]
            cromo_2 = indiv_2[0]
            f1 = np.empty([size,2], dtype=float)
            f2 = np.empty([size,2], dtype=float)
            for i in range(size):
                for j in range(2):
                    f1[i][j] = alpha * cromo_1[i][j] + (1 - alpha) * cromo_2[i][j]    
                    f2[i][j] = fabs((1 - alpha) * cromo_1[i][j] + alpha * cromo_2[i][j])
                    f2[i][j] = f2[i][j] if f2[i][j] < domain[i][1] else domain[i][1]

            return ((f1.tolist(),0),(f2.tolist(),0))
        return  indiv_1,indiv_2

    def heristical_cross(indiv_1, indiv_2, prob_cross, domain):
        size = len(indiv_1[0])
        value = random()
        if value < prob_cross:
            alpha2 = (alpha * 3) - 1.5
            best_cromo = indiv_1[0]
            worst_cromo = indiv_2[0]
            if indiv_2[1] < indiv_1[1]:
                best_cromo = indiv_2[0]
                worst_cromo = indiv_1[0]

            f1 = np.empty([size,2], dtype=float)
            f2 = np.empty([size,2], dtype=float)

            for i in range(size):
                for j in range(2):
                    f1[i][j] = alpha2 * (worst_cromo[i][j] - best_cromo[i][j]) + best_cromo[i][j]
                    f2[i][j] = fabs(alpha2 * (best_cromo[i][j] - worst_cromo[i][j]) + best_cromo[i][j])
                    f2[i][j] = f2[i][j] if f2[i][j] < domain[i][1] else domain[i][1]
            return ((f1.tolist(),0),(f2.tolist(),0))
        return indiv_1, indiv_2
    return heristical_cross
        
# Tournament Selection
def tour_sel(t_size):
    def tournament(pop):
        size_pop= len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = tour(pop,t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def tour(population,size):
    """Minimization Problem.Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1))
    return pool[0]

# Survivals: elitism
def sel_survivors_elite(elite):
    def elitism(parents,offspring):
        """Minimization."""
        size = len(parents)
        comp_elite = int(size* elite)
        offspring.sort(key=itemgetter(1))
        parents.sort(key=itemgetter(1))
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism

# Auxiliary
def best_pop(population):
    """Minimization."""
    population.sort(key=itemgetter(1))
    return population[0]
    
def average_pop(population):
    return sum( [fit for cromo,fit in population] )/len(population)

def average_sigma(cromo):
    return sum( [gene[1] for gene in cromo] )/len(cromo)

def average_pop_sigma(population):
    return sum( [average_sigma(indiv[0]) for indiv in population] )/len(population)


if __name__ == '__main__':
    c1 = [1,2,3,4,5]
    c2 = [4,7,2,5,8]
    my_cross = cross(0.3)
    print(my_cross((c1,0), (c2,0),1.0))
    
   