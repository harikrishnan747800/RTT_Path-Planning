#Program to implement RRT Algorithm


import pygame
from RRTbg import RRTGraph
from RRTbg import RRTMap

def main():
    #test values   PLEASE ENTER THE VALUES HERE
    #dimensions=(500,500)  #input the values here for the Dimension of the map
    #start=(0,0)   #input the starting coordinates
    #goal=(500,500) #input the Goal Coordinates
    #obsdim=30  #Obstacles
    #obsnum=50  #obstacles Number
    dimes=input("Enter the Dimensions of display seperated by space").strip().split()
    xys=input("Enter the starting coordinates seperated by space").strip().split()
    xyg=input("Enter the goal coordinates seperated by space").strip().split()
    dx=int(dimes[0])
    dy=int(dimes[1])
    xs=int(xys[0])
    ys=int(xys[1])
    xg=int(xyg[0])
    yg=int(xyg[1])
    dimensions=(int(dx),int(dy))  
    start=(int(xs),int(ys))   
    goal=(int(xg),int(yg)) 
    obsdim=30  
    obsnum=50  
    iteration=0
    #Plotting the Map using Pygame
    pygame.init()
    map=RRTMap(start,goal,dimensions,obsdim,obsnum)
    graph=RRTGraph(start,goal,dimensions,obsdim,obsnum)
    #Creating Map  [MakeObs->drawMap->drawObs]
    obstacles=graph.makeobs()       
    map.drawMap(obstacles)
    
    #################################
    #Initial Map checking Code
    #################################
    #while(True):
        #x,y=graph.sample_envir()                  #Creating Random nodes
        #n=graph.number_of_nodes()                 #Calculate number of nodes
        #graph.add_node(n,x,y)                     #The function first checks for the validity of nodes and then adds it
        #graph.add_edge(n-1,n)                     #The function checks the vailidity of edges/connections and then adds it
        #x1,y1=graph.x[n],graph.y[n]
        #x2,y2=graph.x[n-1],graph.y[n-1]
        #if (graph.isFree()):                      #Draw it in the map Also, this if condition checks if the obstacle do not overlap the nodes.First the nodes appear then the obstacles are loaded.
        #    pygame.draw.circle(map.map,map.Red,(graph.x[n],graph.y[n]),map.noderad,map.nodeThickness)
         #   if graph.crossObstacle(x1,x2,y1,y2):
         #       pygame.draw.line(map.map,map.Blue,(x1,y1),(x2,y2),map.edgeThickness)
    #################################
    #################################

    while(not graph.path_to_goal()):  #The loop terminates if path is not found
        if iteration%10==0:  #Call bias every 10th iteration
            X,Y,Parent=graph.bias(goal)
            pygame.draw.circle(map.map,map.Grey,(X[-1],Y[-1]),map.noderad*2,0)
            pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]),map.edgeThickness)
        else:
            X,Y,Parent=graph.expand()
            pygame.draw.circle(map.map,map.Grey,(X[-1],Y[-1]),map.noderad*2,0)
            pygame.draw.line(map.map,map.Blue,(X[-1],Y[-1]),(X[Parent[-1]],Y[Parent[-1]]),map.edgeThickness)
        if iteration %5==0:
            pygame.display.update()
        iteration+=1
    map.drawPath(graph.getPathCoords())                           
    pygame.display.update()
    pygame.event.clear()
    pygame.event.wait(0)
    
if __name__== '__main__':
   # main()
    result=False
    while not result:
        try:
            main()
            result=True
        except:
            result=False
    
    
