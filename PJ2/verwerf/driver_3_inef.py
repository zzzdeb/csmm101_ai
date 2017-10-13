# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:41:37 2017

@author: zzz
"""
import sys
import time
import resource

#!/usr/bin/python

class NotPossible(Exception):
    pass
#
class State(object):

    def __init__(self, state, parent = "", path=[]):
        """" state : list """
        
        self.dim = int(len(state)**0.5)
        self.state = state
        self.zero = state.index(0)
        self.child = {}
        self.parent = parent
        self.path = path
        self.childGen()
        
    def childGen(self):
        """ 0 - Up, 1 - Down, 2 - Left, 3 - Right"""
        if not self.zero<self.dim:
            tempS = self.state[:]
            tempS[self.zero] = tempS[self.zero-self.dim]
            tempS[self.zero-self.dim] = 0
            self.child[0] = tempS
        if self.zero<len(self.state)-self.dim:
            tempS = self.state[:]
            tempS[self.zero] = tempS[self.zero+self.dim]
            tempS[self.zero+self.dim] = 0
            self.child[1] = tempS
        if self.zero % self.dim:
            tempS = self.state[:]
            tempS[self.zero] = tempS[self.zero-1]
            tempS[self.zero-1] = 0
            self.child[2] = tempS
        if not self.zero % self.dim == self.dim-1:
            tempS = self.state[:]
            tempS[self.zero] = tempS[self.zero+1]
            tempS[self.zero+1] = 0
            self.child[3] = tempS
    def createChild(self, direction):
        return State(self.child[direction], parent = self.state, path = self.path + [direction])
        
    def __str__(self):
        return self.state
        
    def __eq__(self, state):
        return self.state == state
  
    # def inFrontier(self, nb,  frontier):
    #     for front in frontier:
    #         if self.child[nb] == front.state:
    #             return 1
    #     return 0
        
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
    
    def __init__(self, method, start):
        self.method = method
        self.start = start
        self.dim = len(start)**0.5
        self.goal = [x for x in range(len(start))]
        self.explored = []
        self.frontier = []
        self.frontierList = []
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
        self.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)
        # f = open(self.method+".txt","w")
        f = open("output.txt","w")
        f.write("path_to_goal: " + str(self.pathconvert(self.path)) + "\n")
        f.write("cost_of_path: " + str(len(self.path)) + "\n")
        f.write("nodes_expanded: " + str(len(self.explored)-1) + "\n")
        f.write("fringe_size: " + str(len(self.frontier)) + "\n")
        f.write("max_fringe_size: " + str(self.max_fringe_size) + "\n")
        f.write("search_depth: " + str(len(self.path)) + "\n") # again
        f.write("max_search_depth: " + str(self.max_search_depth) + "\n")
        f.write("running_time: "+ "%.8f" %self.running_time + "\n") 
        f.write("max_ram_usage: " + "%.8f" %self.max_ram_usage + "\n")
        f.close
        return a

    def pathconvert(self, path):
        decr = {0:"Up", 1:"Down", 2:"Left",3:"Right"}
        return list(map(lambda x: decr[x], path))

    def bfs(self):
        self.frontier.append(State(self.start))
        self.frontierList.append(self.frontier[0].state)
        while(len(self.frontier) != 0): 
            
    #    pick  
            now = self.frontier.pop(0)
            del self.frontierList[0]
            
        #explored
            self.explored.append(now.state)
            if now == self.goal:
                self.path=now.path
                return self.path
        
    #    append
            for nb in range(4):
                try:
                    if now.child[nb] not in self.explored and now.child[nb] not in self.frontierList:
                        self.frontier.append(now.createChild(nb))
                        self.frontierList.append(self.frontier[-1].state)
                except KeyError:
                    pass  
            try:
                self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))
            except IndexError:
                pass
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
#                    self.frontierList.append(self.frontier[-1].state)

        return 0
        
        
    def dfs(self):
         self.frontier.append(State(self.start))
         self.frontierList.append(self.frontier[0].state)
         i = 1
    #         print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
         while(len(self.frontier) != 0): 
            if int(len(self.frontier)/(i*1000)):
                 print(str(len(self.frontier)))
    #                 print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
                 i+=1
     #            file = open("debug.txt", "a")
     #            for front in self.frontier:
     #                file.write(str(front)+" ")
     #            file.write("\n")
     #    pick  
            now = self.frontier.pop()
            del self.frontierList[-1]
         #explored
            self.explored.append(now.state)
            if now == self.goal:
                 self.path=now.path
    #                 print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
                 return self.path
        
     #    append
            for nb in range(3,-1,-1):
                try:
                    if now.child[nb] not in self.explored and now.child[nb] not in self.frontierList:
                        self.frontier.append(now.createChild(nb))
                        self.frontierList.append(self.frontier[-1].state)
                except KeyError:
                    pass
            try:
                self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))
            except IndexError:
                pass
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
     #                    self.frontierList.append(self.frontier[-1].state)
    
         return 0
        
    def heuristic(self):
         a = min(self.frontier,key = lambda x: x.heurVal+len(x.path))
         self.frontier.remove(a)
         self.frontierList.remove(a.state)
         return a
        
    def ast(self):
         self.frontier.append(heurState(self.start))
         self.frontierList.append(self.frontier[0].state)
         i = 1
    #         print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
         while(len(self.frontier) != 0): 
            if int(len(self.frontier)/(i*1000)):
                 print(str(len(self.frontier)))
    #                 print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
                 i+=1
     #            file = open("debug.txt", "a")
     #            for front in self.frontier:
     #                file.write(str(front)+" ")
     #            file.write("\n")
     #    pick  
            now = self.heuristic()
            
         #explored
            self.explored.append(now.state)
            if now == self.goal:
                 self.path=now.path[:]
    #                 print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
                 return self.path
        
     #    append
            for nb in range(4):
                try:
                    if now.child[nb] not in self.explored and now.child[nb] not in self.frontierList:
                        self.frontier.append(now.createChild(nb))
                        self.frontierList.append(self.frontier[-1].state)
#                        print(str(len(self.frontier)))
                except KeyError:
                    pass  
#            print("\n")
            try:
                self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))
            except IndexError:
                pass
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
     #                    self.frontierList.append(self.frontier[-1].state)
    
         return 0    
         
    def ida(self, start, depth):
        
         if type(start) == list:
             self.frontier.append(heurState(self.start))
         else:
             self.frontier.append(start)
         self.frontierList.append(self.frontier[0].state)
            
            
         while(len(self.frontier) != 0): 
            
     #    pick  
             now = self.frontier.pop()
             self.frontierList.remove(now.state)
         #explored
             self.explored.append(now.state)
             if now == self.goal:
                 self.path=now.path[:]
                 return self.path
        
     #    append
             for nb in range(3,-1,-1):
                 try:
                     if now.child[nb] not in self.explored:
     #                    if not now.inFrontier(nb, self.frontier):
                         if  now.child[nb] not in self.frontierList:
                             temp = now.createChild(nb)                        
                             if depth>temp.heurVal+len(temp.path):
                                 self.frontier.append(temp)
                                 self.frontierList.append(self.frontier[-1].state)
                             else:
                                 self.idaList.append(now)                            
     #                        print(self.frontier[-1])
                 except KeyError:
                    pass
                 self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
             try:
                 self.max_search_depth = max(self.max_search_depth, len(self.frontier[-1].path))
             except IndexError:
                 pass
         if len(self.idaList):
             return self.ida(self.idaList[0], depth+3)
         return 0
#         self.frontierList.append(self.frontier[-1].state)
        
    
if __name__ == '__main__':
#    print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
    assert len(sys.argv)==3
    start = list(map(lambda x: int(x), sys.argv[2].split(",")))
    # print(str(start))
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
