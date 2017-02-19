"""
Numeros de Joao Brandao.

Algoritmo: Simulated Annealing
Pertubation: Random Neighbor
Representation: binary

Based on work by Ernesto Costa
"""

__author__ = 'Ernesto Costa'
__date__ = 'February 2017'


import random
import math
import matplotlib.pyplot as plt

bad_decisions_in_life = 0
candidates_fitness = []
candidates_length = []
temperature_values = []

# Simulated Annealing
def jb_simulated_annealing(problem_size, max_iter,fitness):
    global bad_decisions_in_life
    global candidates
    global temperature_values

    candidate = random_indiv(problem_size)
    cost_candi = fitness(candidate)
    for i in range(max_iter):
        candidates_fitness.append(cost_candi)
        candidates_length.append(len(fenotipo(candidate)))

        next_neighbor = random_neighbor(candidate,fitness)
        cost_next_neighbor = fitness(next_neighbor)

        temp = calculate_temperature(i) 
        temperature_values.append(temp)
        cost_dif = cost_next_neighbor - cost_candi

        print("\nCost of neighbor is %d, the candidate is %d, difference is %d" % (cost_next_neighbor, cost_candi, cost_dif))
        print("The Prob was %f = exp(%f) = exp(%f/%f)" % (math.exp(cost_dif/temp), cost_dif/temp, cost_dif, temp)) if cost_dif < 0 else 0

        if cost_next_neighbor >= cost_candi: 
            print("Neighbor is better!")
            candidate = next_neighbor
            cost_candi = cost_next_neighbor

        elif math.exp(cost_dif/temp) > random.random(): 
            print("Choosed a bad neighbor!")
            candidate = next_neighbor
            cost_candi = cost_next_neighbor
            bad_decisions_in_life += 1

    return candidate

def calculate_temperature(t):
    k = 100
    r = 0.01
    return k*math.exp(-r*t)
     
# Random Individual
def random_indiv(size):
    return [random.randint(0,1) for i in range(size)]

# Random neighbor
def random_neighbor(individual, fitness):
    neighbor = individual[:]
    position = random.randint(0,len(neighbor) - 1)
    neighbor[position] = (neighbor[position] + 1) % 2
    return neighbor

# Neighbor Solution
def neighbor_solution(individual, fitness):
    solution = individual[:]
    for x in range(2):
        pos = random.randint(0, len(individual)-1)
        solution[pos]= (solution[pos] + 1) % 2
    
    return solution

# Fitness for JB
def evaluate(indiv):
    alfa = 1
    beta = 1.2
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


def display_function(fitness_values, length_values, max_iter):
    x = list(range(max_iter))
    plt.title("Candidates")
    plt.grid(True)
    plt.axhline(c="black")
    plt.axvline(c="black")
    plt.xlabel("X= iterations")
    #plt.ylabel("Y")
    plt.plot(x,fitness_values, "r", label='Candidate Fitness')
    plt.plot(x,length_values, "b", label='Candidate Length')
    plt.plot(x,temperature_values, "g", label='Temperature')
    plt.legend()
    plt.show()

    
if __name__ == '__main__':
    # For test purposes: beware of the time it may takes...
    max_iterations = 1000
    res = jb_simulated_annealing(100,max_iterations,evaluate)
    indiv = fenotipo(res)
    quali = viola(res)

    print('\nINDIV: %s\nQUALIDADE: %s\nTAMANHO:%s' % (indiv, quali,len(indiv)))
    print('Bad decisions made %d/%d (%d%%)' % (bad_decisions_in_life, max_iterations,bad_decisions_in_life/max_iterations*100))

    display_function(candidates_fitness, candidates_length, max_iterations)