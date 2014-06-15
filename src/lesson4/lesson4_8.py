# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

#grid = [[0, 0, 1, 0, 0, 0],
#        [0, 0, 1, 0, 0, 0],
#        [0, 0, 0, 0, 1, 0],
#        [0, 0, 0, 0, 1, 0]]

grid = [ [ 0, 1, 0, 0, 0 ],
         [ 0, 0, 0, 1, 0 ] ]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.
print "Goal:  ", goal

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    # ----------------------------------------
    # insert code here and make sure it returns the appropriate result
    # ----------------------------------------
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1
    
    x = init[0]
    y = init[1]
    g = 0
    
    open_state = [[g, x, y]]
    
    found = False   #true when goal state reached
    giveup = False   #true when exhausted states and still no goal
    
    while found is False and giveup is False:
        #check to see if there are still open items
        if len(open_state) == 0:
            giveup = True
            path = "fail"
        else:
            open_state.sort()
            open_state.reverse()
            next_state = open_state.pop()
            x = next_state[1]
            y = next_state[2]
            g = next_state[0]
            
            #check for goal state
            if x == goal[0] and y == goal[1]:
                found = True
                path = next_state
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open_state.append([g2, x2, y2])
                            closed[x2][y2] = 1
                
    return path
    
ret = search()
print ret