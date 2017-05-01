"""			General config 			"""
use_linkern = False
top_k = 1



"""			TSP config 			"""
tsp_development = True #will plot a curve over generations or run multiple times
tsp_fitness = "distance"
tsp_interpretation = "simple"
generations =	100 #10000
population =  	20 # 200
prob_muta = 	0.25
prob_cross = 	0.75
sigma = 		0.1
tour_size = 	5
elite_size = 	0.1



"""			File selection 			"""
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
files = [{
			"name": "a280_n279_bounded-strongly-corr_01.ttp",
			"tour": "a280.linkern.tour"
		}]
#"""		

