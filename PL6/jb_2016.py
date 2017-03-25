"""

jb_2016.py
The code below is given without any warranty!
Ernesto Costa, February, 2016

"""

from sea_bin_2016_visual import *
from utils_2016 import *
from config import *

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
    parser = argparse.ArgumentParser(
        description='Solves the Joao Brandao Numbers problem using the Simple Evolutionary Algorithm using a binary representation.'
        )
    parser.add_argument(
        '-r', '--runs', type=int, nargs='?',
        help='Number of separate algorithm runs for statistical analysis.')
    parser.add_argument(
        '-p', '--plot', action='store_true',
        help='Turns on plotting capabilities.')
    parser.add_argument(
        '-s', '--save', action='store_true',
        help='Saves plots into files.')
    parser.add_argument(
        '-c', '--config', type=open,
        help='Config file for the SEA Algorithm. If not provided defaults will be used!')
    args = parser.parse_args()
    #print(args) # Uncomment this line to debug the arguments

    # Load configuration file
    config = read_config(args.config)

    # The following calls to get_config will search the provided config file for each variable value
    # if no value is found or the config file is not specified each default value is assumed for each variable
    # "locals()[]"" will get the function by reflection using the function name as key
    prob_muta = get_config(config, ['mutation', 'probability'], 0.01)
    muta_function = locals()[ get_config(config, ['mutation', 'function'], "muta_bin") ]
    
    prob_cross = get_config(config, ['crossover', 'probability'], 0.70)
    cross_function = locals()[ get_config(config, ['crossover', 'function'], "one_point_cross") ] 
    
    tour_size = get_config(config, ['tournament_size'], 3)
    elite_percentage = get_config(config, ['elite_percentage'], 0.1)
    numb_generations = get_config(config, ['number_generations'], 1500)
    size_pop = get_config(config, ['size_population'], 100)
    cromo_size = get_config(config, ['chromosome_size'], 100)

    if args.runs != None:
        boa,stat_average_oa = run(args.runs, numb_generations, size_pop,cromo_size,prob_muta,prob_cross,tour_sel(tour_size),cross_function,muta_function,sel_survivors_elite(elite_percentage), fitness)
        #numb_viola = viola(phenotype(boa[-1]),cromo_size)
        #print('Violations: ',numb_viola)
        #print('Best: ', boa[-1])

        if args.plot:
            display_stat_n(boa,stat_average_oa)
        if args.save:
            file_name = 'stat_n_plot.png'
            print("Saved plot to file '" + file_name + "'.")
            save_stat_n(boa, stat_average_oa, file_name)

    else:
        print("Try with flag -h")
