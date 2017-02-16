"""Random Search. For continuous domains.
Inspired by Clever Algorithms (Jason Brownlee)"""

__author__ = 'Ernesto Costa'
__date__ ='January 2017'


import random

def random_search(sp,max_iter):
    best = random_candidate(sp)
    cost_best = fitness(best)
    for i in range(max_iter):
        candidate = random_candidate(sp)
        cost_candi = fitness(candidate)
        if cost_candi < cost_best:
            best = candidate
            cost_best = cost_candi
    return best


def random_candidate(sp):
    return [random.uniform(sp[i][0],sp[i][1]) for i in range(len(sp))]



def fitness(individual):
    """ De Jong F1 or the sphere function"""
    return sum([ x_i ** 2 for x_i in individual])

if __name__ == '__main__':
    # problem
    size = 3
    search_space = [[-5.12,5.12] for i in range(size)]
    # algorithm
    num_iter = 100000
    # search
    best = random_search(search_space,num_iter)
    print best 
        