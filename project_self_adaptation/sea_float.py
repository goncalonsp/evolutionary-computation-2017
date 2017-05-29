#! /usr/bin/env python

"""
sea_float.py
A very simple EA for float representation.
Ernesto Costa, February 2016
"""

__author__ = 'Ernesto Costa'
__date__ = 'February 2016'

import numpy as np
import matplotlib.pyplot as plt
from random import random,randint,uniform, sample, shuffle,gauss
from operator import itemgetter



# For the statistics
def run(numb_runs,numb_generations,size_pop, domain, prob_mut, sigma, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    statistics = []
    best_1 = [0,1000] # minimization

    for i in range(numb_runs):
        best, stat_best, stat_aver = sea_for_plot(numb_generations, size_pop, domain, prob_mut, sigma, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func)
        statistics.append(stat_best)
        if best_1[1] > best[1]: # minimization
            best_1 = best

    stat_gener = list(zip(*statistics))
    boa = [min(g_i) for g_i in stat_gener] # minimization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return best_1, boa, aver_gener
    
def run_for_file(filename,numb_runs,numb_generations,size_pop, domain, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    with open(filename,'w') as f_out:
        for i in range(numb_runs):
            best = sea_float(numb_generations,size_pop, domain, prob_mut,sigma, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func)
            f_out.write(str(best[1])+'\n')


# Simple [Float] Evolutionary Algorithm    
def sea_float(numb_generations,size_pop, domain, prob_mut, sigma, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    """
    initialize population: indiv = (cromo,fit)
    domain = [...-,[inf_i, sup_i],...]
    sigma = [..., sigma_i, ...]
    """
    
    populacao = gera_pop(size_pop,domain)
    # evaluate population
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]
    for i in range(numb_generations):
        # sparents selection
        mate_pool = sel_parents(populacao)
    # Variation
    # ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            filhos = recombination(indiv_1,indiv_2, prob_cross)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for cromo,fit in progenitores:
            novo_indiv = mutation(cromo,prob_mut, domain,sigma)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Evaluate the new population
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]     
    return best_pop(populacao)

def sea_for_plot(numb_generations,size_pop, domain, prob_mut,sigma,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    # inicializa população: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,domain)
    # avalia população
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]
    
    # para a estatística
    best_1 = best_pop(populacao)
    stat = [best_1[1]]
    stat_aver = [average_pop(populacao)]
    
    for i in range(numb_generations):
        # selecciona progenitores
        mate_pool = sel_parents(populacao)
    # Variation
    # ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            filhos = recombination(indiv_1,indiv_2, prob_cross)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for cromo,fit in progenitores:
            novo_indiv = mutation(cromo,prob_mut,domain,sigma)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Avalia nova _população
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao] 
    
    # Estatística
        best_candidate = best_pop(populacao)
        if best_1[1] > best_candidate[1]:
            best_1 = best_candidate
        stat.append(best_candidate[1])
        stat_aver.append(average_pop(populacao))
    
    return best_1, stat, stat_aver


#Initialize population
def gera_pop(size_pop,domain):
    return [(gera_indiv_float(domain),0) for i in range(size_pop)]

def gera_indiv_float(domain):
    return [uniform(domain[i][0],domain[i][1]) for i in range(len(domain))]


# Variation operators: ------ > gaussian float mutation        
def muta_float_gaussian(indiv, prob_muta, domain, sigma):
    cromo = indiv[:]
    for i in range(len(cromo)):
        cromo[i] = muta_float_gene(cromo[i],prob_muta, domain[i], sigma[i])
    return cromo

def muta_float_uniform(indiv, prob_muta, domain, sigma):
    cromo = indiv[:]
    for i in range(len(cromo)):
        value = random()
        if value < prob_muta:
            cromo[i] = uniform(domain[i][0], domain[i][1])
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
    
    
# Variation Operators : Aritmetical  Crossover
def cross(alpha):
    def aritmetical_cross(indiv_1,indiv_2,prob_cross):
        size = len(indiv_1[0])
        value = random()
        if value < prob_cross:
            cromo_1 = indiv_1[0]
            cromo_2 = indiv_2[0]
            f1 = [None] * size
            f2 = [None] * size
            for i in range(size):
                f1[i] = alpha * cromo_1[i] + (1 - alpha) * cromo_2[i]
                f2[i] = (1 - alpha) * cromo_1[i] + alpha * cromo_2[i]
            return ((f1,0),(f2,0))
        return  indiv_1,indiv_2

    def heristical_cross(indiv_1, indiv_2, prob_cross):
        size = len(indiv_1[0])
        value = random()
        if value < prob_cross:
            alpha2 = (alpha * 3) - 1.5
            best_cromo = indiv_1[0]
            worst_cromo = indiv_2[0]
            if indiv_2[1] > indiv_1[1]:
                best_cromo = indiv_2[0]
                worst_cromo = indiv_1[0]

            f1 = [None] * size
            f2 = [None] * size
            for i in range(size):
                f1[i] = alpha2 * (worst_cromo[i] - best_cromo[i]) + best_cromo[i]
                f2[i] = alpha2 * (best_cromo[i] - worst_cromo[i]) + best_cromo[i]
            return ((f1,0),(f2,0))
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
def best_pop(populacao):
    """Minimization."""
    populacao.sort(key=itemgetter(1))
    return populacao[0]
    
def average_pop(populacao):
    return sum([fit for cromo,fit in populacao])/len(populacao)


if __name__ == '__main__':
    c1 = [1,2,3,4,5]
    c2 = [4,7,2,5,8]
    my_cross = cross(0.3)
    print(my_cross((c1,0), (c2,0),1.0))
    
   