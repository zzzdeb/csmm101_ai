# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 13:39:23 2017

@author: zzz
"""

from sklearn import svm
from sklearn.model_selection import train_test_split, cross_val_score

import numpy as np

from sklearn.metrics import classification_report

data = np.genfromtxt("input3.csv", skip_header=1, delimiter=",")
print(data)
#Classification(data)
#import matplotlib.pyplot as plt

#def Classification(data):
output = open("output3.csv", "w")
C_lin = [0.1, 0.5, 1, 5, 10, 50, 100]

C_pol = [0.1, 1, 3]; degree = [4,5,6]; gammaPol = [0.1, 1]

C_rbf = [0.1, 0.5, 1, 5, 10, 50, 100]; gammaRbf = [0.1, 1]

C_log = [0.1, 0.5, 1, 5, 10, 50, 100]

#k-Nearest Neighbors
n_neighbors = [i for i in range(1,51)]
leaf_size = [i for i in range(5,61,5)]

#Decision Trees
max_depth = [i for i in range(1,51)]
min_samples_split = [i for i in range(2,11)]

#Rnadom Forest
#gleich wie Decision Trees

#data Seperation
X = data[:,:2]
Y = data[:,2]
X_tr, X_test, Y_tr, Y_test = train_test_split(X, Y, test_size=0.4)

##lin
#print("Linear ")
#testScore = -1
#bestScore = -1
#for C in C_lin:
#    clf = svm.SVC(kernel="linear", C=C)#.fit(X_tr, Y_tr)
#    scores = cross_val_score(clf, X_tr, Y_tr, cv=5)
#    print(scores)
#
#    if scores.mean() > bestScore:
#        bestScore = scores.mean()
#        clf_best = clf
#clf_best.fit(X_test, Y_test)
#testScore = clf_best.score(X_test, Y_test)
#        
#print("svm_linear, "+str(bestScore) + ", "+str(testScore)+", "+str(clf_best.C)+"\n")
#output.write("svm_linear, "+str(bestScore) + ", "+str(testScore)+", "+str(clf_best.C)+"\n")
#output.close()

#pol
print("Pol")
for C in C_pol:
    for deg in degree:
#            for gam in gammaPol:
#            clf = svm.SVC(kernel="poly", C=C, degree=deg, gamma=gam)
        clf = svm.SVC(kernel="poly", C=C, degree=deg).fit(X_tr, Y_tr)
        scores = cross_val_score(clf, X_tr, Y_tr, cv=5)
        print(scores)
        
        if scores.mean() > bestScore:
            bestScore = scores.mean()        
            clf_best = clf
#        clf_best
        testScore = clf.predict(X_test)
        print(classification_report(Y_test, testScore))
#        print(str(testScore))
        
output.write("svm_linear, "+str(bestScore) + ", "+str(testScore)+", "+str(clf_best.C)+"\n")

#return 1



    