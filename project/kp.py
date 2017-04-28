"""
kp.py
Sebastian Rehfeldt, April 2017
"""
import numpy

def getPackingPlan(items, tour, distmat, params):
	#TODO implement EA algorithm later

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
	scoredItems = numpy.empty(n_items, dtype=object)
	i = 0
	for i in range(len(tour)):
		city = tour[i]
		dist = distanceToFinish[i]
		for item in items[str(tour[i])]:
			p = item[0]
			w = item[1]

			v = (max_speed-min_speed)/capacity
			speed = max_speed - v*w
			travelTime = dist/speed
			score = p - renting_rate*travelTime
			fitness = renting_rate*dist/max_speed + score

			scoredItems[i] = {
				"city_id": city,
				"profit" : p,
				"weight" : w,
				"score"  : score,
				"fitness": fitness
			}

			i+=1

	#sort items according to
	scoredItems = sorted(scoredItems, key=lambda a: a["score"],reverse=True)

	cur_capacity = 0
	packedItems = {}
	for item in scoredItems:
		city = str(item["city_id"])

		if (cur_capacity+item["weight"]<capacity) and (item["fitness"]>0):

			if hasattr(packedItems, city):
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