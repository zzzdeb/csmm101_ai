# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:23:00 2017

@author: zzz
"""

#        for direc in moves:
#            clone = grid.clone()
#            clone.move(direc)
#            (child, utility) = self.minState(clone, 1)
##            (child, utility) = self.randomState(clone, 1)
#            if utility>maxUtility:
#                (maxChildDir, maxUtility) = (direc, utility)
#        print("max Utility: "+str(maxUtility))
#        print("Time: "+ str(time.clock()-self.s))
#        print(grid.getAvailableMoves())
#        return maxChildDir
#
#
#    def minState(self, grid, layer):
#        if layer==4:
#            return (0, self.ev(grid))
#        (minChild, minUt) = min(map(lambda x: self.maxState(x, layer+1), self.ChildsOfMin(grid)), key = lambda x: x[1])
#        return (minChild, minUt)



#    def maxState(self, grid, layer):
#        if layer==4:
#            return (0, self.ev(grid))
#        try:
#            (maxChild, maxUt) = max(map(lambda x: self.minState(x, layer+1), self.ChildsOfMax(grid)), key = lambda x: x[1])
##            (maxChild, maxUt) = max(map(lambda x: self.randomState(x, layer+1), self.ChildsOfMax(grid)), key = lambda x: x[1])
#        except ValueError:
#            return (0, self.ev(grid)/2)
#        print("Max: Layer " + str(maxUt) + " "+ str(layer))
#        return (maxChild, maxUt)