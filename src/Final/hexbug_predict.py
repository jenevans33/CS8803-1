from hexbug import *
from hexbug_utility import *
from hexbug_visualization import *

##########CONFIGURABLE##########
input_file = 'training_video1-centroid_data'

##########END CONFIGURABLE######

#Get the input array
hu = hexbug_utility()
input_array = hu.get_input(input_file)

#Process input array to get map and boundaries of box
hb = hexbug()
map, minX, maxX, minY, maxY = hb.process(input_array)
print "Min X:  ", minX
print "Max X:  ", maxX
print "Min Y:  ", minY
print "Max Y:  ", maxY
print "Map Length:  ", len(map)

boundaryDictionary = {'top':maxY, 'bottom':minY, 'left':minX, 'right':maxX}  
print "BD:  ", boundaryDictionary 

db_mean = hb.get_distance_mean(map)
print "Distance Between Mean: ", db_mean  

last5_db_mean = hb.get_distance_mean(map[-5:])
print "Last 5 DB Mean:  ", last5_db_mean

#####TESTING AREA#####
#predict_map = hb.test_prediction(map, db_mean, len(map) - 2, None)
#hu.write_map_to_file(map)

#hv = hexbug_visualization()
#hv.scatter_plot_it(map[100:250])

#####REAL DATA RUN AREA####
predict_map = hb.predict_next(map, last5_db_mean, 150, boundaryDictionary)
print predict_map

