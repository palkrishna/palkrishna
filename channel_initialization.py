from  random import randrange
import numpy as np
from math import cos,sin,pi,log10,log2
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
def ch_gen(d2d_dist, num_d2d,C_frequency):
    
    ch_w_fading = np.zeros((num_d2d,num_d2d))
    multi_fading = 0.5 * np.random.randn(num_d2d, num_d2d) ** 2 + 0.5 * np.random.randn(num_d2d, num_d2d) ** 2
    rx_loc, tx_loc = loc_init(d2d_dist, num_d2d)
    for i in range(num_d2d) :         
      
      for j in range(num_d2d) :
          
          d =  np.linalg.norm(tx_loc[i] - rx_loc[j])                                        # distance vector has value of distance between each tx and rx                         
          if d<18:
            pu_ch_gain_db= 28 + 22 * log10(d) + 20 * log10(C_frequency)       # LOS pathloss
            pu_ch_gain = 10**(-pu_ch_gain_db/10)
          
          else :
            pu_ch_gain_db = 32.4 + 30 * log10(d) + 20 * log10(C_frequency)    # NLOS pathloss 
            pu_ch_gain = 10**(-pu_ch_gain_db/10)
          multi_fading = 0.5 * np.random.randn(num_d2d, num_d2d) ** 2 + 0.5 * np.random.randn(num_d2d, num_d2d) ** 2
          final_ch = (pu_ch_gain *(np.sum(multi_fading) ))
         # print(final_ch )
          ch_w_fading[i,j] = final_ch    
    return  ch_w_fading  