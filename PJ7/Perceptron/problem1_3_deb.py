# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 19:27:59 2017

@author: zzz
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import sys

def f(x, w):
    """ calculates polynomial function 
        x: double 
        w: list     """
    ans = (w[0]+w[1]*x)/(-w[2])
    return ans
    
def Class(point, w):
    """ under the line. then 1 else -1 """
    if w[0]+w[1]*point[0]+w[2]*point[1] <0:
        return 1
    return -1
    
def Perception(data, output):
    out = open(output,"w")  #output file named output
    s = time.clock()    
    
    dax = data[:,0]
    day = data[:,1]
    w = np.ones(3, dtype="int")   #initiolaze weights
    
    converged = False
    while not converged:
#        b = np.polyfit(dax, day*w, 1)
#        b = np.polyfit(dax, w, 1)
#        print(b)
#        print(w)
        for i in range(len(data)):
            x = data[i][0]
            y = data[i][1]
            l = data[i][2]
            if Class((x,y),w) * l <0:
                w += (-l)*np.array([1,x,y])
                converged = True
        out.write(str(w[1])+","+str(w[2])+","+str(w[0])+"\n")
        converged = not converged
        
#        while True:
#            if time.clock()-s>0.1:
#                s = time.clock()                
#                break

    linx = np.array([np.min(dax),np.max(dax)])
    liny = f(linx,w)  
    plt.plot(linx, liny)


if __name__ == '__main__':
    data = np.genfromtxt(sys.argv[1], delimiter=",", dtype="int")
    Perception(data, sys.argv[2])
    dax = data[:,0]
    day = data[:,1]
    dal = data[:,2]
    
    
    
    blue = data[dal == 1]   # blue ==1
    red = data[dal != 1]    # red == -1
    
    #plt.figure("Perception")
    plt.plot(red[:,0], red[:,1], "ro", blue[:,0], blue[:,1], "bo")
    plt.show()
    
    

