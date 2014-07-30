import re

class hexbug_utility:

    def __init__(self, outfile='map_file.txt', debug=False):
        self.outfile = outfile
        self.debug = debug
        
    def get_input(self, filename):
        #Read in the input file and create array of the data points.
        p = re.compile('[-0-9]+')  #this should find the points on each line of the input (numeric + or -).  All integers.
        ia = []
        f = open(filename, 'r')
        for line in f:
            x,y = p.findall(line)
            ia.append([int(x),int(y)])
        f.close()
        return ia
    
    def write_map_to_file(self, m):
        #write the map to a file for analysis
        f = open(self.outfile, 'w')
        for i in range(len(m)):
            f.write("%s:%s" % (m[i], '\n'))
        f.close()
        