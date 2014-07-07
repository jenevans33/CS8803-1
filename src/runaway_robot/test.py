from numpy import *
from scipy import optimize



def calc_R(xc, yc):
    """ calculate the distance of each 2D points from the center (xc, yc) """
    return sqrt((x-xc)**2 + (y-yc)**2)

def f_2(c):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(*c)
    return Ri - Ri.mean()

t = [9.0, 35, -13, 10, 23, 0]
v = [ 34.0, 10, 6, -14,  27, -10]

x = r_[t]
y = r_[v]

print "x: ", x
print "y: ", y

x_m = mean(x)
y_m = mean(y)

print "x_m: ", x_m
print "y_m: ", y_m
center_estimate = x_m, y_m
center, ier = optimize.leastsq(f_2, center_estimate)

xc, yc = center
Ri       = calc_R(*center)
R        = Ri.mean()
residu   = sum((Ri - R)**2)

print "xc: ", xc
print "yc: ", yc
print "Ri: ", Ri
print "R: ", R
print "residu: ", residu