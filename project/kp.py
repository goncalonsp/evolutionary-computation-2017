"""
kp.py
Sebastian Rehfeldt, April 2017
Gonçalo Pereira, May 2017, KP EA solver
"""
import numpy as np
import sea_bin_2016_visual
from utils import *
from read_ttp_file import readFile
from argparse import ArgumentParser
import config
import math

def get_best_five_items(city, items):
	city_items = items[str(city)]

	# Send only the best 5 items.
	# If there are no more than 5 item, send them all.
	if len(city_items) > 5:
		return sorted(city_items, key=get_item_ratio, reverse=True)[0:5]
	return sorted(city_items, key=get_item_ratio, reverse=True)

def get_item_ratio(item):
	return item[0]/item[1]

def getPackingPlan(items, tour, distmat, params):
	#TODO implement EA algorithm later
	#TODO maybe improve heuristic or use it for basis of EA

	capacity = params["kp_capacity"]
	min_speed = params["min_speed"]
	max_speed = params["max_speed"]
	renting_rate = params["renting_rate"]
	n_items = params["number_of_items"]

	distanceToFinish = []
	cur_dist = 0
	former_city = 0
	#pre-calculate traveling distance from city to end of tour
	#start from back to improve performance (dynamic programming approach)
	for i in range(len(tour)):
		city_id=tour[len(tour)-i-1]

		cur_dist = cur_dist+distmat[former_city,city_id]
		distanceToFinish.append(cur_dist)

		former_city = city_id

	#print(distanceToFinish[len(distanceToFinish)-1]+distmat[former_city,0])
	#should match length of tour

	#reverse order as we started from the back
	distanceToFinish = distanceToFinish[::-1]
	
	#calculate score and fitness value for each item (value-R*time to finish)
	#items will be an array which contains dictionarys (city id, profit, weight, score, fitness)
	#uses simple heuristic from paper "A comprehensive benchmark..."
	scoredItems = np.empty(n_items, dtype=object)
	j = 0
	for i in range(len(tour)):
		city = tour[i]
		dist = distanceToFinish[i]
		for item in items[str(city)]:
			p = item[0]
			w = item[1]

			v = (max_speed-min_speed)/capacity
			speed = max_speed - v*w
			travelTime = dist/speed
			score = p - renting_rate*travelTime
			fitness = renting_rate*dist/max_speed + score

			scoredItems[j] = {
				"city_id": city,
				"profit" : p,
				"weight" : w,
				"score"  : score,
				"fitness": fitness
			}

			j+=1

	#sort items according to
	scoredItems = sorted(scoredItems, key=lambda a: a["score"],reverse=True)

	cur_capacity = 0
	packedItems = {}
	for item in scoredItems:
		city = str(item["city_id"])

		if (cur_capacity+item["weight"]<=capacity) and (item["fitness"]>0):

			keys = list(packedItems.keys())
			if city in keys:
				packedItems[city].append((item["profit"],item["weight"]))
			else:
				packedItems[city] = [(item["profit"],item["weight"])]

			cur_capacity += item["weight"]
		if (cur_capacity==capacity):
			break

	#print(packedItems)
	#print(capacity)
	#print(cur_capacity)


	return packedItems


"""
---------------------------------------------------

Evolutionary Algorithm Implementation for the KS problem

---------------------------------------------------
"""
def fitness(items, params):
	"""
	items  
		is a dictionary where, size N-1 (N number of cities),
		where the key is the city number, range [1;N-1]
		where the value an array of tuples, each representing an item
		each tuple contains 2 values, profit and weight
	params
		is a dictionary with, as an example
		max_speed: 1.0
		edge_weight_type: CEIL_2D
		kp_data_type: [bounded, strongly, corr]
		renting_rate: 5.61
		number_of_items: 279
		problem_name: a280-TTP
		kp_capacity: 25936.0
		min_speed: 0.1
		dimension: 280
	"""
	def fitness_(indiv):
		quali = evaluate(phenotype(indiv), items, params)
		return quali
	return fitness_

def phenotype(indiv):
	"""from a binary string to a list of cities that are in the plan"""
	pheno = [idx+1 for idx, val in enumerate(indiv) if val == 1]
	return pheno

def calc_weight(pheno, items):
	return sum([items[str(city)][0][1] for city in pheno])

def evaluate(pheno, items, params):
	""" pheno = [...,2,243,15,59,...]"""
	total_weight = calc_weight(pheno, items)
	if total_weight > params['kp_capacity']:
		return 0
	return sum([items[str(city)][0][0] for city in pheno])

def evaluate_log(pheno, items, params):
	""" pheno = [...,2,243,15,59,...]"""
	total_weight = calc_weight(pheno, items)
	quality = sum([items[str(city)][0][0] for city in pheno])
	capacity = params['kp_capacity']
	if total_weight > capacity:
		rho = max([items[str(city)][0][0]/items[str(city)][0][1] for city in pheno])
		quality -= math.log(1 + rho * (total_weight - capacity),2)
	return quality

def evaluate_quadratic(pheno, items, params):
	""" pheno = [...,[id,weight,value],...]"""
	total_weight = calc_weight(pheno, items)
	quality = sum([items[str(city)][0][0] for city in pheno])
	capacity = params['kp_capacity']
	if total_weight > capacity:
		rho = max([items[str(city)][0][0]/items[str(city)][0][1] for city in pheno])
		quality -=  (rho * (total_weight - capacity))**2
	return quality

def kp_ea_solver(items, params, configs):
	capacity = params["kp_capacity"]
	min_speed = params["min_speed"]
	max_speed = params["max_speed"]
	renting_rate = params["renting_rate"]
	n_items = params["number_of_items"]

if __name__ == '__main__':

	parser = ArgumentParser(
		description='Evolutionary Computation solver for the KP Problem.'
		)

	parser.add_argument(
		'INPUT', type=str,
		help='ttp file to be read.')

	parser.add_argument(
		'-c', '--config', type=open,
		help='Configurations file. If not provided defaults will be used!')

	args = parser.parse_args()

	# Load configuration file
	configs = config.read_config(args.config)

	# The following calls to get_config will search the provided config file for each variable value
	# if no value is found or the config file is not specified each default value is assumed for each variable
	# "locals()[]"" will get the function by reflection using the function name as key
	generations = config.get_config(configs, ['number_generations'], 100)
	population_size = config.get_config(configs, ['size_population'], 20)
	prob_muta = config.get_config(configs, ['mutation', 'probability'], 0.25)
	prob_cross = config.get_config(configs, ['crossover', 'probability'], 0.75)
	tour_size = config.get_config(configs, ['tournament_size'], 5)
	elite_size = config.get_config(configs, ['elite_percentage'], 0.1)
	runs = config.get_config(configs, ['runs'], 5)

	development = config.get_config(configs, ['development'], False)
	plot_generations = config.get_config(configs, ['plot_generations'], True)
	
	# Read the file
	print("===================Instance==============")
	print(args.INPUT)
	distmat, items, params = readFile(args.INPUT)


	# Define EA parameters
	size_cromo = distmat.shape[0]-1 # as the starting and ending point is fixed
	my_fitness = fitness(items, params)
	sea = sea_bin_2016_visual.sea
	sea_for_plot = sea_bin_2016_visual.sea_for_plot
	run = sea_bin_2016_visual.run
	crossover = sea_bin_2016_visual.uniform_cross
	mutation = sea_bin_2016_visual.muta_bin
	tour_selection = sea_bin_2016_visual.tour_sel(tour_size)
	sel_survivors = sea_bin_2016_visual.sel_survivors_elite(elite_size)
	gen_population = sea_bin_2016_visual.gera_pop

	args = [generations, population_size, size_cromo, prob_muta, prob_cross, tour_selection, crossover, mutation, sel_survivors, my_fitness, gen_population]

	if(development):
		if(plot_generations):
			best, population, stat, stat_average = sea_for_plot(*args)
			
			display_stat_1(stat,stat_average)
		else:
			best, population = sea(
								generations,
								population_size, 
								size_cromo, 
								prob_muta,
								prob_cross,
								tour_selection,
								crossover,
								mutation,
								sel_survivors, 
								my_fitness,
								gen_population)

		print(best)
		print(calc_weight(phenotype(best[0]), items))


	else:
		best, best_average, tours = run(
										runs, 
										generations,
										population_size, 
										size_cromo, 
										prob_muta,
										prob_cross,
										tour_selection,
										crossover,
										mutation,
										sel_survivors, 
										my_fitness,
										gen_population)

		if(plot_generations):
			display_stat_n(best,best_average)

