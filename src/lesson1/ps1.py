colors = [['red', 'green', 'green',   'red', 'red'],
          ['red',   'red', 'green',   'red', 'red'],
          ['red',   'red', 'green', 'green', 'red'],
          ['red',   'red',   'red',   'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']

p = [[1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20]]

motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#Do not delete this comment!
#Do not use any import statements.
#Adding or changing any code above may
#cause the assignment to be graded incorrectly.

#Enter your code here:
alpha = 1.0 - sensor_right
p_stay = 1.0 - p_move

def sense(p, colors, measurement):
    a = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    s=0.0
        
    for i in range(len(p)):
        for j in range(len(p[i])):
            hit = (measurement == colors[i][j])
            a[i][j] = p[i][j] * (hit * sensor_right + (1 - hit) * alpha)
            s += a[i][j]
            
    for i in range(len(a)):
        for j in range(len(p[i])):
            a[i][j] /= s
            
    return a

def move(p, motion):   
    a = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    
    for i in range(len(p)):
        for j in range(len(p[i])):
            a[i][j] = (p_move * p[(i - motion[0]) % len(p)][(j - motion[1]) % len(p[i])]) + (p_stay * p[i][j])
    return a
   
            
if len(measurements) != len(motions):
    raise ValueError, "Measurements and Motions must have same length."

p_init = 1.0 / float(len(colors)) / float(len(colors))
p = [[p_init for row in range(len(colors[0]))] for col in range(len(colors))]

for k in range(len(measurements)):
    p = move(p, motions[k])
    p = sense(p, colors, measurements[k])


#Your probability array must be printed 
#with the following code.

show(p)