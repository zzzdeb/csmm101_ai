# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:02:04 2017

@author: zzz
"""
import pylab as plt
from GameManager_3 import GameManager
from Grid_3       import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_3   import PlayerAI
from Displayer_3  import Displayer

maxTiles = []
maxAITimes = []
AITimes = []
endGrids = []
depths = []
for i in range(5):
    gameManager = GameManager()
    playerAI  	= PlayerAI()
    computerAI  = ComputerAI()
    displayer 	= Displayer()

    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)

    maxTiles.append(gameManager.start())
    maxAITimes.append(gameManager.maxAITime)
    AITimes.append(gameManager.AITime)
    print("Play "+str(i+1)+":" + str(maxTiles[-1]))
    endGrids.append(gameManager.endGrid)
    depths.append(playerAI.depths)
    
for grid in endGrids:
    displayer.display(grid)
    
    
def sumTile(grid):
    sum = 0
    for i in range(grid.size):
        for j in range(grid.size):
            sum += grid.map[i][j]
    return sum
    
plt.figure('first')
plt.clf()
plt.subplot(232)
plt.xlabel('x')
plt.ylabel('y')
plt.plot(range(len(maxTiles)),maxTiles,label='MaxTiles')
plt.legend(loc='upper left')

plt.subplot(231)
for times in AITimes:
    plt.plot(range(len(times)),times, label=str(sum(times)/len(times)))
    
plt.legend(loc='upper right')

plt.subplot(233)
plt.plot(range(len(maxAITimes)),maxAITimes, label='MaxTimes')
plt.legend(loc='upper left')

plt.subplot(235)
plt.plot(range(len(maxAITimes)), list(map(lambda x: sum(x)/len(x), AITimes)) , label='avarageTimes')
plt.legend(loc='upper left')

plt.subplot(236)
plt.plot(range(len(maxAITimes)), list(map(lambda x: sumTile(x), endGrids)) , label='SumTiles')
plt.legend(loc='upper left')

f = open("IDA_Depth26810.txt","w")
for depth in depths:
    f.write(str(depth)+"\n")
f.close()

plt.savefig("IDA_Depth26810.pdf")

