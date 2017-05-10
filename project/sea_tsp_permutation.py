"""
sea_bin.py
A very simple EA for float representation.
Ernesto Costa, March 2015 & February 2016
Adjusted by Sebastian Rehfeldt
"""


from random import random,randint, sample, gauss, shuffle
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
            new_indiv = mutation(cromo,prob_mut)
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
    # random permutation initialization
    indiv = list(range(1,size_cromo+1))
    shuffle(indiv)
    return indiv

# Variation operators: Permutation Mutation    
def muta_permutation(indiv,prob_muta):
    # Mutation by swapping genes' places
    cromo = indiv[:]
    for i in range(len(indiv)):
        if random() < prob_muta:
            j = randint(0,len(cromo)-1)
            tmp = cromo[i]
            cromo[i] = cromo[j]
            cromo[j] = tmp
    return cromo

# Variation Operators :Crossover
# Credits to:
# http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/CycleCrossoverOperator.aspx
def cycle_crossover(indiv_1, indiv_2, prob_cross):
    value = random()
    if value < prob_cross:
        cromo1 = indiv_1[0]
        cromo2 = indiv_2[0]

        # To keep track of 'seen' indexes
        marked = [False] * len(cromo1)

        # Identify cycles
        cycles = []
        for idx1 in range(0, len(cromo1)):
            cycle = []

            if not marked[idx1]:
                
                # Get the position of the value in indiv 1 in indiv 2
                idx2 = cromo2.index(cromo1[idx1])
                # Add a part of the cycle
                # (the index, indiv 2 index value, indiv 1 index value)
                cycle.append((idx2, cromo2[idx2], cromo1[idx2]))
                # mark the index as seen
                marked[idx2] = True

                # until we loop completely
                while idx2 != idx1:
                    # repeat as above using the index of the indiv 1 value in indiv 2
                    idx2 = cromo2.index(cromo1[idx2])
                    cycle.append((idx2, cromo2[idx2], cromo1[idx2]))
                    marked[idx2] = True

                # add the found cycle
                cycles.append(cycle)

        # Copy the material from the cycles to the offspring
        child1 = [None] * len(cromo1)
        child2 = [None] * len(cromo1)
        # Alternate between each cycle, first for child 1, second for 2
        alt = True
        for cycle in cycles:
            for part in cycle:
                if alt:
                    child1[part[0]] = part[2]
                    child2[part[0]] = part[1]
                else:
                    child1[part[0]] = part[1]
                    child2[part[0]] = part[2]
            alt ^= True

        return ((child1,0),(child2,0))
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

if __name__ == '__main__':
    # run to test cycle crossover
    p1 = ([1, 2, 3, 4, 5, 6, 7, 8, 9],0)
    p2 = ([9, 3, 7, 8, 2, 6, 5, 1, 4],0)
    print("Parent 1: {}".format(p1))
    print("Parent 2: {}".format(p2))
    (c1, c2) = cycle_crossover(p1, p2, 1)
    print("Child  1: {}".format(c1))
    print("Child  2: {}".format(c2))