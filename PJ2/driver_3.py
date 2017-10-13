# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:01:13 2017

@author: zzz
"""
import sys
import time
import resource

class State(object):
    def __init__(self, state, parent = "", depth = 0):
        """ state: string
            parent: string: [state]+dir """
        self.state = state
#        self.child = {}
        self.parent = parent
        self.depth = depth
        
class heurState(State):
    
    def __init__(self, state, parent = "", depth = 0):
        State.__init__(self, state, parent = parent, depth = depth)
        self.heurVal = 0
        
    def __str__(self):
        return str(self.state)+" "+self.parent+" "+str(self.heurVal)+" "+str(self.pathVal)
                
class Solver(object):
    
    def __init__(self, start):
        self.start = start
        self.dim = int(len(start)**0.5)
        self.goal = [x for x in range(len(start))]
        self.explored = {}
        self.frontier = []
        self.frontierSet = set()
        self.path = []
        self.max_fringe_size = 0    #the maximum size of the frontier set in the lifetime of the algorithm
        self.max_search_depth = 0    #the maximum depth of the search tree in the lifetime of the algorithm
        self.running_time   = 0   #the total running time of the search instance, reported in seconds
        self.max_ram_usage  = 0  #the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes
        
    def output(self):
        f = open("output.txt","w")
        f.write("path_to_goal: " + str(self.path) + "\n")
        f.write("cost_of_path: " + str(len(self.path)) + "\n")
        f.write("nodes_expanded: " + str(len(self.explored)-1) + "\n")
        f.write("fringe_size: " + str(len(self.frontier)) + "\n")
        f.write("max_fringe_size: " + str(self.max_fringe_size) + "\n")
        f.write("search_depth: " + str(len(self.path)) + "\n") # again
        f.write("max_search_depth: " + str(self.max_search_depth) + "\n")
        f.write("running_time: "+ "%.8f" %self.running_time + "\n") 
        f.write("max_ram_usage: " + "%.8f" %self.max_ram_usage + "\n")
        f.close
        
    def genChild(self, state):
        """ state: list
            child: list: dir:string + state:list"""
        zero = state.index(0)
        children = []
        if not zero<self.dim:
            tempS = state[:]
            tempS[zero], tempS[zero-self.dim] = tempS[zero-self.dim], tempS[zero]
#            if str(nb[1:]) not in self.explored and str(nb[1:]) not in self.frontierSet:
            children.append(["0"]+tempS)
        if zero<len(state)-self.dim:
            tempS = state[:]
            tempS[zero], tempS[zero+self.dim] = tempS[zero+self.dim], tempS[zero]
            children.append(["1"]+tempS)
        if zero % self.dim:
            tempS = state[:]
            tempS[zero], tempS[zero-1] = tempS[zero-1], tempS[zero]
            children.append(["2"]+tempS)
        if not zero % self.dim == self.dim-1:
            tempS = state[:]
            tempS[zero], tempS[zero+1] = tempS[zero+1], tempS[zero] 
            children.append(["3"]+tempS)
        return children
        
    def genAns(self, state):
        """state: string"""
        if self.explored[state] == "":
            return 1
        self.path.insert(0, self.pathconvert(self.explored[state][-1]))
        return self.genAns(self.explored[state][:-1])
        
    def pathconvert(self, path):
        decr = {"0":"Up", "1":"Down", "2":"Left","3":"Right"}
        return decr[path]

    
    def depthFinder(self, state):
        """state: string"""
        if self.explored[state] == "":
            return 1
        return 1+self.depthFinder(self.explored[state][:-1])
        
    def solver(self):
        s = time.time()
        a = self.solve()
        self.running_time = time.time()-s
        self.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024.0)
        # self.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024.0)
        return a
        
class BFS(Solver):
    
    def __init__(self, start):
        Solver.__init__(self, start)
        
    def solve(self):
        self.frontier.append(State(self.start))
        self.frontierSet.add(str(self.start))
        while(len(self.frontier) != 0):
            
    #    pick  
            now = self.frontier.pop(0)
            self.frontierSet.remove(str(now.state))
            
        #explored
            self.explored[str(now.state)] = now.parent
            if now.state == self.goal:
                self.genAns(str(now.state))
#                self.max_search_depth = max(self.max_search_depth, now.depth)
#                self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
                return 1
        
    #    append
            children = self.genChild(now.state)
#            if len(children)==0:
#                self.max_search_depth = max(self.max_search_depth, now.depth)
#            else:
            for nb in children:
                """ nb = [dir, zahlen]"""
                if str(nb[1:]) not in self.explored and str(nb[1:]) not in self.frontierSet:
                    self.frontier.append(State(nb[1:], parent = str(now.state)+nb[0], depth = now.depth+1))
                    self.frontierSet.add(str(nb[1:]))
            self.max_search_depth = max(self.max_search_depth, self.frontier[-1].depth)
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
        return 0

class DFS(Solver):
    
    def __init__(self, start):
        Solver.__init__(self, start)
        
    def solve(self):
        self.frontier.append(State(self.start))
        self.frontierSet.add(str(self.start))
        while(len(self.frontier) != 0):
            
    #    pick  
            now = self.frontier.pop()
            self.frontierSet.remove(str(now.state))
            
        #explored
            self.explored[str(now.state)] = now.parent
            if now.state == self.goal:
                self.genAns(str(now.state))
#                self.max_search_depth = max(self.max_search_depth, now.depth)
#                self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
                return 1
        
    #    append
            children = self.genChild(now.state)
#            if len(children)==0:
#            else:
            for nb in children[::-1]:
                """ nb = [dir, zahlen]"""
                if str(nb[1:]) not in self.explored and str(nb[1:]) not in self.frontierSet:
                    self.frontier.append(State(nb[1:], parent = str(now.state)+nb[0], depth = now.depth+1))
                    self.frontierSet.add(str(nb[1:]))
            self.max_search_depth = max(self.max_search_depth, self.frontier[-1].depth)
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
        return 0
      
 
      
class AST(Solver):
    
    def __init__(self, start):
        Solver.__init__(self, start)
        
    def heuristic(self):
        a = min(self.frontier,key = lambda x: x.heurVal+x.depth)
        self.frontier.remove(a)
        self.frontierSet.remove(str(a.state))
        return a
        
#    def valueInit(self, state):
#        self.heurValInit(state)
#        state.pathVal = 1+self.depthFinder(state.parent[:-1])

    def heurValInit(self, state):
        for num in range(len(state.state)):
            state.heurVal += abs(num%self.dim - int(state.state[num])%self.dim)
            state.heurVal += abs(int(num/self.dim) - int(int(state.state[num])/self.dim))    
    
    def solve(self):
        self.frontier.append(heurState(self.start))
        self.frontierSet.add(str(self.start))
        while(len(self.frontier) != 0):
            
    #    pick  
            now = self.heuristic()
            
        #explored
            self.explored[str(now.state)] = now.parent
            if now.state == self.goal:
                self.genAns(str(now.state))
#                self.max_search_depth = max(self.max_search_depth, self.depthFinder(str(now.state)))
#                self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
                return 1
        
    #    append
            children = self.genChild(now.state)
#            if len(children)==0:
#                self.max_search_depth = max(self.max_search_depth, self.depthFinder(str(now.state)))
#            else:
            for nb in children[::-1]:
                """ nb = [dir, zahlen]"""
                if str(nb[1:]) not in self.explored and str(nb[1:]) not in self.frontierSet:
                    self.frontier.append(heurState(nb[1:], parent = str(now.state)+nb[0], depth = now.depth+1))
                    self.heurValInit(self.frontier[-1])
#                        print(self.frontier[-1])
                    self.frontierSet.add(str(nb[1:]))
            self.max_search_depth = max(self.max_search_depth, self.frontier[-1].depth)
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
        return 0
        
class IDA(AST):
    
    def __init__(self, start):
        AST.__init__(self, start)   
        self.idaList =[]

    def solver(self):
        s = time.time()
        a = self.solve(heurState(self.start))
        self.running_time = time.time()-s
        self.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024.0)
        return a


    def solve(self, start , depth = 6):
#        if type(start)==list:
#            self.frontier.append(heurState(start))
#        else:
        self.frontier.append(start)
        self.frontierSet.add(str(self.frontier[-1].state))
        
        
        while(len(self.frontier) != 0):
            
    #    pick  
            now = self.frontier.pop()
            self.frontierSet.remove(str(now.state))
            
        #explored
            self.explored[str(now.state)] = now.parent
            if now.state == self.goal:
                self.genAns(str(now.state))
#                self.max_search_depth = max(self.max_search_depth, self.depthFinder(str(now.state)))
#                self.max_fringe_size = max(self.max_fringe_size, len(self.frontier))
                return 1
        
    #    append
            children = self.genChild(now.state)
#            if len(children)==0:
#                self.max_search_depth = max(self.max_search_depth, self.depthFinder(str(now.state)))
#            else:
            for nb in children[::-1]:
                """ nb = [dir, zahlen]"""
                if str(nb[1:]) not in self.explored and str(nb[1:]) not in self.frontierSet:
                    temp = heurState(nb[1:], parent = str(now.state)+nb[0], depth=now.depth+1) 
                    self.heurValInit(temp)
                    if depth>temp.heurVal+temp.depth:                       
                        self.frontier.append(temp)
                        self.frontierSet.add(str(nb[1:]))
                    else:
                        self.idaList.append(temp)
            try:
                self.max_search_depth = max(self.max_search_depth, self.frontier[-1].depth)
            except IndexError:
                pass
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
        if len(self.idaList):
             return self.solve(self.idaList.pop(0), depth = depth+4)
        return 0

if __name__ == '__main__':
#    print(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)))
    assert len(sys.argv)==3
    start = list(map(lambda x: int(x), sys.argv[2].split(",")))
    # print(str(start))
    if sys.argv[1]=="bfs":
        x = BFS(start)
    elif sys.argv[1]=="dfs":
        x = DFS(start)
    elif sys.argv[1]=="ast":
        x = AST(start)
    elif sys.argv[1]=="ida":
        x = IDA(start)
    x.solver()
    x.output()

#x = BFS([1,2,5,3,4,0,6,7,8])
##print(x.solve())
##x.output()
#
#y = DFS([1,2,5,3,4,0,6,7,8])
##print(y.solve())
##y.output()
#
#z = IDA([1,2,5,3,4,0,6,7,8])
#print(z.solve([1,2,5,3,4,0,6,7,8], 10))
#z.output()
#
#k = AST([1,2,5,3,4,0,6,7,8])
##print(k.solve())
##k.output()
