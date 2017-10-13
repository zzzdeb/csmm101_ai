
import sys
import time
import resource

class State(object):

    def __init__(self, state, parent = [], dim):
        """" state : list """
        
        self.dim = dim
        self.state = state
        self.zero = state.index(0)
        self.child = {}
        self.parent = parent
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
        return State(self.child[direction], parent = self.state)
        
    def __str__(self):
        return self.state
        
    def __eq__(self, state):
        return self.state == state

    def __eq__(self, stateObj):
        return self.state == stateObj.state and self.parent == stateObj.parent


class heurState(State):
    
    def __init__(self, state, parent = []):
        State.__init__(self, state, parent = parent)
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

    def findParentInSet(node)
        """ node: State """
        return State(node.parent) 

    def genAns(self, node):
        """ node: State
            generates path"""
        if node.parent = []:
            return []
        else: 
            node.parent
            return genAns()
    
    def depthFinder(self, node):
        if node.parent = []:
            return 0
        else: 
            node.parent
            return depthFinder()+1

    def bfs(self):
        self.frontier.append(State(self.start, self.dim))
        self.frontierSet.add(str(self.frontier[0].state))
        while(len(self.frontier) != 0):
            
    #    pick  
            now = self.frontier.pop(0)
            self.frontierSet.remove(str(now.state))
            
        #explored
            self.explored.append(now)
            if now == self.goal:
                self.path=genAns(now)

                self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
                return self.path
        
    #    append
            for nb in range(4):
                i = 0
                try:
                    if now.child[nb] not in self.explored and now.child[nb] not in self.frontierList:
                        self.frontier.append(now.createChild(nb))
                        self.frontierSet.add(str(self.frontier[-1].state))
                except KeyError:
                    i+=1

            if i==4:
                self.max_search_depth = max(self.max_search_depth, depthFinder(now))
                
            self.max_fringe_size = max(self.max_fringe_size,len(self.frontier))
        return 0
        
       