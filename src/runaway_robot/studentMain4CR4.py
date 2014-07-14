# ----------
# Part Four
#
# Again, you'll track down and recover the runaway Traxbot. 
# But this time, your speed will be about the same as the runaway bot. 
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3. Again, try to catch the target in as few steps as possible.


from robot import *
from math import *
from numpy import *
from scipy import optimize
import random


def filter(x, P, measurements):      
    for n in range(len(measurements)):        
        # prediction
        x = (F * x) + u
        P = F * P * F.transpose()
        
        # measurement update
        Z = matrix([measurements[n]])
        y = Z.transpose() - (H * x)
        S = H * P * H.transpose() + R
        K = P * H.transpose() * linalg.inv(S)
        x = x + (K * y)
        P = (I - (K * H)) * P
    
    return x, P

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 
    
    def calc_R(xc, yc):
        """ calculate the distance of each 2D points from the center (xc, yc) """
        return sqrt((x_na-xc)**2 + (y_na-yc)**2)
    
    def f_2(c):
        """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
        Ri = calc_R(*c)
        return Ri - Ri.mean()    

    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = []
        x_set = [0.0001]
        y_set = [0.0001]
        iter = 0
        dist = []
        ot = 0.0
        turn_angle = []
        P =  matrix([[1000.0, 0.0], [0.0, 1000.0]])
    else: # not the first time, update my history
        measurements = OTHER[0]
        x_set = OTHER[1]
        y_set = OTHER[2]
        iter = OTHER[3]
        dist = OTHER[4]
        ot = OTHER[5]
        turn_angle = OTHER[6]
        P = OTHER[7]
 
    iter = iter + 1
    print "*****ITERATION:  ", iter
    print "NOISY TARGET:  ", target_measurement
    turning = 0.0
    distance = 0.0
    #####  BUILDING THE CIRCLE AND TAKING RADIUS #####
    x_set.append(target_measurement[0])
    y_set.append(target_measurement[1])
    x_na = r_[x_set[-50:]]
    y_na = r_[y_set[-50:]]    
    x_m = mean(x_na)
    y_m = mean(y_na)   
    
        #####  FILTER OUT THE NOISE  #####
    x = matrix([[target_measurement[0]], [target_measurement[1]]])   
    new_x, P = filter(x, P, measurements[-20:])
    xprime = new_x.item(0)
    yprime = new_x.item(1)
    fixed_target = (xprime, yprime)
    print "FIXED TARGET:  ", fixed_target  
    
    center_estimate = x_m, y_m
    print "Center Estimate:  ", center_estimate
    center, ier = optimize.leastsq(f_2, center_estimate)    
    xc, yc = center
    Ri       = calc_R(*center)
    R        = Ri.mean()    
    print "Center:  ", center
    print "Radius:  ", R
    
    #Find turning angle
    theta = atan2((target_measurement[1] - yc),(target_measurement[0] - xc))
    print "THETA:  ", theta    
    ta = abs(theta) - abs(ot)
    turn_angle.append(abs(ta))
    tan = r_[turn_angle]    
    print "TURN Angle:  ", mean(tan)
    
    #Find distance traveled
    if len(measurements) > 1:
        d = distance_between(target_measurement, measurements[len(measurements) - 1])
        dist.append(d)
        d_na = r_[dist]
        dist_mean = mean(d_na)
        print "DIST MEAN:  ", dist_mean
    else:
        dist_mean = None
        
    if dist_mean:
        heading = get_heading(measurements[len(measurements) - 1], fixed_target)
        test_robot = robot(target_measurement[0], target_measurement[1], heading, mean(tan), dist_mean)
        test_robot.move_in_circle()
        next_spot = test_robot.sense()
        print "DISTANCE TO CENTER (1):  ", distance_between(next_spot, center)
        if distance_between(hunter_position, next_spot) >= max_distance:
            #can't make it in 1.....Go 2 places ahead
            print "Can't reach the next spot...going 2"
            test_robot.move_in_circle()
            next_spot = test_robot.sense()  
            print "DISTANCE TO CENTER (2):  ", distance_between(next_spot, center)                             
    else:
        next_spot = (0.0, 0.0)

    if dist_mean:
        heading = get_heading(measurements[len(measurements) - 1], fixed_target)
        future_x = target_measurement[0] + dist_mean * cos(heading)
        future_y = target_measurement[1] + dist_mean * sin(heading) 
        test_spot = (future_x, future_y)  
    else:
        test_spot = (0.0, 0.0)
    
    print "NEXT SPOT:  ", next_spot  
    print "TEST SPOT:  ", test_spot      

    measurements.append(target_measurement)    
    OTHER = [measurements, x_set, y_set, iter, dist, theta, turn_angle, P]
    heading_to_target = get_heading(hunter_position, next_spot)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = distance_between(hunter_position, next_spot)
    print "DISTANCE  ", distance

    return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0
    #For Visualization
    import turtle
    window = turtle.Screen()
    window.bgcolor('white')
    chaser_robot = turtle.Turtle()
    chaser_robot.shape('arrow')
    chaser_robot.color('blue')
    chaser_robot.resizemode('user')
    chaser_robot.shapesize(0.3, 0.3, 0.3)
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.3, 0.3, 0.3)
    size_multiplier = 15.0 #change size of animation
    chaser_robot.hideturtle()
    chaser_robot.penup()
    chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
    chaser_robot.showturtle()
    broken_robot.hideturtle()
    broken_robot.penup()
    broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
    broken_robot.showturtle()
    measuredbroken_robot = turtle.Turtle()
    measuredbroken_robot.shape('circle')
    measuredbroken_robot.color('red')
    measuredbroken_robot.penup()
    measuredbroken_robot.resizemode('user')
    measuredbroken_robot.shapesize(0.1, 0.1, 0.1)
    broken_robot.pendown()
    chaser_robot.pendown()
    #End of Visualization
    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:
        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        print "HUNTER:  ", hunter_position
        print "TARGET:  ", target_position
        separation = distance_between(hunter_position, target_position)
        print "SEPARATION:  ", separation
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)

        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()
        #Visualize it
        measuredbroken_robot.setheading(target_bot.heading*180/pi)
        measuredbroken_robot.goto(target_measurement[0]*size_multiplier, target_measurement[1]*size_multiplier-100)
        measuredbroken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
        chaser_robot.setheading(hunter_bot.heading*180/pi)
        chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
        #End of visualization
        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught

def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER


target = robot(0.0, 10.0, 0.0, 2*pi / 30, 2.0)
measurement_noise = .05*target.distance
#measurement_noise = 0.0
target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)
#KF Setup

x = matrix([[0.], [0.]]) # initial state (location and velocity)
u = matrix([[0.], [0.]]) # external motion

F =  matrix([[1.0, 0.0], [0.0, 1.0]])
H =  matrix([[1.0, 0.0], [0.0, 1.0]])
R =  matrix([[0.1, 0.0], [0.0, 0.1]])
I =  matrix([[1.0, 0.0], [0.0, 1.0]])

print demo_grading(hunter, target, next_move)