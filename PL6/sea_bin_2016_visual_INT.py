"""
sea_bin_visual.py
A very simple EA for binary representation.
Ernesto Costa, March 2015 & February 2016
"""

__author__ = 'Ernesto Costa'
__date__ = 'February 2016'

from jb_2016_INT import viola, phenotype
from math import floor
from random import random,randint, sample, seed
from operator import itemgetter

def run(numb_runs,numb_generations,size_pop, max_cromo_size, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    statistics = []
    for i in range(numb_runs):
        seed(i)
        best, stat_best, stat_aver = sea_for_plot(numb_generations,size_pop, max_cromo_size, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func)
        statistics.append(stat_best)
        write_run(best)
        print('Percentagem: ' + str( ((i+1)*100) / numb_runs) )
    stat_gener = list(zip(*statistics))
    boa = [max(g_i) for g_i in stat_gener] # maximization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return boa,aver_gener

def write_run (indiv):
    num_viola = viola(phenotype(indiv[0]), len(indiv[0]))
    f = open('jb_runs.out', 'a+')
    f.write('Fitness: ' + str(indiv[1]) + '. Nº Elements: ' + str(len(indiv[0])) + ' Nº Violations: ' + str(num_viola) + '\n')
    f.close()

# Simple [Binary] Evolutionary Algorithm		
def sea(numb_generations,size_pop, max_cromo_size, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    # inicialize population: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,max_cromo_size)
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
        for indiv,fit in progenitores:
            novo_indiv = mutation(indiv,prob_mut)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Evaluate the new population
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]     
    return best_pop(populacao)


# Simple [Binary] Evolutionary Algorithm 
# Return the best plus, best by generation, average population by generation
def sea_for_plot(numb_generations,size_pop, max_cromo_size, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    # inicializa população: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,max_cromo_size)
    # avalia população
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]
    
    # para a estatística
    stat = [best_pop(populacao)[1]]
    stat_aver = [average_pop(populacao)]
    
    for i in range(numb_generations):
        # selecciona progenitores
        mate_pool = sel_parents(populacao)
	    # Variation
	    # ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            cromo_1= mate_pool[i]
            cromo_2 = mate_pool[i+1]
            filhos = recombination(cromo_1,cromo_2, prob_cross)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in progenitores:
            novo_indiv = mutation(indiv,max_cromo_size,prob_mut)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Avalia nova _população
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao] 
	
	# Estatística
        stat.append(best_pop(populacao)[1])
        stat_aver.append(average_pop(populacao))
        ##print ("Best individual: {0} -- Avg population: {1}".format(stat[-1], stat_aver[-1]))
	
    return best_pop(populacao),stat, stat_aver


# Initialize population
def gera_pop(size_pop,max_cromo_size):
    return [(gera_indiv(max_cromo_size),0) for i in range(size_pop)]

def gera_indiv(max_cromo_size):
    # Random initialization
    # The individual is a set of numbers
    indiv = [i+1 for i in range(max_cromo_size) if randint(0,1) == 1]
    return indiv

# Variation operators: Integer mutation 

def muta_int_upd(indiv, max_cromo_size, prob_muta):
    # Mutation by gene, changing one value
    cromo = indiv[:]
    for i in range(len(indiv)):
        cromo[i] = muta_new_val(indiv, max_cromo_size)
    return cromo

def muta_int_del(indiv, max_cromo_size, prob_muta):
    cromo = indiv[:]
    for i in range(len(indiv)):
        value = random()
        if value < prob_muta:
            cromo.remove(i+1)
    return cromo

def muta_int_add(indiv, max_cromo_size, prob_muta):
    cromo = indiv[:]
    value = random()
    if value < prob_muta:
        cromo.append(muta_new_val(indiv, max_cromo_size))
    return cromo

def muta_new_val(indiv, max_cromo_size):
    # Return a new unique value for the given individual
    # This allow us to avoid repeated values on the individuals
    val = randint(1, max_cromo_size)
    while val in indiv:
        val = randint(1, max_cromo_size)
    return val

# Variation Operators :Crossover
def max_size_cross(indiv_1, indiv_2, prob_cross):
    value = random()
    cromo_1 = indiv_1[0]
    cromo_2 = indiv_2[0]
    if value < prob_cross:
        size = max(len(indiv_1), len(indiv_2))
        size_1 = floor(size / 2)
        size_2 = size - size_1

        # To avoid having repeated values in the individuals, we apply the SET
        # Having repeated values would be a really big issue. 
        # They I'll have to be removed or penalized. In this case, we remove them.
        # This means, the size of the children might be smaller than expected.
        child_1 = list(set(sample(cromo_1, size_1) + sample(cromo_2, size_2)))
        child_2 = list(set(sample(cromo_1, size_2) + sample(cromo_2, size_1)))
        return ((child_1,0), (child_2,0))
    else:
        return (indiv_1, indiv_2)
	    
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
def display(indiv, phenotype):
    print('Chromo: %s\nFitness: %s' % (phenotype(indiv[0]),indiv[1]))
    
def best_pop(populacao):
    populacao.sort(key=itemgetter(1),reverse=True)
    return populacao[0]

def average_pop(populacao):
    return sum([fit for cromo,fit in populacao])/len(populacao)
    
# -------------------  Problem Specific Definitions  ------------  
# -------------------  One max problem --------------------------

def merito(indiv):
    # wrapper for fitness evaluation
    return evaluate(fenotipo(indiv))

def fenotipo(indiv):
    return indiv


def evaluate(indiv):
    return sum(indiv)

if __name__ == '__main__':
    #to test the code with oneMax function
    prefix = '/Users/ernestojfcosta/tmp/'
    best_1 = sea(100, 20,100,0.01,0.9,tour_sel(3),one_point_cross,muta_bin,sel_survivors_elite(0.02), merito)
    display(best_1,fenotipo)