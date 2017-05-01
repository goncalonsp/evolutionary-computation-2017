"""
read_ttp_file.py
Sebastian Rehfeldt, April 2017

The ttp file extension will be expected to use the following pattern:

PROBLEM NAME:   a280-TTP
KNAPSACK DATA TYPE: bounded strongly corr
DIMENSION:  <number of places for the tsp problem>
NUMBER OF ITEMS:    <number of items for the tsp problem>
CAPACITY OF KNAPSACK:   <knapsack maximum capacity>
MIN SPEED:  0.1
MAX SPEED:  1
RENTING RATIO:  5.61
EDGE_WEIGHT_TYPE:   CEIL_2D
NODE_COORD_SECTION  (INDEX, X, Y):
1   288 149
2   288 129
3   270 133
4   256 141
5   256 157
6   246 157
7   236 169
8   228 169
ITEMS SECTION   (INDEX, PROFIT, WEIGHT, ASSIGNED NODE NUMBER): 
1   101 1   2
2   202 2   3
3   404 4   4
4   202 2   5
5   996 896 6
6   1992    1792    7
7   3984    3584    8
8   467 367 9
9   934 734 10


"""
import numpy
from argparse import ArgumentParser

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

    return distmat, items, problem_parameters

if __name__ == '__main__':
    """ Run me directly to see how the readFile function reads the ttp files """
    parser = ArgumentParser(
        description='Read a ttp file.'
        )
    parser.add_argument(
        'INPUT', type=str,
        help='ttp file to be read.')    
    args = parser.parse_args()

    distmat, items, params = readFile(args.INPUT);
    
    print("\ndistmat = {} length {}"
        .format(type(distmat),distmat.shape))
    print(distmat)
    
    print("\nitems = {} length {}"
        .format(type(items),len(items)))
    print(items)
    
    print("\nparams = ")
    print(params)
