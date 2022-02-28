from  random import randrange,uniform
import numpy as np
from math import cos,sin,pi,log10,log2
import pylab
################### Initializing position of rx and tx in circular form #########################
def loc_init(d2d_dist, num_d2d):
    r=100         # radius of circle
    rx_loc = np.zeros((num_d2d , 2))
    tx_loc = np.zeros((num_d2d , 2))
    for i in range(num_d2d):
        angle= randrange(0,360)
        angle=angle*pi/180
        tx_loc[i, 0] = r*cos(angle)
        rx_loc[i, 0] = r*cos(angle) + d2d_dist
        tx_loc[i, 1] = r*sin(angle)
        rx_loc[i,1] = r*sin(angle)    
    return rx_loc, tx_loc
d2d_dist =50
num_d2d = 1
rx_loc, tx_loc = loc_init(d2d_dist, num_d2d)
xtx = np.zeros(1000) # x and y are arrays which store the coordinates of the position 
ytx = np.zeros(1000)
xrx = np.zeros(1000) # x and y are arrays which store the coordinates of the position 
yrx = np.zeros(1000)
for z in range (1000):
  for i in range(num_d2d):
        angle= randrange(0,360)
        r = uniform(0.8,2.8)
        angle=angle*pi/180
        tx_loc[i, 0] += r*cos(angle)
        xtx[z]= tx_loc[i, 0]
        tx_loc[i, 1] += r*sin(angle)
        ytx[z]= tx_loc[i, 1]
  for i in range(num_d2d):
        angle= randrange(0,360)
        r = uniform(0.8,2.8)
        angle=angle*pi/180
        rx_loc[i, 0] += r*cos(angle)
        xrx[z]= rx_loc[i, 0]
        rx_loc[i, 1] += r*sin(angle)
        yrx[z]= rx_loc[i, 1]      
pylab.title("Random Walk tx-rx pair") #plotting the walk.
pylab.xlabel('x - axis')
pylab.ylabel('y - axis')
pylab.plot(xtx, ytx,label = "tx")
pylab.plot(xrx, yrx,label ="rx" )
pylab.show()