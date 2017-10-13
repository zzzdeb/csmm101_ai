# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 19:27:59 2017

@author: zzz
"""

import numpy as np
import sys
import matplotlib.pyplot as plt

def f(x, w):
    """ calculates polynomial function 
        x: double 
        w: list     """
    ans = (w[0]+w[1]*x)/(-w[2])
    return ans
    
def Class(point, w):
    """ under the line. then 1 else -1 """
    if w[0]+w[1]*point[0]+w[2]*point[1] >=0:
        return 1
    return -1
    
def Perceptron(data, output):
    out = open(output,"w")  #output file named output
    w = np.ones(3, dtype="int")   #initiolaze weights
    
    converged = False
    while not converged:
        for i in range(len(data)):
            x = data[i][0]
            y = data[i][1]
            l = data[i][2]
            if Class((x,y),w) * l <0:
                w += l*np.array([1,x,y])
                converged = True
        out.write(str(w[1])+","+str(w[2])+","+str(w[0])+"\n")
        converged = not converged
    

    
    return w

def make_prediction_grid(limits, w, delta=1):
    (xmin, xmax, ymin, ymax) = limits
    xs = np.arange(xmin-1, xmax+1, delta)
    ys = np.arange(ymin-1, ymax+1, delta)
    xx, yy = np.meshgrid(xs, ys)
    
    prediction_grid = np.zeros(xx.shape, dtype="int")
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            prediction_grid[j,i] = Class((x,y),w)
    return (xx, yy, prediction_grid)

def plot_prediction_grid (xx, yy, prediction_grid, filename):
    """ Plot KNN predictions for every point on the grid."""
    from matplotlib.colors import ListedColormap
    background_colormap = ListedColormap (["hotpink","lightskyblue", "yellowgreen"])
    background_colormap = ListedColormap (["lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap (["red","blue","green"])
    plt.figure(figsize =(10,10))
    plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
#    plt.scatter(predictors[:,0], predictors [:,1], c = outcomes, cmap = observation_colormap, s = 50)
    plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
    plt.xticks(()); plt.yticks(())
    plt.xlim (np.min(xx)-1, np.max(xx)+1)
    plt.ylim (np.min(yy)-1, np.max(yy)+1)

    
if __name__ == '__main__':
    data = np.genfromtxt(sys.argv[1], delimiter=",", dtype="int")
    w = Perceptron(data, sys.argv[2])
    
    dax = data[:,0]
    day = data[:,1]
    dal = data[:,2]
    
    limits = (np.min(dax)-1, np.max(dax)+1, np.min(day)-1, np.max(day)+1)
    xx, yy, prediction_grid =make_prediction_grid(limits, w)
    plot_prediction_grid(xx, yy, prediction_grid, "Perceptron.pdf")
    
    blue = data[dal == 1]   # blue ==1
    red = data[dal != 1]    # red == -1
    
#    plt.figure("Perception")
    plt.plot(red[:,0], red[:,1], "ro", blue[:,0], blue[:,1], "bo")
    plt.show()

