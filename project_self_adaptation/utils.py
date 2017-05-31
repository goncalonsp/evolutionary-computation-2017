"""
Utilities for visualization
Ernesto Costa, February 2016
Adjusted by Gabriel Rodrigues and Gonçalo Pereira
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import random
import matplotlib.pyplot as plt
from matplotlib import cm

# auxiliary 
def display(indiv, phenotype):
    print('Chromo: %s\nFitness: %s' % (phenotype(indiv[0]),indiv[1]))
    
def display_stat_1(best, average, title='Performance over generations', ylabel='Fitness'):
    generations = list(range(len(best)))
    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel(ylabel)
    plt.plot(generations, best, label='Best')
    plt.plot(generations,average,label='Average')
    plt.legend(loc='best')
    plt.show()

def save_stat_1(best, average, file_name, title='Performance over generations', ylabel='Fitness'):
    generations = list(range(len(best)))
    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel(ylabel)
    plt.plot(generations, best, label='Best')
    plt.plot(generations,average,label='Average')
    plt.legend(loc='best')
    plt.savefig(file_name, bbox_inches='tight')
    
def display_stat_n(boa, average_best, title='Performance over generations', ylabel='Fitness'):
    generations = list(range(len(boa)))
    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel(ylabel)
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.show()

def save_stat_n(boa, average_best, file_name, title='Performance over generations', ylabel='Fitness'):
    generations = list(range(len(boa)))
    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel(ylabel)
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.savefig(file_name, bbox_inches='tight')


def fun(x):
  return x[0]**2 + x[1]

def plot_3d_function(func, domain, spacing):
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(domain[0], domain[1], spacing)
    X, Y = np.meshgrid(x, y)
    zs = np.array([func([x,y]) for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    surface = ax.plot_surface(X, Y, Z, cmap=cm.jet)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    fig.colorbar(surface, shrink=0.5, aspect=5)

    plt.show()

if __name__ == '__main__':
    domain = np.array([-3.0,3.0])
    spacing = 0.05
    plot_3d_function(fun, domain, spacing)