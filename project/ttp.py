"""
ttp_2017.py
Sebastian Rehfeldt, April 2017
"""
import os
from read_ttp_file import readFile
from argparse import ArgumentParser
import math
import tsp
import kp
import config


def readTour(file):
    tour = []
    length = 0
    with  open(file) as file_in:
        amounts = file_in.readline()
        firstLine = file_in.readline() #contains tour part which is not needed

        lines = file_in.readlines()
        for line in lines:
            start, end, dist = line.split()
            tour.append(int(start))
            length += int(dist)

    return tour, length


def calculateObjectiveValue(tour,plan,distmat,params):

    renting_rate = params["renting_rate"]
    capacity = params["kp_capacity"]
    min_speed = params["min_speed"]
    max_speed = params["max_speed"]
    v = (max_speed-min_speed)/capacity

    profit = 0
    cur_weight = 0
    time = 0

    keys = list(plan.keys())

    former_city = 0
    for i in range(len(tour)):
        #travel to city tour[i]
        city = tour[i]
        dist = distmat[former_city,city]
        speed = max_speed - v*cur_weight
        travelTime = dist/speed

        #load item
        if str(city) in keys:
            items = plan[str(city)]
            for item in items:
                profit += item[0]
                cur_weight += item[1]

        time += travelTime
        former_city = city

    #travel back to first city which has index 0      
    city = 0
    dist = distmat[former_city,city]
    speed = max_speed - v*cur_weight
    travelTime = dist/speed
    time += travelTime

    objective = profit - renting_rate*time

    return profit, time, objective

if __name__ == '__main__':

    parser = ArgumentParser(
        description='Evolutionary Computation solver for the TTP Problem.'
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

    #TODO verify the solution on toy example from paper "The travelling thief problem: the first ..."

    folder = os.path.dirname(os.path.realpath(__file__))
    tourpath = folder + "/instances/" + config.file["tour"]
    
    # Read the file
    print("===================Instance==============")
    print(args.INPUT)
    distmat, items, params = readFile(args.INPUT)

    if(config.use_linkern):
        tour, length = readTour(tourpath)
        plan = kp.getPackingPlan(items, tour, distmat, params)
        profit, time, objective = calculateObjectiveValue(tour,plan,distmat,params)
    else:
        #TODO think about a way to combine both approaches instead of solving in sequential order (real future work)
        #maybe: after running kp - start over with tsp and find a good tour for that packing plan and continue with KP then and start to loop (not a super smart idea and super slow, but I didnt find a good solution yet)

        #return top k distinct tours as longer tours could be better for the whole problem (k in config)
        tours = tsp.getTours(distmat) #tour does not include starting and ending cities with index 0
        #set shortest tour as initial tour
        tour = tours[0][0]
        length = tours[0][1]

        #create plans for each tour
        #plan is a dict where the key is the city id and the value an array of tuples (profit,weight)
        plan = {}
        profit = 0
        time = 0
        objective = - math.inf

        for i in range(len(tours)):
            cur_tour = tours[i][0]
            cur_length = tours[i][1]
            cur_plan = kp.getPackingPlan(items, cur_tour, distmat, params)
            p, t, o = calculateObjectiveValue(cur_tour,cur_plan,distmat,params)
            #print("========")
            #print(cur_length)
            #print(o)

            #update everything if new tour with plan is better
            if o>objective:
                if(objective > - math.inf):
                    print("A longer tour was better")
                tour = cur_tour
                length = cur_length
                plan = cur_plan
                profit = p
                time = t
                objective = o

    """             OUTPUT             """
    print("\n\n===================TOUR==============")
    print(tour)

    if(config.tsp_fitness == "simple"):
        print("\n\n===================LENGTH==============")
        print(length) #linkern length is around 2613 (using MATLAB code for a280)

    print("\n\n===================Plan==============")
    print(plan)

    print("\n\n===================Objective==============")
    print("Profit   : "+str(profit))
    print("Time     : "+str(time))
    print("Rent     : "+str(params["renting_rate"]))
    print("Objective: "+str(objective))
