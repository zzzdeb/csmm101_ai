import time



class PlayerAI(object):
    def __init__(self):
        self.depths = {}
        
    def getMove(self, grid):        
        self.pruned = [0,0]
        s = time.clock()
        depth = 2
        (maxChildDir, maxUtility) = self.maxState(grid, 1, s,  depth = depth)
        depth = 4
        while True:
            depth+=2
            (tempMaxChild, temMaxUtility) = self.maxState(grid, 1, s, depth = depth)
            if tempMaxChild!=None:
                (maxChildDir, maxUtility) = (tempMaxChild, temMaxUtility)
            else:
                depth-=2
                break
        if maxChildDir==None:
            depth = 0
            maxChildDir = grid.getAvailableMoves()[0]
        if self.depths.get(depth,0):
            self.depths[depth]+=1
        else:
            self.depths[depth]=1
        print("Time: "+ str(time.clock()-s))
        print("maxUtility: "+ str(maxUtility))
        print("Pruned min max: "+ str(self.pruned))
        print("depht: " + str(depth))
        print(self.depths)
        return maxChildDir
        
  

        
    def minState(self, grid, layer, s, depth=3, alpha=-1, beta = 10000000000):
        
        if time.clock()-s>0.099:
            return (None,None)
        
        if layer==depth:
            return (0, self.ev(grid))
            
        (minChildDir, minUtility) = (-1, 10000000000)
        
        children = self.ChildsOfMin(grid)
        
        if not len(children):
            return (0, self.ev(grid))
            
        for child in children:
            (minChild, utility) = self.maxState(child, layer+1, s, depth = depth, alpha=alpha, beta = beta)
            
            if minChild == None:
                return (None,None)
                
            if utility<minUtility:
                (minChildDir, minUtility) = (minChild, utility)
            if utility<beta:
                beta = utility
            if alpha>=beta:
                self.pruned[0]+=1
                break

#        print("max Utility: "+str(maxUtility))
#        print("Time: "+ str(time.clock()-self.s))
#        print(grid.getAvailableMoves())
        return (minChildDir, minUtility)
    
    def maxState(self, grid, layer, s, depth = 3, alpha = -1, beta = 10000000000):

        if time.clock()-s>0.099:
            return (None,None)     
        
        if layer==depth:
            return (0, self.ev(grid))
            
        (maxChildDir, maxUtility) = (-1, -1)
        moves = grid.getAvailableMoves(dirs = [0,2,1,3])
        if not len(moves):
            return (0, self.ev(grid))
            
        for direc in moves:
            clone = grid.clone()
            clone.move(direc)
            (child, utility) = self.minState(clone, layer+1, s, depth = depth,  alpha=alpha, beta = beta)
#            (child, utility) = self.randomState(clone, 1)
            if child == None:
                return (None,None)
            if utility>maxUtility:
                (maxChildDir, maxUtility) = (direc, utility)
            if utility>alpha:
                alpha = utility
            if alpha>=beta:
                self.pruned[1]+=1
                break

#        print("max Utility: "+str(maxUtility))
#        print("Time: "+ str(time.clock()-self.s))
#        print(grid.getAvailableMoves())
        return (maxChildDir, maxUtility)
    
    def ev(self, grid):
        value = 0
#        value= (4+self.getNumZeros(grid))*grid.getMaxTile() + self.getSumTile(grid)
        
        heur1 = 0
        for x in range(grid.size):
            for y in range(grid.size):
                heur1 += grid.map[x][y]**2
#        heur2 = 0
#        for x in range(grid.size):
#            for i in range(2):
#                for j in range(0,3,2):
#                    try:
#                        if grid.map[x+i][x+j] == grid.map[x][x+1]:
#                            heur2 += grid.map[x+i][x+j] * grid.map[x][x+1]
#                    except IndexError:
#                        pass
#                    try:
#                        if grid.map[x+i][x+j] == grid.map[x+1][x]:
#                            heur2 += grid.map[x+i][x+j] * grid.map[x+1][x]
#                    except IndexError:
#                        pass
#                    try:
#                        if grid.map[x+i][x+j] == grid.map[x][x-1]:                        
#                            heur2 += grid.map[x+i][x+j] * grid.map[x][x-1]
#                    except IndexError:
#                        pass
#                    try:
#                        if grid.map[x+i][x+j] == grid.map[x-1][x]:
#                            heur2 += grid.map[x+i][x+j] * grid.map[x-1][x]
#                    except IndexError:
#                        pass
            
        heur3 = 0
#        maxTile = grid.getMaxTile()
#        for i in (0,3):
#            for j in (0,3):
#                if grid.map[i][j] == maxTile:
#                    heur3=heur1
#        heur4 = 0
#        maxTile = grid.getMaxTile()
#        for i in (0,3):
#            for j in (0,3):
#                heur4 += grid.map[i][j]*maxTile
#        for i in (1,2):
#            for j in (1,2):
#                heur4 += grid.map[i][j]*maxTile/2
#        for i in (1,2):
#            for j in (0,3):
#                heur4 += grid.map[i][j]*maxTile/4
#                heur4 += grid.map[i][j]*maxTile/4
        
        heur4 = 0
        x = [[1,2,4,8],
        [2,4,8,16],
        [4,8,16,32],
        [8,16,32,64]]
        maxTile = grid.getMaxTile()
        for i in range(4):
            for j in range(4):
                heur4 += maxTile*grid.map[i][j]/x[i][j]                
                
        value = heur1+heur3+heur4
#        print("heur1: "+ str(heur1))
#        print("heur2: "+ str(heur4))
        return value
    
    def ChildsOfMax(self, grid):
#        print(grid)
        children = []
        for direc in grid.getAvailableMoves():
            children.append(grid.clone())
            children[-1].move(direc)
        return children
    
    def ChildsOfMin(self, grid):
        """getAvailableCells: (x,y)"""
        children = []
        for pos in grid.getAvailableCells()[:2]:
            clone1 = grid.clone()
            clone2 = grid.clone()
            clone1.setCellValue(pos, 2)
            clone2.setCellValue(pos, 4)
            children.insert(0, clone1)
            children.append(clone2)

        return children
        
    def getSumTile(self, grid):
        sumTile = 0

        for x in range(grid.size):
            for y in range(grid.size):
                sumTile += grid.map[x][y]

        return sumTile
        
    def getNumZeros(self, grid):
        n = 0
        for x in range(grid.size):
            for y in range(grid.size):
                n += 1 if grid.map[x][y] ==0 else 0

        return n
    
    
    def randomState(self, grid, layer):
        if layer == 3:
            return (0, self.ev(grid))
        children = self.ChildsOfMin(grid)
        avarageWert = sum(map(lambda x: self.maxState(x, layer+1)[1], children))/len(children)
        
#        if layer==1:
#            for child in children:
#                for i in range(grid.size):
#                    for j in range(grid.size):
#                        print("%6d  " % child.map[i][j], end="")
#                    print("")
#                print("")
        print("Avarage Utility: Layer " + str(avarageWert) + " "+ str(layer))
        return (0, avarageWert)
#        
      