# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:40:31 2017

@author: zzz
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import numpy as np

import sys


def plotPoints(data, fig):
    ax = fig.add_subplot(111, projection='3d')
    age = data[:,0]
    weight = data[:,1]
    height = data[:,2]
    ax.plot(age, weight, height, "o", label="data")
    ax.set_xlabel("Age (Years)")
    ax.set_ylabel("Weight (Kilogramms)")
    ax.set_zlabel("Height (Meters)") 
    ax.legend()
    
def plotFlat(x, y, b, fig):
    xmin = np.min(x)
    xmax = np.max(x)
    ymin = np.min(y)
    ymax = np.max(y)
    
    X = np.arange(xmin-0.5, xmax+0.5, 0.1)
    Y = np.arange(ymin-0.5, ymax+0.5, 0.1)
    X, Y = np.meshgrid(X,Y)
    Z = b[0]+X*b[1]+Y*b[2]
    fig.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.5)
    return 1
    
    
#def stdDev(data):
#    summe = np.sum((data-np.average(data))**2)
#    a = summe/len(data)
#    ans = a**0.5
#    return ans


#def f(x, y, b):
#    return b[0]+
    
def f(x, b):
    y = b[0]
    for i in range(len(x)):
        y +=x[i]*b[i+1]
    return y

def delta(x, y, b, i):
#    print("y: "+str(y))
    
    delta = np.sum((y - x[0]*b[0]-x[1]*b[1]-x[2]*b[2])*(-x[i]))/len(y)
    return delta

def linRegression(i, out, fig, alpha=1, numIter=100):
    """ x: age
        y: weight
        z: height """
    x_s = i[:,0]
    y_s = i[:,1]
    z_s = i[:,2]    
    # initielize b to zero
    b = np.zeros(len(i[0]))
    newb = np.copy(b)
    for i in range(numIter):
        newb[0] -= alpha*delta((1,x_s,y_s),z_s, b, 0)
        newb[1] -= alpha*delta((1,x_s,y_s),z_s, b, 1)
        newb[2] -= alpha*delta((1,x_s,y_s),z_s, b, 2)
        b = np.copy(newb)
    return b


if __name__ == "__main__":
    
    data = np.genfromtxt("input2.csv", delimiter=",")
    out = open("output2.csv","w")
    
    fig = plt.figure()
    #    plotPoints(data, fig)
    #features
    x = data[:,0]; y = data[:,1]; z = data[:,2]
    
    #scaled features
    x_s = (x-np.average(x))/np.std(x)
    y_s = (y-np.average(y))/np.std(y)
    z_s = (z-np.average(z))/np.std(z)
    scaledData = np.vstack((x_s, y_s, z_s)).T
    
    
    #plotting scaled features
    i = np.empty((len(x_s),3))
    i[:,0]=x_s
    i[:,1]=y_s
    i[:,2]=z
    plotPoints(i, fig)
    
    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.02]
    numIter = 100
    for alpha in alphas:
        if alpha == alphas[-1]:
            numIter=10000
        b = linRegression(i, out, fig, alpha=alpha, numIter=numIter)
        
        ans = [alpha, numIter]
        ans.extend(b)
        print(str(ans)[1:-1])
        out.write(str(ans)[1:-1]+"\n")
        
    ax = fig.gca(projection='3d')
    plotFlat(x_s, y_s ,b, ax)
        
x = np.array([[1,1,1,1,1],[2,2,2,2,2],[3,3,3,3,3]])
y = np.array([1,2,3,4,5])
b = np.array([1,2,3])
print(delta(x, y, b, 0))
print(delta(x, y, b, 1))
print(delta(x, y, b, 2))

out.close()
        
    