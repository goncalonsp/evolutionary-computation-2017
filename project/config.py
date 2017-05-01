"""
config.py
Goncalo Pereira, May 2017
"""

import argparse
import json

"""         General config          """
use_linkern = False
top_k = 5


"""         TSP config          """
tsp_development = False #set true to analyze EA algorithm for TSP
tsp_plot_generations = True #plots evolution of best and average over generations if true, otherwise it will print best and average best over different runs
tsp_runs = 5
tsp_fitness = "distance"
tsp_interpretation = "simple"
generations =   100 #10000
population =    20 # 200
prob_muta =     0.25
prob_cross =    0.75
sigma =         0.1
tour_size =     5
elite_size =    0.1



"""         File selection          """
"""
files = [{
			"name": "a280_n279_bounded-strongly-corr_01.ttp",
			"tour": "a280.linkern.tour"
		},{
			"name": "a280_n1395_uncorr-similar-weights_05.ttp",
			"tour": "a280.linkern.tour"
		},{
			"name": "a280_n2790_uncorr_10.ttp",
			"tour": "a280.linkern.tour"
		},{
			"name": "fnl4461_n4460_bounded-strongly-corr_01.ttp",
			"tour": "fnl4461.linkern.tour"
		},{
			"name": "fnl4461_n22300_uncorr-similar-weights_05.ttp",
			"tour": "fnl4461.linkern.tour"
		},{
			"name": "fnl4461_n44600_uncorr_10.ttp",
			"tour": "fnl4461.linkern.tour"
		}]
"""

#"""
file = {
			"name": "a280_n279_bounded-strongly-corr_01.ttp",
			"tour": "a280.linkern.tour"
		}
#"""        

def read_config(file):
	if file:
		config = json.load(file)
	else:
		print("Warning: No configuration was provided, default values will be used!")
		config = None
	
	# The following calls to get_config will search the provided config file for each variable value
	# if no value is found or the config file is not specified each default value is assumed for each variable
	# "locals()[]"" will get the function by reflection using the function name as key
	
	global use_linkern
	use_linkern = get_config(config, ['general', 'use_linkern'], False)
	global top_k
	top_k = get_config(config, ['general', 'top_k'], 5)

	global tsp_development
	tsp_development = get_config(config, ['tsp', 'development'], False)
	global tsp_plot_generations
	tsp_plot_generations = get_config(config, ['tsp', 'plot_generations'], True)
	global tsp_runs
	tsp_runs = get_config(config, ['tsp', 'runs'], 5)
	global tsp_fitness
	tsp_fitness = get_config(config, ['tsp', 'fitness'], "distance")
	global tsp_interpretation
	tsp_interpretation = get_config(config, ['tsp', 'interpretation'], "simple")
	
	global generations
	generations = get_config(config, ['tsp', 'number_generations'], 100)
	global population
	population = get_config(config, ['tsp', 'size_population'], 20)
	global prob_muta
	prob_muta = get_config(config, ['tsp', 'mutation', 'probability'], 0.25)
	global prob_cross
	prob_cross = get_config(config, ['tsp', 'crossover', 'probability'], 0.75)
	global sigma
	sigma = get_config(config, ['tsp', 'mutation', 'sigma'], 0.1)
	global tour_size
	tour_size = get_config(config, ['tsp', 'tournament_size'], 5)
	global elite_size
	elite_size = get_config(config, ['tsp', 'elite_percentage'], 0.1)

	return config

def get_config(config, keys, default):
	if not keys: return config
	if not config: return default
	
	if isinstance(config,dict):
		if keys[0] in config: 
			return get_config(config[keys[0]], keys[1:], default)
	if isinstance(config,list):
		if len(config) >= keys[0]:
			return get_config(config[keys[0]], keys[1:], default)

	print("Warning: default value of {} used for configuration {}".format(default, keys))
	return default
	