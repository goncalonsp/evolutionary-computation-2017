"""
Numeros de Joao Brandao.

Algoritmo: Hill-climbing
Pertubation: best neighbor
Representation: binary

Based on work by Ernesto Costa
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

# Simulated Annealing
def simulated_annealing(problem_size, max_iter, ini_temp, fitness):
    candidate = random_indiv(problem_size)
    cost_candi = fitness(candidate)
    temp = ini_temp
    for i in range(max_iter):
        temp = calculate_temperature(temp)
        next_neighbor = random_neighbor(candidate)
        cost_next_neighbor = fitness(next_neighbor)

        if cost_next_neighbor >= cost_candi:
            candidate = next_neighbor
            cost_candi = cost_next_neighbor 
        elif math.exp((cost_candi - cost_next_neighbor)/temp) > random.random() :   
            candidate = next_neighbor
            cost_candi = cost_next_neighbor    
    return candidate

# Calculate Temperature of simulated annealing
def calculate_temperature(temperature):
    return temperature + 1

# Random Individual
def random_indiv(size):
    return [random.randint(0,1) for i in range(size)]

# Random Neighbor
def random_neighbor(individual):
    neighbor = individual[:]
    position = random.randint(0,len(neighbor) - 1)
    neighbor[position] = (neighbor[position] + 1) % 2
    return neighbor

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
    beta = 2.5
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
    # res = fenotipo(jb_hc(10,100,evaluate))
    candidate = simulated_annealing(100,100,1,evaluate)
    res = fenotipo(candidate)
    quali = viola(candidate)
    print('INDIV: %s\nQUALIDADE: %s\nTAMANHO:%s' % (res, quali,len(res)))
