import numpy as np
import re
from math import *


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_input(filename):
    #Read in the input file and create array of the data points.
    p = re.compile('[-0-9]+')
    ia = []
    f = open(filename, 'r')
    for line in f:
        x,y = p.findall(line)
        ia.append([int(x),int(y)])
    f.close()
    return ia

def write_map_to_file(m):
    #write the map to a file for analysis
    f = open('map_file.txt', 'w')
    for i in range(len(m)):
        f.write("%s:%s" % (m[i], '\n'))
    f.close()

def process(in_a):
    #Iterate through the array.  Check point against last point for distance and angle and build hashmap (or in python
    #an array of dicts).  All -1, -1 points are bad so make a note of it and don't use the distances or angles.  
    #Also build a set of complete X and Y measurements to get the MIN/MAX of X coords and Y coords....this should 
    #be around the boundaries of the box.
    allX = []
    allY = []
    m = []
    previous_point = None
    for i in range(len(in_a)):
        if in_a[i] != [-1, -1]:
            allX.append(in_a[i][0])
            allY.append(in_a[i][1])
            if previous_point:
                db = distance_between(previous_point, in_a[i])
                theta = atan2((in_a[i][1] - previous_point[1]),(in_a[i][0] - previous_point[0]))
                dict = {"id" : i, "db" : db, "angle" : theta, "pre_point" : previous_point, "cur_point" : in_a[i]}
                previous_point = in_a[i]
            else:
                dict = {"id" : i, "db" : None, "angle" : None, "pre_point" : previous_point, "cur_point" : in_a[i]}
                previous_point = in_a[i]
        else:
            previous_point = None
            dict = {"id" : i, "db" : None, "angle" : None, "pre_point" : previous_point, "cur_point" : in_a[i]}
        m.append(dict)
    return np.array(m), min(allX), max(allX), min(allY), max(allY)

#Get the input array
input_array = get_input('training_video1-centroid_data')

#Process input array to get map and boundaries of box
map, minX, maxX, minY, maxY = process(input_array)
print "Min X:  ", minX
print "Max X:  ", maxX
print "Min Y:  ", minY
print "Max Y:  ", maxY

print len(map)

write_map_to_file(map)