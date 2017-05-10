"""
sea_bin.py
A very simple EA for float representation.
Ernesto Costa, March 2015 & February 2016
Adjusted by Sebastian Rehfeldt
"""


from random import random,randint, sample, gauss
from operator import itemgetter

# Simple Evolutionary Algorithm     
def sea(numb_generations,size_pop, size_cromo, prob_mut, sigma, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func):
    # initialize population: indiv = (cromo,fit)
    population = gen_pop_func(size_pop,size_cromo)
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
            new_indiv = mutation(cromo,prob_mut,sigma)
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

def sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut, sigma, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func):
    # initialize population: indiv = (cromo,fit)
    population = gen_pop_func(size_pop,size_cromo)
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
            new_indiv = mutation(cromo,prob_mut,sigma)
            descendants.append((new_indiv,fitness_func(new_indiv)))
        # New population
        population = sel_survivors(population,descendants)
        # Evaluate the new population
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]   

        stat.append(best_pop(population)[1])
        stat_aver.append(average_pop(population))

    """
    return: the best individual found
            the population of the final generation
            the best individual from each generation
            the average individual from each generation
    """
    return best_pop(population), population, stat, stat_aver

def run(numb_runs,numb_generations,size_pop, domain, prob_mut, sigma, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func):
    statistics = []
    bestTours = []
    for i in range(numb_runs):
        best, population, stat_best, stat_aver = sea_for_plot(numb_generations,size_pop, domain, prob_mut, sigma, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_pop_func)
        bestTours.append(best)
        statistics.append(stat_best)
        print("{}%".format( (i+1)*100/numb_runs ))
    stat_gener = list(zip(*statistics))
    best = [min(g_i) for g_i in stat_gener] # minimization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return best,aver_gener,bestTours
    

# Initialize population
def gera_pop(size_pop,size_cromo):
    return [(gera_indiv(size_cromo),0) for i in range(size_pop)]

def gera_indiv(size_cromo):
    # random initialization
    indiv = [random() for i in range(size_cromo)]
    return indiv

# Variation operators: ------ > gaussian float mutation     
def muta_float_gaussian(indiv, prob_muta, sigma):
    cromo = indiv[:]
    for i in range(len(cromo)):
        cromo[i] = muta_float_gene(cromo[i],prob_muta, sigma)
    return cromo

def muta_float_uniform(indiv, prob_muta, sigma):
    cromo = indiv[:]
    for i in range(len(cromo)):
        cromo[i] = muta_float_gene(cromo[i],prob_muta, 200)
    return cromo

def muta_float_gene(gene,prob_muta, sigma):
    value = random()
    new_gene = gene
    if value < prob_muta:
        muta_value = gauss(0,sigma)
        new_gene = gene + muta_value
        if new_gene < 0:
            new_gene = 0
        elif new_gene > 1:
            new_gene = 1
    return new_gene




# Variation Operators :Crossover
def one_point_cross(indiv_1, indiv_2,prob_cross):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    cromo_2 = indiv_2[0]
	    pos = randint(0,len(cromo_1))
	    f1 = cromo_1[0:pos] + cromo_2[pos:]
	    f2 = cromo_2[0:pos] + cromo_1[pos:]
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)
	    
def two_points_cross(indiv_1, indiv_2,prob_cross):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    cromo_2 = indiv_2[0]	    
	    pc= sample(range(len(cromo_1)),2)
	    pc.sort()
	    pc1,pc2 = pc
	    f1= cromo_1[:pc1] + cromo_2[pc1:pc2] + cromo_1[pc2:]
	    f2= cromo_2[:pc1] + cromo_1[pc1:pc2] + cromo_2[pc2:]
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)
	
def uniform_cross(indiv_1, indiv_2,prob_cross):
    value = random()
    if value < prob_cross:
        cromo_1 = indiv_1[0]
        cromo_2 = indiv_2[0]
        f1=[]
        f2=[]
        for i in range(0,len(cromo_1)):
            if random() < 0.5:
                f1.append(cromo_1[i])
                f2.append(cromo_2[i])
            else:
                f1.append(cromo_2[i])
                f2.append(cromo_1[i])
        return ((f1,0),(f2,0))
    else:
        return (indiv_1,indiv_2)

	    


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
    pool.sort(key=itemgetter(1), reverse=False)
    return pool[0]




# Survivals Selection: elitism
def sel_survivors_elite(elite):
    def elitism(parents,offspring):
        size = len(parents)
        comp_elite = int(size* elite)
        offspring.sort(key=itemgetter(1), reverse=False)
        parents.sort(key=itemgetter(1), reverse=False)
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism




# Auxiliary
    
def best_pop(population):
    population.sort(key=itemgetter(1),reverse=False)
    return population[0]

def average_pop(population):
    return sum([fit for cromo,fit in population])/len(population)

