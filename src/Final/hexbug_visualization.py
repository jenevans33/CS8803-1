import matplotlib.pyplot as plt
import turtle
import re

class hexbug_visualization:

    def __init__(self, debug=False):
        self.debug = debug
        
    def scatter_plot_it(self, map):
        #This produces a very simple scatter plot of the coordinate data passed in.  You should only pass in a slice
        #of the total data (100 - 200 points max) or else the points get so tightly bundled you can't really make much 
        #out of it.  This is purely for testing and analysis purposes.
        
        x_data = []
        y_data = []
        for i in range(len(map)):
            if map[i]["cur_point"] != [-1, -1]:
                x_data.append(map[i]["cur_point"][0]) 
                y_data.append(map[i]["cur_point"][1])
                
        # Create a Figure object.
        fig = plt.figure(figsize=(10, 8))
        # Create an Axes object.
        ax = fig.add_subplot(1,1,1) # one row, one column, first plot
        # Plot the data.
        ax.scatter(x_data, y_data, color="blue", marker="o")
        # Add a title.
        ax.set_title("Hexbug Scatter Plot")
        # Add some axis labels.
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # Produce an image.
        plt.show()
        
    def plot_old_new(self, oldmap, newmap):
        #This produces a very simple scatter plot of the coordinate data passed in.  You should only pass in a slice
        #of the total data (100 - 200 points max) or else the points get so tightly bundled you can't really make much 
        #out of it.  This is purely for testing and analysis purposes.
        
        oldx_data = []
        oldy_data = []
        for i in range(len(oldmap)):
            if oldmap[i]["cur_point"] != [-1, -1]:
                oldx_data.append(oldmap[i]["cur_point"][0]) 
                oldy_data.append(oldmap[i]["cur_point"][1])
        
        newx_data = []
        newy_data = []
        for j in range(len(newmap)):
            newx_data.append(newmap[j]["coord"][0])
            newy_data.append(newmap[j]["coord"][1])
                
        # Create a Figure object.
        fig = plt.figure(figsize=(10, 8))
        # Create an Axes object.
        ax = fig.add_subplot(1,1,1) # one row, one column, first plot
        # Plot the data.
        ax.scatter(oldx_data, oldy_data, color="blue", marker="o")
        ax.scatter(newx_data, newy_data, color="red", marker="^")
        # Add a title.
        ax.set_title("Hexbug Scatter Plot")
        # Add some axis labels.
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # Produce an image.
        plt.show()        
    
    def visualize_target(self, target_map, shift_factor, boundary_pts):
        #This function produces a visual of the targets movement in the box. Passed in are the target positions  
        #array (target_xy), factor to shift x,y by a certain amount (shift_factor), and boundary points 
        #array in the form [min_x, min_y, max_x, max_y]
        
        #Define the boundary points: [min_x, min_y, max_x, max_y]
        temp=[boundary_pts[0], boundary_pts[1], boundary_pts[2], boundary_pts[3]]
        #Shift boundary points to fit in the popup window
        boundary_points=[i-shift_factor for i in temp]  
        
        target_xy = []
        #Shift target positions to fit in the popup window
        for j in range(len(target_map)):
            value0=target_map[j]["cur_point"][0]-shift_factor
            value1=target_map[j]["cur_point"][1]-shift_factor
            value = [value0, value1]
            target_xy.append( value )
        
        #Set window properties
        window = turtle.Screen()
        window.bgcolor("white")

        #Set target properties
        target=turtle.Turtle()
        target.color("blue")
        target.shape("blank")
        target.pendown()
        target.pensize(1)   

        #Set boundary properties
        boundary=turtle.Turtle()
        boundary.color("black")
        boundary.shape("blank")
        boundary.pensize(1)
        boundary.penup()
        boundary.setposition(boundary_points[0],boundary_points[1])
        boundary.pendown()
        boundary.setposition(boundary_points[2],boundary_points[1])
        boundary.setposition(boundary_points[2],boundary_points[3])
        boundary.setposition(boundary_points[0],boundary_points[3])
        boundary.setposition(boundary_points[0],boundary_points[1])

        #Draw target path
        for i in range(len(target_xy)):
            target.goto(target_xy[i])

        window.exitonclick()        # wait for a user click on the canvas
        
        
