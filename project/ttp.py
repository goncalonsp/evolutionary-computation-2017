"""
ttp_2017.py
Sebastian Rehfeldt, April 2017
"""
import os
import numpy
import tsp
import kp

def createDistMat(coordinates):
    distmat = numpy.zeros(shape=(len(coordinates),len(coordinates)))

    #run until second last element
    for i in range(0,len(coordinates)-1):
        #start at next element and run until last
        for j in range(i+1,len(coordinates)):
            dist = numpy.sqrt(numpy.square(coordinates[i][0]-coordinates[j][0])+numpy.square(coordinates[i][1]-coordinates[j][1]))
            distmat[i,j]= dist
            distmat[j,i]= dist     
    return distmat
    



def readFile(file):
    with  open(file) as file_in:
        # read header
        problem_name = file_in.readline()
        kp_data_type = file_in.readline()
        dimension = file_in.readline()
        number_of_items = file_in.readline()
        kp_capacity = file_in.readline()
        min_speed = file_in.readline()
        max_speed = file_in.readline()
        renting_rate = file_in.readline()
        edge_weight_type = file_in.readline()

        problem_parameters = {
            "problem_name": problem_name.split()[2],
            "kp_data_type": kp_data_type.split()[3:],
            "dimension": int(dimension.split()[1]),
            "number_of_items": int(number_of_items.split()[3]),
            "kp_capacity": float(kp_capacity.split()[3]),
            "min_speed": float(min_speed.split()[2]),
            "max_speed": float(max_speed.split()[2]),
            "renting_rate": float(renting_rate.split()[2]),
            "edge_weight_type": edge_weight_type.split()[1]
        }

        separator = file_in.readline()
        
        #read coordinates (index, x, y)
        line = file_in.readline()
        coordinates = []
        while line.split()[0].isdigit():
            n,x,y = line.split()
            coordinates.append((float(x),float(y)))

            line = file_in.readline()

        #calculate distant matrix
        distmat = createDistMat(coordinates)

        #read items (index, profit, weight, assigned node number)
        #each city stores tuples of items having a profit and weight
        items = {}

        lines = file_in.readlines()
        for line in lines:
            n,p,w,node = line.split()
            #coordinates cities and distmat start to count at 0
            #datafile starts to count at 1
            #subtract 1 to match cities in items and coordinates
            node = str(int(node)-1)
            keys = list(items.keys())
            if node in keys:
                items[node].append((float(p),float(w)))
            else:
                items[node] = [(float(p),float(w))]

    return coordinates, distmat, items, problem_parameters

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
    #TODO verify the solution on toy example from paper "The travelling thief problem: the first ..."

    filename = "a280_n279_bounded-strongly-corr_01.ttp"
    #filename = "a280_n1395_uncorr-similar-weights_05.ttp"
    #filename = "a280_n2790_uncorr_10.ttp"
    #filename = "fnl4461_n4460_bounded-strongly-corr_01.ttp"
    #filename = "fnl4461_n22300_uncorr-similar-weights_05.ttp"
    #filename = "fnl4461_n44600_uncorr_10.ttp"

    #these files cant be used because the numpy array would be too big :-D
    #filename = "pla33810_n33809_bounded-strongly-corr_01.ttp"
    #filename = "pla33810_n169045_uncorr-similar-weights_05.ttp"
    #filename = "pla33810_n338090_uncorr_10.ttp"




    folder = os.path.dirname(os.path.realpath(__file__))    
    filepath = folder + "/instances/" + filename

    coordinates, distmat, items, params = readFile(filepath)
    #TODO: multiple runs of the algorithm for allowing a statistical analysis

    #TODO think about a way to combine both approaches instead of solving in sequential order
    #maybe: after running kp - start over with tsp and find a good tour for that packing plan and continue with KP then and start to loop (not a super smart idea and super slow, but I didnt find a good solution yet)

    #TODO try to use linkern.tour instead
    tour, length = tsp.getTour(coordinates,distmat) #tour does not include starting and ending cities with index 0
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