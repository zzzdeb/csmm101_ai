# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:41:37 2017

@author: zzz
"""
import sys
import time
#import resource

#!/usr/bin/python

class NotPossible(Exception):
    pass
#
class State(object):

    def __init__(self, state, parent = "", path=[]):
        """" state : string 0-8 """
        
        self.dim = int(len(state)**0.5)
        self.state = state
        self.zero = state.find("0")
        self.child = {}
        self.parent = parent
        self.path = path
        self.keys = []
        self.childGen()
        
    def childGen(self):
        if not self.zero<self.dim:
            tempL = self.state[self.zero-self.dim]
            self.child["Up"] = self.state.replace(tempL, " ").replace("0", tempL).replace(" ", "0")
            self.keys.append("Up")            
        if self.zero<len(self.state)-self.dim:
            tempL = self.state[self.zero+self.dim]
            self.child["Down"] = self.state.replace(tempL, " ").replace("0", tempL).replace(" ", "0")
            self.keys.append("Down")
        if self.zero % self.dim:
            tempL = self.state[self.zero-1]
            self.child["Left"] = self.state.replace(tempL, " ").replace("0", tempL).replace(" ", "0")
            self.keys.append("Left")
        if not self.zero % self.dim == self.dim-1:
            tempL = self.state[self.zero+1]
            self.child["Right"] = self.state.replace(tempL, " ").replace("0", tempL).replace(" ", "0")
            self.keys.append("Right")
    def createChild(self, direction):
        return State(self.child[direction], parent = self.state, path = self.path + [direction])
        
    def __str__(self):
        return self.state
        
    def __eq__(self, state):
        return self.state == state
  
    def inFrontier(self, nb,  frontier):
        for front in frontier:
            if self.child[nb] == front.state:
                return 1
        return 0
        
class heurState(State):
    
    def __init__(self, state, parent = "", path=[]):
        State.__init__(self, state, parent = parent, path=path)
        self.heurVal = 0
        self.heurValInit()
        
    def heurValInit(self):
        for num in range(len(self.state)):
            self.heurVal += abs(num%self.dim - int(self.state[num])%self.dim)
            self.heurVal += abs(int(num/self.dim) - int(int(self.state[num])/self.dim))
        
    def createChild(self, direction):
        return heurState(self.child[direction], parent = self.state, path = self.path + [direction])
    

class Solver(object):
    
    def __init__(self, method, start, goal="012345678"):
        self.method = method
        self.start = start
        self.goal = goal
        self.dim = len(start)**0.5
        self.explored = set()
        self.frontier = []
        self.frontierSet = set()
        self.path = []
        self.max_fringe_size = 0    #the maximum size of the frontier set in the lifetime of the algorithm
        self.max_search_depth = 0    #the maximum depth of the search tree in the lifetime of the algorithm
        self.running_time   = 0   #the total running time of the search instance, reported in seconds
        self.max_ram_usage        = 0  #the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes
        self.idaList =[]        
        
    def solve(self):
        s = time.time()
        if self.method == "bfs":
            a = self.bfs()
        elif self.method == "dfs":
            a = self.dfs()
        elif self.method == "ast":
            a = self.ast()
        elif self.method == "ida":
            a = self.ida(self.start, 3)
        self.running_time = time.time() - s
        f = open(self.method+".txt","w")
        f.write("path_to_goal: " + str(self.path) + "\n")
        f.write("cost_of_path: " + str(len(self.path)) + "\n")
        f.write("nodes_expanded: " + str(len(self.explored)-1) + "\n")
        f.write("fringe_size: " + str(len(self.frontier)) + "\n")
        f.write("max_fringe_size: " + str(self.max_fringe_size) + "\n")
        f.write("search_depth: " + str(len(self.path)) + "\n") # again
        f.write("max_search_depth: " + str(self.max_search_depth) + "\n")
        f.write("running_time: "+ "%.8f" %self.running_time + "\n") 
        f.write("max_ram_usage: " + str(self.max_ram_usage) + "\n")
        f.close
        return a

    def bfs(self):
        self.frontier.append(State(self.start))
#        self.frontierList.append(self.frontier[0].state)
        while(len(self.frontier) != 0): 
            
    #    pick  
            now = self.frontier[0]
            del self.frontier[0]
#            del self.frontierList[0]
            
        #explored
            self.explored.add(now.state)
            if now == self.goal:
                self.path=now.path[:]
                return self.path
        
    #    add
            for nb in now.keys:
                if now.child[nb] not in self.explored:
                    self.frontier.append(now.createChild(nb))
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
            self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))
#                    self.frontierList.append(self.frontier[-1].state)

        return 0
        
    def dfs(self):
        self.frontier.append(State(self.start))
        self.frontierSet.add(self.frontier[0].state)
        i = 1
        while(len(self.frontier) != 0): 
            if int(len(self.frontier)/(i*1000)):
                print(str(len(self.frontier)))
                i+=1
#            file = open("debug.txt", "a")
#            for front in self.frontier:
#                file.write(str(front)+" ")
#            file.write("\n")
    #    pick  
            now = self.frontier.pop()
            self.frontierSet.remove(now.state)
        #explored
            self.explored.add(now.state)
            if now == self.goal:
                self.path=now.path[:]
                return self.path
        
    #    add
            for nb in now.keys[::-1]:
                if now.child[nb] not in self.explored:
#                    if not now.inFrontier(nb, self.frontier):
                    if not now.child[nb] in self.frontierSet:
                        self.frontier.append(now.createChild(nb))
                        self.frontierSet.add(self.frontier[-1].state)
#                        print(self.frontier[-1])
                        
            
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
            self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))
#                    self.frontierList.append(self.frontier[-1].state)

        return 0
        
    def heuristic(self):
        a = min(self.frontier,key = lambda x: x.heurVal+len(x.path))
        self.frontier.remove(a)
        return a
        
    def ast(self):
        self.frontier.append(heurState(self.start))
#        self.frontierList.append(self.frontier[0].state)
        while(len(self.frontier) != 0): 
            
    #    pick  
            now = self.heuristic()
#            del self.frontierList[0]
            
        #explored
            self.explored.add(now.state)
            if now == self.goal:
                self.path=now.path[:]
                return self.path
        
    #    add
            for nb in now.keys:
                if now.child[nb] not in self.explored:
                    self.frontier.append(now.createChild(nb))
#                    self.frontierList.append(self.frontier[-1].state)
                    
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
            self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))

        return 0
    
    def ida(self, start, depth):
        
        if type(start) == str:
            self.frontier.append(heurState(self.start))
        else:
            self.frontier.append(start)
        self.frontierSet.add(self.frontier[0].state)
            
            
        while(len(self.frontier) != 0): 
            
    #    pick  
            now = self.frontier.pop()
            self.frontierSet.remove(now.state)
        #explored
            self.explored.add(now.state)
            if now == self.goal:
                self.path=now.path[:]
                return self.path
        
    #    add
            for nb in now.keys[::-1]:
                if now.child[nb] not in self.explored:
#                    if not now.inFrontier(nb, self.frontier):
                    if  now.child[nb] not in self.frontierSet:
                        temp = now.createChild(nb)                        
                        if depth>temp.heurVal+len(temp.path):
                            self.frontier.append(temp)
                            self.frontierSet.add(self.frontier[-1].state)
                        else:
                            self.idaList.append(now)                            
#                        print(self.frontier[-1])
            try:
                self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
                self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))
            except IndexError:
                pass
        if len(self.idaList):
            return self.ida(self.idaList[0], depth+3)
        return 0
#                    self.frontierList.append(self.frontier[-1].state)
        
    
if __name__ == '__main__':
    assert len(sys.argv)==3
    start = sys.argv[2].replace(",","")
    solver = Solver(sys.argv[1], start)
    solver.solve()


#==============================================================================
# output.txt
# path_to_goal = answer: the sequence of moves taken to reach the goal
# cost_of_path = len(answer): the number of moves taken to reach the goal
# nodes_expanded = len(explored): the number of nodes that have been expanded
# fringe_size = len(frontier): the size of the frontier set when the goal node is found
# max_fringe_size: the maximum size of the frontier set in the lifetime of the algorithm
# search_depth = costofpath: the depth within the search tree when the goal node is found
# max_search_depth = :  the maximum depth of the search tree in the lifetime of the algorithm
# running_time = : the total running time of the search instance, reported in seconds
# max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes
#==============================================================================
