import numpy as np
from math import *

class hexbug:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def distance_between(self, point1, point2):
        """Computes distance between point1 and point2. Points are (x, y) pairs."""
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def process(self, in_a):
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
                    db = self.distance_between(previous_point, in_a[i])
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
            
        #There are some points that are way off from the rest and are anomalies that should not be used
        #for min and max determination.  If the point is within 10 of the next point then it should be ok.    
        sorted_maxX = sorted(allX, reverse=True)
        sorted_maxY = sorted(allY, reverse=True)
        sorted_minX = sorted(allX)
        sorted_minY = sorted(allY)
        for i in range(len(sorted_maxX)):
            if sorted_maxX[i] - sorted_maxX[i + 1] <= 10:
                maxX = sorted_maxX[i]
                break
        for i in range(len(sorted_maxY)):
            if sorted_maxY[i] - sorted_maxY[i + 1] <= 10:
                maxY = sorted_maxY[i]
                break        
        for i in range(len(sorted_minX)):
            if sorted_minX[i + 1] - sorted_minX[i] <= 10:
                minX = sorted_minX[i]
                break
        for i in range(len(sorted_minY)):
            if sorted_minY[i + 1] - sorted_minY[i] <= 10:
                minY = sorted_minY[i]
                break        
        return m, minX, maxX, minY, maxY
    
    def simple_next_move(self, current, distance, heading):
        #Simple next move.  Take current move, avg distance, and heading to predict next spot.
        print "SNM-CURRENT POS:  ", current
        print "SNM-DISTANCE:  ", distance
        print "SNM-HEADING:  ", heading
        x = current[0] + distance * cos(heading)
        y = current[1] + distance * sin(heading)   
        print "SNM-NEXT POS:  ", (x,y)  
        return (int(x), int(y))
        
    def get_distance_mean(self, map):
        #returns the mean distance based on the input map.
        dblist = []
        for i in range(len(map)):
            if map[i]["db"] != None and map[i]["db"] != 0.0:
                dblist.append(map[i]["db"])   
        return np.mean(dblist) 
    
    def test_prediction(self, mapfile, d, boundaryDictionary, start=None, stop=None):
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
            x,y = self.simple_next_move(cur_point["cur_point"], d, cur_point["angle"])
            hm = {"coord" : [x,y]}
            pm.append(hm)
            
        return pm
    
    def predict_next(self, mapfile, dist, frames, boundaryDictionary):
        #predict the next n number of frames
        
        #TODO:  instead of just arbitrarily using the current angle I think we should analyze the last say 5 points and
        #       angles to make sure the last one is not an anomaly.  If it is use the mean of the correct ones.
        
        #TODO:  when we get the point back from next_move need to make sure it wouldn't have hit a wall and bounced.  
        #       if it would then call the bounce function and replace the coordinates and angle with that.
        
        curpoint = mapfile[len(mapfile) - 2]
        pm = []
        hitWall = False
        for i in range(frames):
            x,y = self.simple_next_move(curpoint["cur_point"], dist, curpoint["angle"])
            print "PN-CURPOINT:  ", curpoint
            #does x or y hit a boundary
            if (x <= boundaryDictionary["left"] or x >= boundaryDictionary["right"]) and not hitWall:
                #hit x boundary
                print "HIT X BOUNDARY WITH PREDICTED POINT:  ", (x,y)
                curX, curY = curpoint["cur_point"]
                diffX = abs(x - curX)
                diffY = abs(y - curY)
                (x,y), angle = self.bounce(curpoint["cur_point"], (diffX,diffY), curpoint["angle"], boundaryDictionary)
                hm = {"coord" : [x,y]}
                curpoint = {"cur_point" : [x,y], "angle" : angle}
                hitWall = True
            elif (y <= boundaryDictionary["bottom"] or y >= boundaryDictionary["top"]) and not hitWall:
                #hit y boundary
                print "HIT Y BOUNDARY WITH PREDICTED POINT:  ", (x,y)
                curX, curY = curpoint["cur_point"]
                diffX = abs(x - curX)
                diffY = abs(y - curY)            
                (x,y), angle = self.bounce(curpoint["cur_point"], (diffX,diffY), curpoint["angle"], boundaryDictionary)
                hm = {"coord" : [x,y]}
                curpoint = {"cur_point" : [x,y], "angle" : angle} 
                hitWall = True           
            else:
                #didn't hit a boundary
                print "NO BOUNDARY HIT"
                hm = {"coord" : [x,y]}
                curpoint = {"cur_point" : [x,y], "angle" : curpoint["angle"]}
                hitWall = False
            pm.append(hm)
        return pm        
    
    def getHeading(self, angle):
        #which direction are we heading?
        if angle > pi: #heading down
            if angle > 3.0*pi/2.0: #heading right
                heading = {"vertical" : "down", "horizontal" : "right"}
            else: #heading left
                heading = {"vertical" : "down", "horizontal" : "left"}
        else: #heading up
            if angle > pi/2.0: #heading left
                heading = {"vertical" : "up", "horizontal" : "left"}
            else: #heading right
                heading = {"vertical" : "up", "horizontal" : "right"}
        return heading
    
    def whichWallHit(self, heading, velocityX, velocityY, boundaryDictionary, position):
        #which wall are we hitting?
        print "VelocityX:  ", velocityX
        print "VelocityY:  ", velocityY
        print "Heading:  ", heading
        print "Position:  ", position
        wallHit = []
        if heading["vertical"] == "up": #check distance from top
            print "GOING UP"
            distance = abs(position[1] - boundaryDictionary["top"])
            if distance <= velocityY:
                wallHit.append(["top", distance])
        else: #heading["vertical"] == "down" so check distance from bottom
            print "GOING DOWN"
            distance = abs(position[1] - boundaryDictionary["bottom"])
            if distance <= velocityY:
                wallHit.append(["bottom", distance])
        
        if heading["horizontal"] == "right": #check distance from right
            print "GOING RIGHT"
            distance = abs(position[0] - boundaryDictionary["right"])
            if distance <= velocityX:
                wallHit.append(["right", distance])
        else: # heading["horizontal"] == "left": #check distance from left
            print "GOING LEFT"
            distance = abs(position[0] - boundaryDictionary["left"])
            if distance <= velocityX:
                wallHit.append(["left", distance])
                
        if len(wallHit) > 1: #need to sort in order of wall hit first
            wallHit.sort()
        print "Wallhit", wallHit ##CODE TESTING
        return wallHit
    
    
    def oneBounce(self, wallHit, position, velocityX, velocityY, angle, boundaryDictionary):
        dist2wall = wallHit[0][1]
        if (wallHit[0][0] == "top") or (wallHit[0][0] == "bottom"):
            newX = (position[0] + velocityX) #X just keeps moving same direction
            newAngle = 2.0*pi - angle
            if (wallHit[0][0] == "bottom"):
                newY = boundaryDictionary[wallHit[0][0]] - (velocityY - dist2wall) #max Y value minues leftover velocity
            else: #top
                newY = boundaryDictionary[wallHit[0][0]] + (velocityY - dist2wall) #min Y value plus leftover velocity           
            
        elif (wallHit[0][0] == "left") or (wallHit[0][0] == "right"):
            newY = (position[1] + velocityY)  #Y just keeps moving same direction
            newAngle = pi/2.0 - angle
            if (wallHit[0][0] == "right"):
                newX = boundaryDictionary[wallHit[0][0]] - (velocityX - dist2wall) #max X value minus leftover velocity
            else: #left
                newX = boundaryDictionary[wallHit[0][0]] + (velocityX - dist2wall) #min X value plus leftover velocity        
        return newX, newY, newAngle
        
    def twoBounce(self, wallHit, position, velocityX, velocityY, angle, boundaryDictionary):
        for i in range(2):
            dist2wall = wallHit[i][1]
            if (wallHit[i][0] == "top") or (wallHit[i][0] == "bottom"):
                newAngle = 2.0*pi - angle
                if (wallHit[i][0] == "bottom"):
                    newY = boundaryDictionary[wallHit[i][0]] - (velocityY - dist2wall) #max Y value minues leftover velocity
                else: #top
                    newY = boundaryDictionary[wallHit[i][0]] + (velocityY - dist2wall) #min Y value plus leftover velocity           
            
            elif (wallHit[i][0] == "left") or (wallHit[i][0] == "right"):
                newAngle = pi/2.0 - angle
                if (wallHit[i][0] == "right"):
                    newX = boundaryDictionary[wallHit[i][0]] - (velocityX - dist2wall) #max X value minus leftover velocity
                else: #left
                    newX = boundaryDictionary[wallHit[i][0]] + (velocityX - dist2wall) #min X value plus leftover velocity       
        return newX, newY, newAngle
        
    def bounce(self, position, velocity, angle, boundaryDictionary):
        """Function receives a center of mass position, velocity and angle,
        along with a dictionary of the boundary positions top, bottom, left and right.
        It compares the current position, velocity and angle with the boundary 
        positions and determines where it will hit the wall and bounce. It returns a
        new postion and angle, one "move" later. It assumes the velocity is not
        impacted by the bounce.
        Function should be called after a check that we are within 1 move of a wall."""
        
        print "BOUNCE VELOCITY:  ", velocity    
        angle = angle%(2.0*pi) #ensure angle is % 2*pi
                  
        heading = self.getHeading(angle) #ensure angle is CCW direction (no negative angles)
                           
        velocityX, velocityY = velocity #get X and Y components of velocity vector
          
        wallHit = self.whichWallHit(heading, velocityX, velocityY, boundaryDictionary, position) #determine where we are hitting
    
        newX = -1
        newY = -1
        newAngle = 0    
        #reflect to new X and Y coords -- SIMPLE 1 Bounce
        if len(wallHit) == 1:
            newX, newY, newAngle = self.oneBounce(wallHit, position, velocityX, velocityY, angle, boundaryDictionary)
               
        #reflect to new X and Y coords: corner hit with first and then second bounces
        if len(wallHit) == 2:
            newX, newY, newAngle = self.twoBounce(wallHit, position, velocityX, velocityY, angle, boundaryDictionary)
            
        #quick error check
        if len(wallHit) > 2:
            print "oops, something went very wrong! too many hits"   
                
        return (newX,newY), newAngle    
            