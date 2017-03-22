#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
sgp_alunos_2016.py
Implementation of GP. Simple version. Inspired by tinyGP by R. Poli 
Ernesto Costa, March 2012
Adapted for Python 3 -  March 2015
Revised for runs - March 2016

Individuals are represented by a pair [indiv,fit]
where indiv is an individual represented recursively as a list of lists. For example, f(t_1,...,t_n)
is represented as [f, rep(t_1), ..., rep(t_n)]

"""
import matplotlib.pyplot as plt
from random import random, choice,uniform,sample, seed
from types import FunctionType
from operator import itemgetter
from copy import deepcopy
import math
import os
from utils import *

MIN_RND = -5
MAX_RND = 5

# Evolver
def sgp(problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,seed_=False):
    """ 
    Problem dependent data, i.e., terminal set, function set and fitness cases are kept in a file.       
    Could be implemented as a class object...

    
    problem = file name where the data for the problem are stored
    num_gen = number of generations
    pop_size = population size
    in_max_depth = max depth for initial individuals
    max_len = maximum number of nodes
    prob_mut_node = mutation probability for node mutation
    prob_cross = crossover probability (mutation probability = 1 - prob_cross)
    t_size = tournament size
    seed = define seed for the random generator. Default = False.

    """
    # initialize the random numbers generator
    if seed_:
        seed(123456789)	
    # Extract information about the problem.  problem is the name of
    # the file where that information is stored
    # Fitness Cases = [[X1,...,Xn Y], ...]
    fit_cases = get_fit_cases(problem)
    # Header = Numb_Input_Vars, Function_Set
    numb_vars, function_set = get_header(problem)
    vars_set = generate_vars(numb_vars)
    ephemeral_constant = 'uniform(MIN_RND,MAX_RND)'
    const_set = [ephemeral_constant]
    terminal_set = vars_set + const_set
    # Define initial population
    chromosomes = ramped_half_and_half(function_set,terminal_set,pop_size, in_max_depth)
    # Evaluate population
    population = [[chromo,evaluate(chromo,fit_cases)] for chromo in chromosomes]
    best_indiv,best_fitness = best_indiv_population(population)

    #statistics
    stat = [best_fitness]
    stat_aver = [avg_indiv_population(population)]

    print('Best at Generation %d:\n%s\nFitness: %s\n----------------' % (0,best_indiv,best_fitness))
    # Evolve
    for i in range(numb_gen):
        # offspring after variation
        offspring = []
        for j in range(pop_size):
            if random() < prob_cross:
		# subtree crossover
                parent_1 = tournament(population,t_size)[0]
                parent_2 = tournament(population,t_size)[0]
                new_offspring = subtree_crossover(parent_1, parent_2)
            else: # prob mutation = 1 - prob crossover!
		# mutation
                parent = tournament(population,t_size)[0]
                new_offspring = point_mutation(parent,prob_mut_node, function_set, vars_set,const_set)
            offspring.append(new_offspring)
        # Evaluate new population (offspring)
        offspring = [[chromo,evaluate(chromo,fit_cases)] for chromo in offspring]
        # Merge parents and offspring
        population = survivors_generational(population,offspring)
		# Statistics
        best_indiv,best_fitness = best_indiv_population(population)

        stat.append(best_fitness)
        stat_aver.append(avg_indiv_population(population))
    
    print('FINAL BEST\n%s\nFitness ---> %f\n\n' % (best_indiv,best_fitness))
    return best_fitness, best_indiv, stat, stat_aver

# ------------------------------  Variants
def sgp_for_single_plot(problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,seed_=False):
    """ To be implemented by you."""
    pass

def sgp_for_plot(problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,seed_=False):
    """ To be implemented by you."""
    pass

def sgp_for_plot_survivors(problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,seed_=False):
    """ To be implemented by you."""
    pass


# ----------------------------- Function Set Wrappers    
def add_w(x,y):
	return x + y

def mult_w(x,y):
	return x * y
    
def sub_w(x,y):
    return x -y

def div_prot_w(x,y):
    if abs(y) <= 1e-3:
        return 1
    else:
        return x/y
# --------------------------------------- Variation operators
# Crossover
def sub_tree(tree,position):
    def sub_tree_aux(tree,position):
        global count
        if position == count:
            count = 0
            return tree
        else:
            count += 1
            if isinstance(tree,list):
                for i,sub in enumerate(tree[1:]):
                    res_aux = sub_tree(sub, position)
                    if res_aux:
                        break
                return res_aux
    return sub_tree_aux(tree,position)

def replace_sub_tree(tree, sub_tree_1, sub_tree_2):
    if tree == sub_tree_1:
        return sub_tree_2
    elif isinstance(tree, list):
        for i,sub in enumerate(tree[1:]):
            res = replace_sub_tree(sub, sub_tree_1, sub_tree_2)
            if res and (res != sub):
                return [tree[0]] + tree[1:i+1] + [res] + tree[i+2:]
        return tree
    else:
        return tree


def subtree_crossover(par_1,par_2):
    """ATENTION:if identical sub_trees it replaces the first ocorrence..."""
    # Choose crossover point (indepently)
    size_1 = indiv_size(par_1)
    size_2 = indiv_size(par_2)
    cross_point_1 = choice(list(range(size_1)))
    cross_point_2 = choice(list(range(size_2)))
    # identify subtrees to echange
    sub_tree_1 = sub_tree(par_1, cross_point_1)
    sub_tree_2 = sub_tree(par_2, cross_point_2)
    # Exchange
    new_par_1 = deepcopy(par_1)
    offspring = replace_sub_tree(new_par_1, sub_tree_1,sub_tree_2)
    return offspring


# Mutation
def point_mutation(par, prob_mut_node, func_set, vars_set,const_set):
    par_mut = deepcopy(par)
    if random() < prob_mut_node:
        if isinstance(par_mut,list):
	    # Function
            symbol = par_mut[0]
            return [change_function(symbol, func_set)] + [point_mutation(arg, prob_mut_node, func_set, vars_set,const_set) for arg in par_mut[1:]]
        elif isinstance(par_mut, (float, int)):
	    # It's a constant
            return eval(const_set[0])
        elif var_b(par_mut): 
	    # It's a variable
            return change_variable(par_mut,vars_set)
        else:
            raise TypeError # should not happen
    return par_mut


def change_function(symbol, function_set):
    new_function = choice(function_set)
    while (new_function[0] == symbol) or (new_function[1] != arity(symbol,function_set)):
        new_function = choice(function_set)
    return new_function[0]

def arity(symbol,function_set):
    for func in function_set:
        if func[0] == symbol:
            return func[1]	
                                              

def change_variable(variable,vars_set):
    if len(vars_set) == 1:
        return variable
    new_var = choice(vars_set)
    while new_var == variable:
        new_var = choice(vars_set)
    return new_var


# ------------------------------------- Population
# Generate an individual: method full or grow
# FGGP: algorithm 2.1, pg.14
def gen_rnd_expr(func_set,term_set,max_depth,method):
	"""Generation of tree structures using full or grow."""
	if (max_depth == 0) or (method == 'grow' 
	                        and (random() < 
	                             (len(term_set) / (len(term_set) + len(func_set))))):
		index = choice(list(range(len(term_set))))
		if index == (len(term_set) - 1) : 
		    # ephemeral constant
		    ephemeral_const = term_set[index]
		    expr = eval(ephemeral_const)
		else:
		    # variable: 'Xn'
		    expr = term_set[index]
	else:
		func=choice(func_set)
		# func = [name_function, arity]
		expr = [func[0]] +  [gen_rnd_expr(func_set,term_set, max_depth -1, method) 
		              for i in range(int(func[1]))]
	return expr
	

# Method ramped half-and-half.	
def ramped_half_and_half(func_set,term_set,size, max_depth):
	depth=list(range(3,max_depth))
	pop=[]
	for i in range(size//2):
		pop.append(gen_rnd_expr(func_set,term_set,choice(depth),'grow'))
	for i in range(size//2):
		pop.append(gen_rnd_expr(func_set,term_set,choice(depth),'full'))
	if (size % 2 ) != 0:
	    pop.append(gen_rnd_expr(func_set,term_set,choice(depth),'full'))
	return pop
 
# ------------------------------------------ Parents' Selection

def tournament(population,size):
    """Maximization Problem.Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]

# ---------------------------------------------- Survivors' Selection

def survivors_generational(population,offspring):
    """Change all population with the new individuals."""
    return offspring

def survivors_elite(elite_size):
    """To be implemented by you."""
    pass

def survivors_best():
    """To be implemented by you."""
    pass
	
	
# ------------------------------------------------ Fitness Evaluation
def evaluate(individual,fit_cases):
    """ 
    Evaluate an individual. *** Maximization ***
    Gives the inverse of the sum of the absolute error for each fitness cases.
    fit_cases = [[X1, ..., XN, Y], ...]
    The smaller the error the better the fitness.
    """
    indiv = deepcopy(individual)
    error = 0
    for case in fit_cases:
        result = interpreter(indiv, case[:-1])
        error += abs(result - case[-1])
    return 1.0 / (1.0 + error)

# Interpreter. FGGP, algorithm 3.1 - pg.25
def interpreter(indiv,variables):
    if isinstance(indiv,list) :
        func = eval(indiv[0])
        if isinstance(func, FunctionType) and (len(indiv) > 1): 
	    # Function: evaluate
            value = func(*[interpreter(arg,variables) for arg in indiv[1:]])
        else:
	    # Macro: don't evaluate arguments
            value = indiv
    elif isinstance(indiv, (float, int)):
	# It's a constant
        value = indiv 
    elif var_b(indiv): 
	# It's a variable
        index = get_var_index(indiv)
        value = variables[index] # binding value
    elif isinstance(eval(indiv), FunctionType):
	# Terminal 0-ary function: execute
        value = eval(indiv)(*())
    return value

# get data
def get_fit_cases(file_problem):
    f_in = open(file_problem,'r')
    data = f_in.readlines()
    f_in.close()
    fit_cases_str = [ case[:-1].split() for case in data[1:]]
    fit_cases = [[float(elem) for elem in case] for case in fit_cases_str]
    return fit_cases

def get_header(file_problem):
    f_in = open(file_problem)
    header_line = f_in.readline()[:-1]
    f_in.close()
    header_line = header_line.split()
    header = [int(header_line[0])] + [[ [header_line[i], int(header_line[i+1])]
                                  for i in range(1,len(header_line),2)]]
    return header
    
def get_var_index(var):
    return int(var[1:])

def generate_vars(n):
    """ generate n vars, X1, ..., Xn."""
    vars_set = []
    for i in range(n):
        vars_set.append('X'+str(i))
    return vars_set

def var_b(name):
    """Test: is name a variable?"""
    return isinstance(name, str) and (name[0]== 'X') and (name[1:].isdigit())

        
def indiv_size(indiv):
    """ Number of nodes of an individual."""
    if not isinstance(indiv, list):
        return 1
    else:
        return 1 + sum(map(indiv_size, indiv[1:]))
    
def best_indiv_population(population):
    # max value of fitness 
    all_fit_values = [indiv[1] for indiv in population]
    max_fit = max(all_fit_values)
    # index max value
    index_max_fit = all_fit_values.index(max_fit)
    # find indiv
    return population[index_max_fit]

    
def avg_indiv_population(population):
    # avg value of fitness 
    all_fit_values = [indiv[1] for indiv in population]
    return sum(all_fit_values)/len(all_fit_values)

def run_for_plot(num_runs,target,problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size,seed=False):
	"""To be implemented by you."""
	pass
	
def run_for_plot_survivors(num_runs,target,problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, t_size, survivors, seed=False):
	"""To be implemented by you."""
	pass
    
# display 
def display_one_run(data,titulo):
    """To be implemented by you."""  
    pass


def plot_data(file_name, name,body,indiv,loc='best'):
    with open(file_name) as f_in:
        f_in = open(file_name)
        # read fitness cases
        data = f_in.readlines()[1:]
        f_in.close()
        # plot
        values_x = [float(line[:-1].split()[0]) for line in data]
        values_y = [float(line[:-1].split()[-1]) for line in data]
        calculated_values_y = [interpreter(indiv,x) for x in values_x]
        
        plt.ylabel('Value')
        plt.xlabel('Input Values')
        plt.title(name)
        p = plt.plot(values_x,values_y,'r-o',label=str(body))
        p = plt.plot(values_x,calculated_values_y,'b-o',label="regression")
        plt.legend(loc= loc)
        plt.show()


if __name__ == '__main__':
    # my file prefix
    prefix = os.path.dirname(os.path.realpath(__file__)) +'/'
    filename_1 = 'data_symb.txt'
    file_name_2 = 'data_sin.txt'
    # parameters
    count = 0
    numb_runs = 10
    problem = prefix+ filename_1 #change function
    numb_gen = 10
    pop_size = 50
    in_max_depth = 6
    max_len = 1000
    prob_mut_node = 0.01
    prob_cross = 0.8
    tour_size = 3
    elite_size = 0.05
    seed=False
    
    survivors = survivors_generational
    #survivors = survivors_elite(elite_size)
    #survivors = survivors_best
    
    best,best_indiv,stat,stat_aver = sgp(problem,numb_gen,pop_size,in_max_depth,max_len,prob_mut_node,prob_cross,tour_size, seed)
    #display_stat_1(stat,stat_aver)
    plot_data(problem,'Symbolic Regression','x**2 + x + 1',best_indiv,'lower right')
    #results = sgp_for_single_plot(problem,numb_gen,pop_size, in_max_depth, max_len,prob_mut_node, prob_cross, tour_size,seed_=False)
    #display_one_run(results,'Symbolic Regression')
    #run_for_plot(numb_runs,'Simbolic Regression',problem,numb_gen,pop_size,in_max_depth,max_len,prob_mut_node,prob_cross,tour_size, seed)
    #run_for_plot_survivors(numb_runs,'Simbolic Regression',problem,numb_gen,pop_size,in_max_depth,max_len,prob_mut_node,prob_cross,tour_size, survivors,seed)
    

  