import numpy as np
import matplotlib.pyplot as plt
import re
from math import *


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_input(filename):
    #Read in the input file and create array of the data points.
    p = re.compile('[-0-9]+')  #this should find the points on each line of the input (numeric + or -).  All integers.
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
    return m, min(allX), max(allX), min(allY), max(allY)

def simple_next_move(current, distance, heading):
    #Simple next move.  Take current move, avg distance, and heading to predict next spot.
    x = current[0] + distance * cos(heading)
    y = current[1] + distance * sin(heading)     
    return (int(x), int(y))
    
def get_distance_mean(map):
    #returns the mean distance based on the input map.
    dblist = []
    for i in range(len(map)):
        if map[i]["db"] != None:
            dblist.append(map[i]["db"])   
    return np.mean(dblist) 

def test_prediction(mapfile, d, start=None, stop=None):
    #test predict next steps.  This is just for testing out the code.  The real predict next
    #function to use for getting the frames to turn in will be predict_next()
    if start and not stop:
        ta = [mapfile[start]]
    elif start and stop:
        ta = mapfile[start:stop]
    elif stop and not start:
        #throw error
        raise Exception('Having a stop with no start makes no sense')
    else:
        #no start and no stop...do whole map
        #Need to really work on this because a bad point will blow this whole thing up.
        ta = mapfile
       
    pm = []
    for i in range(len(ta)):
        cur_point = ta[i]
        x,y = simple_next_move(cur_point["cur_point"], d, cur_point["angle"])
        hm = {"coord" : [x,y]}
        pm.append(hm)
        
    return pm

def predict_next(mapfile, d, frames):
    #predict the next n number of frames
    
    #TODO:  instead of just arbitrarily using the current angle I think we should analyze the last say 5 points and
    #       angles to make sure the last one is not an anomaly.  If it is use the mean of the correct ones.
    
    #TODO:  when we get the point back from next_move need to make sure it wouldn't have hit a wall and bounced.  
    #       if it would then call the bounce function and replace the coordinates and angle with that.
    
    curpoint = mapfile[len(mapfile) - 2]
    pm = []
    for i in range(frames):
        x,y = simple_next_move(curpoint["cur_point"], d, curpoint["angle"])
        hm = {"coord" : [x,y]}
        pm.append(hm)
        curpoint = {"cur_point" : [x,y], "angle" : curpoint["angle"]}
    return pm

def scatter_plot_it(map):
    #This produces a very simple scatter plot of the coordinate data passed in.  You should only pass in a slice
    #of the total data (100 - 200 points max) or else the points get so tightly bundled you can't really make much 
    #out of it.  This is purely for testing and analysis purposes.
    x_data = []
    y_data = []
    for i in range(len(map)):
        if map[i]["cur_point"] != [-1, -1]:
            x_data.append(map[i]["cur_point"][0]) 
            y_data.append(map[i]["cur_point"][1])
            
    print "XDATA: ", len(x_data)
    print "YDATA: ", len(y_data)
    
    # Create a Figure object.
    fig = plt.figure(figsize=(10, 8))
    # Create an Axes object.
    ax = fig.add_subplot(1,1,1) # one row, one column, first plot
    # Plot the data.
    ax.scatter(x_data, y_data, color="blue", marker="o")
    # Add a title.
    ax.set_title("Data Scatter Plot")
    # Add some axis labels.
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    # Produce an image.
    plt.show()

##########CONFIGURABLE##########
input_file = 'training_video1-centroid_data'

##########END CONFIGURABLE######

#Get the input array
input_array = get_input(input_file)

#Process input array to get map and boundaries of box
map, minX, maxX, minY, maxY = process(input_array)
print "Min X:  ", minX
print "Max X:  ", maxX
print "Min Y:  ", minY
print "Max Y:  ", maxY
print "Map Length:  ", len(map)
  
db_mean = get_distance_mean(map)
print "Distance Between Mean: ", db_mean  

#####TESTING AREA#####
#predict_map = test_prediction(map, db_mean, len(map) - 2, None)
write_map_to_file(map)
#scatter_plot_it(map)

#####REAL DATA RUN AREA####
#predict_map = predict_next(map, db_mean, 10)
#print predict_map

