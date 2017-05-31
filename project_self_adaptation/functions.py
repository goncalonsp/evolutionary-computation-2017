"""
functions.py
Function optimization.
Gabriel Rodrigues & Gonçalo Pereira, 2017
"""
__author__ = 'Gabriel Rodrigues & Gonçalo Pereira'
__date__ = 'May 2017'

from utils import *
from random import gauss
import numpy as np

RASTRIGIN_DOMAIN = np.array([-5.12, 5.12])
DE_JONG_F1_DOMAIN = RASTRIGIN_DOMAIN
DE_JONG_F4_DOMAIN = np.array([-1.28, 1.28])
SCHWEFEL_DOMAIN = np.array([-500,500])
PLOT_SPACING = 0.05
PLOT_SCHWEFEL_SPACING = 2.0

# Evaluation functions
def de_jong_f1_eval (x):
    w = np.array(x)
    return sum( w**2 )

def de_jong_f4_eval (x):
    w = np.array(x)
    calc_r = lambda vi,i: i * vi**4
    r = np.fromiter((calc_r(wi,i) for i, wi in enumerate(w)), np.float, w.size)
    return sum( r ) + gauss(0,1)

def schwefel_eval (x):
    w = np.array(x)
    return sum( -w * np.sin( np.absolute(w)**(1/2)) )

def rastrigin_eval (x):
    A = 10
    w = np.array(x)
    n = w.size
    return A * n + sum( (w**2 - A * np.cos(2*np.pi*w)) )

if __name__ == '__main__':
    # Plot Rastrigin function #
    plot_3d_function(rastrigin_eval, RASTRIGIN_DOMAIN, PLOT_SPACING)

    # Plot De Jong F1 function #
    plot_3d_function(de_jong_f1_eval, DE_JONG_F1_DOMAIN, PLOT_SPACING)

    # Plot De Jong F4 function #
    plot_3d_function(de_jong_f4_eval, DE_JONG_F4_DOMAIN, PLOT_SPACING)

    # Plot Schwefel function #
    plot_3d_function(schwefel_eval, SCHWEFEL_DOMAIN, PLOT_SCHWEFEL_SPACING)
