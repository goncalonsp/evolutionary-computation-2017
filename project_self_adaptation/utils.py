"""
Utilities for visualization
Ernesto Costa, February 2016
Adjusted by Gabriel Rodrigues nad Gonçalo Pereira
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import random
import matplotlib.pyplot as plt

# auxiliary 
def display(indiv, phenotype):
    print('Chromo: %s\nFitness: %s' % (phenotype(indiv[0]),indiv[1]))
    
def display_stat_1(best, average):
    generations = list(range(len(best)))
    plt.title('Performance over generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best')
    plt.plot(generations,average,label='Average')
    plt.legend(loc='best')
    plt.show()

def save_stat_1(best, average, file_name):
    generations = list(range(len(best)))
    plt.title('Performance over generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best')
    plt.plot(generations,average,label='Average')
    plt.legend(loc='best')
    plt.savefig(file_name, bbox_inches='tight')
    
def display_stat_n(boa, average_best):
    generations = list(range(len(boa)))
    plt.title('Performance over runs')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.show()

def save_stat_n(boa, average_best, file_name):
    generations = list(range(len(boa)))
    plt.title('Performance over runs')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.savefig(file_name, bbox_inches='tight')


def fun(x, y):
  return x**2 + y

def plot_function(func, ):
    fig = plt.figure()
    
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(-3.0, 3.0, 0.05)
    X, Y = np.meshgrid(x, y)
    zs = np.array([func(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


    
if __name__ == '__main__':
    pass