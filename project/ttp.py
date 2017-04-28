"""
ttp_2017.py
Sebastian Rehfeldt, April 2017
"""
import os
import numpy

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
        line = file_in.readline()
        #each city stores tuples of items having a profit and weight
        items = {}

        lines = file_in.readlines()
        for line in lines:
            n,p,w,node = line.split()
            if hasattr(items, node):
                items[node].append((float(p),float(w)))
            else:
                items[node] = [(float(p),float(w))]

    return coordinates, distmat, items



if __name__ == '__main__':

    folder = os.path.dirname(os.path.realpath(__file__))
    filename = "a280_n279_bounded-strongly-corr_01.ttp"
    filepath = folder + "/instances/" + filename

    coordinates, distmat, items = readFile(filepath)

  