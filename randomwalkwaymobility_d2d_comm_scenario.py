############################ WMMSE Algorithm with mobile users with different speeds #######################################
import pandas as pd
from openpyxl import workbook,load_workbook
from  random import randrange,uniform
from  random import randrange,uniform
import numpy as np
from math import cos,sin,pi,log10,log2,sqrt
import pylab
######################## Simulation Parameters #################
bw = 1*10**9              # Bandwidth = 1GHz
p_t_dB = 23               # maximum d2d transmit power in dB
p_t = 10**(p_t_dB/10)      
C_frequency = 28         # carrier frequency = 28 GHz
num_d2d =4
Noise = -174               # noise = -174 dBm
s= 10**(-174/10)
d2d_dist = 50
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
def get_loc(rx_loc, tx_loc,num_d2d,speed) :
  for i in range(num_d2d):
        angle= randrange(0,360)
        r = speed*5/18
        angle=angle*pi/180
        tx_loc[i, 0] += r*cos(angle)
        tx_loc[i, 1] += r*sin(angle)
  for i in range(num_d2d):
        angle= randrange(0,360)
        r = speed*5/18
        angle=angle*pi/180
        rx_loc[i, 0] += r*cos(angle)
        rx_loc[i, 1] += r*sin(angle)
  return rx_loc, tx_loc
################### Algorithm defination #################
def WMMSE(num_d2d, H, Pmax, var_noise):
    k = num_d2d
    vnew = 0
    b = np.ones((k))*(sqrt(Pmax))
    f = np.zeros((k))
    w = np.zeros((k))
    for i in range(k):
        f[i] = H[i,i] * b[i] /(np.square(H[i,:]) @ np.square(b) + var_noise)
        w[i] = 1 / (1 - f[i] * b[i] * H[i, i])
        vnew = vnew + log2(w[i])

    VV = np.zeros(100)
    for iter in range(100):
        vold = vnew
        for i in range(k):
            btmp = w[i] * f[i] * H[i, i] / sum(w * np.square(f) * np.square(H[:, i]))
            b[i] = min(btmp, np.sqrt(Pmax)) + max(btmp, 0) - btmp

        vnew = 0
        for i in range(k):
            f[i] = H[i, i] * b[i] / ((np.square(H[i, :])) @ (np.square(b)) + var_noise)
            w[i] = 1 / (1 - f[i] * b[i] * H[i, i])
            vnew = vnew + log2(w[i])

        VV[iter] = vnew
        if vnew - vold <= 1e-3:
            break

    p_opt = np.square(b)
    return p_opt

######################## algorithm end ####################################
###############################  For creating excel sheets of value ####################################
 wb1=load_workbook('receiver1.xlsx')          
 ws1 = wb1.active

for speed in range(3,61,3) :
 sum_capacity =0  
 for iteration in range(50) :
  rx_loc, tx_loc = loc_init(d2d_dist, num_d2d)           # initializing tx-rx pairs location 
  cap = 0
  a=0

  for sim_time  in range(1000) :
     rx_loc, tx_loc = get_loc(rx_loc, tx_loc,num_d2d,speed)
     h=np.zeros((num_d2d,num_d2d))
     for i in range(num_d2d) :
      for j in range(num_d2d) :
        d =  np.linalg.norm(tx_loc[i] - rx_loc[j])
        pl_dB = 36.85 + 30*log10(d) +18.9*log10(C_frequency)
        pl = 10**(pl_dB/10)
        h[i,j] = 0.5 * np.random.randn() ** 2 + 0.5 * np.random.randn() ** 2
        h[i,j] = h[i,j]*pl
        
     p_opt=WMMSE(num_d2d,h,p_t,1)  
     print(p_opt)    
     for k in range(num_d2d):
       s = 1
       for l in range(num_d2d):
         if l!=k :
          s = s+h[k,l]**2*p_opt[l]

     for i in range(num_d2d) :
 #     for j in range(num_d2d) :
        d =  np.linalg.norm(tx_loc[i] - rx_loc[i])  
        if d < 100 :
            cap +=log2(1+h[i,j]**2*p_opt[j]/s)
            a+=1
 #           break
  sum_capacity += cap/a        
 sum_capacity =sum_capacity/50
 ws1.append([sum_capacity])
wb1.save('receiver1.xlsx')
