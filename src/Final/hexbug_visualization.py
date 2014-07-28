import matplotlib.pyplot as plt

class hexbug_visualization:

    def __init__(self, x_data=[], y_data=[]):
        self.x_data = x_data
        self.y_data = y_data
        
    def scatter_plot_it(self, map):
        #This produces a very simple scatter plot of the coordinate data passed in.  You should only pass in a slice
        #of the total data (100 - 200 points max) or else the points get so tightly bundled you can't really make much 
        #out of it.  This is purely for testing and analysis purposes.

        for i in range(len(map)):
            if map[i]["cur_point"] != [-1, -1]:
                self.x_data.append(map[i]["cur_point"][0]) 
                self.y_data.append(map[i]["cur_point"][1])
                
        # Create a Figure object.
        fig = plt.figure(figsize=(10, 8))
        # Create an Axes object.
        ax = fig.add_subplot(1,1,1) # one row, one column, first plot
        # Plot the data.
        ax.scatter(self.x_data, self.y_data, color="blue", marker="o")
        # Add a title.
        ax.set_title("Hexbug Scatter Plot")
        # Add some axis labels.
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # Produce an image.
        plt.show()
