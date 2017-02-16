"""
Números de João Brandão.

Algoritmo: Hill-climbing
Pertubation: best neighbor
Representation: binary

"""

__author__ = 'Ernesto Costa'
__date__ = 'February 2017'


import random
import math

# Basic Hill Climbing
def jb_hc(problem_size, max_iter,fitness):
    candidate = random_indiv(problem_size)
    cost_candi = fitness(candidate)
    for i in range(max_iter):
        next_neighbor = best_neighbor(candidate,fitness)
        cost_next_neighbor = fitness(next_neighbor)
        if cost_next_neighbor >= cost_candi: 
            candidate = next_neighbor
            cost_candi = cost_next_neighbor      
    return candidate

# Random Restart
def restart(problem_size, max_iter, frequency, fitness):
    candidate = jb_hc(problem_size, frequency, fitness)

    for i in range(1,math.floor(max_iter/frequency) - 1):
        new_candidate = jb_hc(problem_size, frequency, fitness)
        if fitness(new_candidate) > fitness(candidate):
            candidate = new_candidate
    return candidate
     
# Random Individual
def random_indiv(size):
    return [random.randint(0,1) for i in range(size)]

# Best neighbor
def best_neighbor(individual, fitness):
    best = individual[:]
    best[0] = (best[0] + 1) % 2
    for pos in range(1,len(individual)):
        new_individual = individual[:]
        new_individual[pos]= (individual[pos] + 1) % 2
        if fitness(new_individual) > fitness(best):
            best = new_individual
    return best

# Fitness for JB
def evaluate(indiv):
    alfa = 1
    beta = 1.5
    return alfa * sum(indiv) - beta * viola(indiv)

def viola(indiv):
	# count constraint violations
	comp=len(indiv)
	v=0
	for i in range(1,comp):
		limite= min(i,comp - i - 1)
		vi=0
		for j in range(1,limite+1):
			if (indiv[i]==1) and (indiv[i-j]==1) and (indiv[i+j] == 1):
				vi+=1
		v+=vi
	return v  
    
# Auxiliar
def fenotipo(indiv):
    fen = [i+1 for i in range(len(indiv)) if indiv[i] == 1]
    return fen

    
if __name__ == '__main__':
    # For test purposes: beware of the time it may takes...
    #res = fenotipo(jb_hc(10,100,evaluate))
    candidate = restart(100,100,20, evaluate)
    res = fenotipo(candidate)
    quali = viola(candidate)
    print('INDIV: %s\nQUALIDADE: %s\nTAMANHO:%s' % (res, quali,len(res)))
