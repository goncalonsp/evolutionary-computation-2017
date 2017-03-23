"""

jb_2016.py
The code below is given without any warranty!
Ernesto Costa, February, 2016

"""

from sea_bin_2016_visual_INT import *
from utils_2016 import *

# João Brandão

def fitness(indiv):
    return evaluate(phenotype(indiv), len(indiv))

def phenotype(indiv):
    # The phenotype is the same as the genotype
    return indiv


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
	max_cromo_size = 30
	prob_muta = 0.01 #0.001, 0.05, 0.1
	prob_cross = 0.70
	tour_size = 3
	elite_percent = 0.1

	boa,stat_average_oa = run(n_runs, generations, pop_size,max_cromo_size,prob_muta,prob_cross,tour_sel(tour_size),max_size_cross,muta_int_add,sel_survivors_elite(elite_percent), fitness)
	#numb_viola = viola(phenotype(boa[-1]),max_cromo_size)
	#print('Violations: ',numb_viola)
	#print('Best: ', boa[-1])

	display_stat_n(boa,stat_average_oa)
