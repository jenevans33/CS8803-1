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
hb = hexbug(debug=False)
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

last5_db_mean = hb.get_distance_mean(map[-7:])
print "Last 5 DB Mean:  ", last5_db_mean

#####TESTING AREA#####
error_rate, pm = hb.test_prediction(map, boundaryDictionary, 63, 1, 400)
print "FINAL ERROR:  ", error_rate
#hu.write_map_to_file(map)

hv = hexbug_visualization()
hv.plot_old_new(map[400:464], pm)
#hv.visualize_target(map[25801:25826], 375, [minX, minY, maxX, maxY])

#####REAL DATA RUN AREA####
#predict_map = hb.predict_next(map, last5_db_mean, 150, boundaryDictionary)
#print predict_map

