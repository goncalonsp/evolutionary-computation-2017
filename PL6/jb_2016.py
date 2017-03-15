"""

jb_2016.py
The code below is given without any warranty!
Ernesto Costa, February, 2016

"""

from sea_bin_2016_visual import *
from utils_2016 import *

# João Brandão

def fitness(indiv):
    return evaluate(phenotype(indiv), len(indiv))

def phenotype(indiv):
    fen = [i+1 for i in range(len(indiv)) if indiv[i] == 1]
    return fen


def evaluate(indiv, comp):
    alfa = 1.0
    beta = 1.1
    return alfa * len(indiv) - beta * viola(indiv,comp)

def viola(indiv,comp):
    # Count violations
    v = 0
    for elem in indiv:
	    limite = min(elem-1,comp-elem)
	    vi = 0
	    for j in range(1,limite+1):
		    if ((elem - j) in indiv) and ((elem+j) in indiv):
			    vi += 1
	    v += vi
    return v

def write_run (indiv):
	f = open('jb_runs.out', 'a+')
	f.write(str(indiv) + '\n')
	f.close()


if __name__ == '__main__':
	n_runs = 30
	generations = 1500
	pop_size = 100
	cromo_size = 100
	prob_muta = 0.01 #0.001, 0.05, 0.1
	prob_cross = 0.75
	tour_size = 3
	elite_percent = 0.1
	#run(numb_runs,numb_generations,size_pop, size_cromo, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
	best,stat,stat_average = run(n_runs, generations, pop_size,cromo_size,prob_muta,prob_cross,tour_sel(tour_size),one_point_cross,muta_bin,sel_survivors_elite(elite_percent), fitness)
	numb_viola = viola(phenotype(best),cromo_size)
	print('Violations: ',numb_viola)
	print('Best: ', best)

	display_stat_1(stat,stat_average)
    