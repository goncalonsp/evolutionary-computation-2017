"""
ttp_2017.py
Sebastian Rehfeldt, April 2017
"""
import os
import tsp
import kp
from read_ttp_file import readFile
from argparse import ArgumentParser

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
    # use one of the following files:
    # "a280_n279_bounded-strongly-corr_01.ttp"
    # "a280_n1395_uncorr-similar-weights_05.ttp"
    # "a280_n2790_uncorr_10.ttp"
    #
    # each of these bellow will take 151.8 MB for the distmat array
    # "fnl4461_n4460_bounded-strongly-corr_01.ttp"
    # "fnl4461_n22300_uncorr-similar-weights_05.ttp"
    # "fnl4461_n44600_uncorr_10.ttp"

    # these files cant be used because the distmat array would be too big :-D, about 8.5 GB big
    # "pla33810_n33809_bounded-strongly-corr_01.ttp"
    # "pla33810_n169045_uncorr-similar-weights_05.ttp"
    # "pla33810_n338090_uncorr_10.ttp"

    args = parser.parse_args()

    #TODO verify the solution on toy example from paper "The travelling thief problem: the first ..."

    # Read the file
    distmat, items, params = readFile(args.INPUT)
    print("done reading")
    #TODO: multiple runs of the algorithm for allowing a statistical analysis

    #TODO think about a way to combine both approaches instead of solving in sequential order
    #maybe: after running kp - start over with tsp and find a good tour for that packing plan and continue with KP then and start to loop (not a super smart idea and super slow, but I didn't find a good solution yet)

    #TODO try to use linkern.tour instead
    tour, length = tsp.getTour(distmat) #tour does not include starting and ending cities with index 0
    print("===================TOUR==============")
    print(tour)
    print("\n\n===================LENGTH==============")
    print(length)

    #TODO run for top k distinct tours and select the best
    #plan is a dict where the key is the city id and the value an array of tuples (profit,weight)
    plan = kp.getPackingPlan(items, tour, distmat, params)
    print("\n\n===================Plan==============")
    print(plan)

    profit, time, objective = calculateObjectiveValue(tour,plan,distmat,params)

    print("\n\n===================Objective==============")
    print("Profit   : "+str(profit))
    print("Time     : "+str(time))
    print("Rent     : "+str(params["renting_rate"]))
    print("Objective: "+str(objective))