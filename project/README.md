# Traveling Thief Problem

## Project Goal

The goal of this project is to implement and test an algorithmic
solution for the Traveling Thief Problem (TTP) mainly based on evolutionary algorithms (EA). The TTP is a combination of the Traveling Salesman Problem (TSP) and the 0/1 Knapsack Problem (KP).

## Problem Definition

_The following was taken from the project description. See attached pdf for the complete project description and formal definitions_

### Traveling Salesman Problem

The TSP involves n cities that a salesman must visit exactly once, minimizing a certain aspect (length of the path, time of the trip). To solve it we must know the localization of the cities or a matrix with the distance between every pair of cities. When time is the criterion we need also to know the velocity of the salesman.

### 0/1 Knapsack Problem

The KP involves a set of `m` items `I1 , . . . , Im` each one with a certain value `(pi)` and weight `(wi)`, that a thief want to put in its knapsack of limited capacity `W`. The goal is to maximize the value without exceeding the knapsack capacity.

### Traveling Thief Problem

The TTP is a combination of the TSP and KP. The thief has to visit exactly once each city, like in the TSP, and when he visit a city he may decide to pick (or not) an item to put in his/her knap-sack, like in the KP. A solution for the TTP is a tour `x` and a picking plan `z = (z1 , . . . , zm )`, `zi ∈ {0 ∪ Ai}`. `Ai` is the set of cities where the item `Ii` is available. If `zi = 0` that means that no item was picked. It is clear that a good solution for the problem will be one that minimizes the time of the trip and maximizes the value of the items in the knapsack.

#### Solved model

From the two proposed models we chosen the TTP1. In this model we want to maximize:

        G(x,z) = g(z) − R × f(x,z)

where `g(z)` is the total value for the picking plan `z`, as it would be computed by the stand-alone `0/1 KP`, `R` is the rent per time unit that the thief as to pay while doing the tour, and `f` is the total time of the tour. The fact that the time depend on the tour and on the picking plan is because the velocity decreases as a function of the weight of the knapsack. In fact the current velocity is given by:

        vc = vmax − Wc × (vmax − vmin) / W

From the formula it is clear that when the knapsack is empty the velocity is maximum and when the knapsack is full the velocity is minimum. On the other hand the rent rate `(R)` per time unit links the time to the value.

## Proposed Approach



## Contents of this project

* `instances/` - Instances used for running the TTP problem;
* `results/` - All results mentioned in the Report, as well as configuration files;
* `README.md` - this file;
* `RUNNING.md` - instructions on how to run all developed scripts and variations;
* `config.py` - configurations library. Loads json files and provides helper functions regarding configuration;
* `config*.json` - complementary configuration examples for the multiple scripts;
* `gen_config_and_run.py` - helper tool for scripts and parameter testing;
* `gen_pop_test.py` - Script to test the impact of different generation population algorithms for TSP using the objective function for TTP;
* `kp.py` - KP EA, heuristics and related helper functions;
* `read_ttp_file.py` - TTP file extension/format reading library;
* `sea_bin_2016_visual.py` - EA algorithm using binary representation, used in KP's EA;
* `sea_tsp_permutation.py` - EA algorithm using permutations representation, used in TSP's EA;
* `sea_tsp_randkey.py` - EA algorithm using random key representation, used in TSP's EA;
* `sea_ttp.py` - EA algorithm using coevolution cooperation, used in TTP's EA;
* `tsp.py` - TSP EA, heuristics and related helper functions;
* `ttp.py` - Heuristic approach for the TTP problem;
* `ttp_ea.py` - TTP EA implementation;
* `utils.py` - Miscellanea library, contains functions to plot and save graphs to file.

## Report 

The in-development report can be found on: https://docs.google.com/document/d/1NOPVEJ6EqHyL5s1EvfdtUGpAVchFqTb-00XmeJZgiY0/edit?usp=sharing


# Disclaimer

Work based on work by Ernesto Costa. 
See each file for appropriate credits.
See Report for Bibliography.