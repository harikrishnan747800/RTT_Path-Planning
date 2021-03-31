import random 
import math
import pygame

class RRTMap:
    def __init__(self,start,goal,MapDimensions,obsdim,obsnum):  #inputs are starting point, end point the map dimension and obstacle dimensions and numbers 
        self.start=start
        self.goal=goal
        self.MapDimensions=MapDimensions
        self.Maph,self.Mapw=self.MapDimensions #Splitting dimensions 
        self.MapWindowName="Output"
        #For pygame 
        pygame.display.set_caption(self.MapWindowName)
        self.map=pygame.display.set_mode((self.Mapw,self.Maph))
        self.map.fill((255,255,255))
        self.noderad=2
        self.nodeThickness=0
        self.edgeThickness=1
        self.obstacles=[]  #Obstacles will be stored inside this list
        self.obsdim=obsdim
        self.obsNumber=obsnum
        #defining colours for the map components
        self.Grey=(70,70,70)
        self.Blue=(0,0,255)
        self.Green=(0,255,0)
        self.Red=(255,0,0)
        self.White=(255,255,255)
        
        
    def drawMap(self,obstacles):  #This is to ensure that the start and end positions are circled Green to differentiate between the nodes
        pygame.draw.circle(self.map,self.Green,self.start,self.noderad+5,0)  #SYNTAX for draw.circle is surface/display(i.e. map) then colour, size(radius) and then line thickness
        pygame.draw.circle(self.map,self.Green,self.goal,self.noderad+20,1)
        self.drawObs(obstacles)  #calling the method to create the obstacles on the map

    def drawPath(self, path):  #This method makes the valid nodes Red in colour to differentiate it amongst the random nodes
        for node in path:
            pygame.draw.circle(self.map, self.Red, node,3, 0)

    def drawObs(self,obstacles):  #Taking out each obstacle created by the method "makeobs" and creating a rectangle for it
        obstacleList=obstacles.copy()
        while (len(obstacleList)>0):
            obstacle=obstacleList.pop(0)
            pygame.draw.rect(self.map,self.Grey,obstacle)   #SYNTAX for draw.rect is the display(i.e. map in this case) then colour, object(i.e. the obstacle)
        
    
class RRTGraph:
    def __init__(self,start,goal,MapDimensions,obsdim,obsnum):
        (x,y)=start
        self.start=start
        self.goal=goal
        self.goalFlag=False
        self.maph,self.mapw=MapDimensions
        self.x=[]
        self.y=[]
        self.parent=[]
        #Appending the start nodes to tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)#start node hence 0
        #Defining obstacles
        self.obstacles=[]
        self.obsDim=obsdim
        self.obsNum=obsnum
        #Checking the traversal
        self.goalstate=None
        self.path=[]

        #Creating obstacles
    def makeRandomRect(self):
        uppercornerx=int(random.uniform(0,self.mapw-self.obsDim)) #Subtracting from the Dimensions to ensure that the obstacles do not becomes greater than the map itself
        uppercornery=int(random.uniform(0,self.maph-self.obsDim))
        return (uppercornerx,uppercornery)
    
    #Using the above method to create the obstacles now. Considering only rectanglular obstacles in the map
    def makeobs(self):
        obs=[]
        for i in range(0,self.obsNum):
            rectang=None
            startgoalcol=True
            while startgoalcol:
                upper=self.makeRandomRect()
                rectang=pygame.Rect(upper,(self.obsDim,self.obsDim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol=True
                else:
                    startgoalcol=False #Terminates the while loop as this means that obstacle is on the start or end point
                obs.append(rectang)
            self.obstacles=obs.copy()#If successful, copy the list of obstacles to the obstacles class
        return obs
                    
                
    def add_node(self,n,x,y):  #To create nodes in the map by taking inputs -Node Number,(x,y) coordinates
        self.x.insert(n,x)
        self.y.append(y)
    def remove_node(self,n):   #To remove a node by using its node number
        self.x.pop(n)
        self.y.pop(n)
        
    def add_edge(self,parent,child):  #To create an edge by considering child as index and parent as element
        self.parent.insert(child,parent)
        
    def remove_edge(self,n): #Removing edge by removing the parent
        self.parent.pop(n)
        
    def number_of_nodes(self):
        return len(self.x)
    
    def distance(self,n1,n2):#Calculating Eucelidan Distance
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        px=(float(x1)-float(x2))**2
        py=(float(y1)-float(y2))**2
        return (px+py)**(0.5)

    def sample_envir(self): #Random Sampling by considering map borders as limits
        x=int(random.uniform(0,self.mapw))
        y=int(random.uniform(0,self.maph))
        return x,y
    
    def nearest(self,n):  #Checks for the nearest node present
        dmin=self.distance(0,n)
        nnear=0  #Closest node number
        for i in range(0,n):
            if self.distance(i,n)<dmin:
                dmin=self.distance(i,n)
                nnear=i
        return nnear

    def step(self,nnear,nrand,dmax=35):  #Creating the new Node
        d=self.distance(nnear,nrand)
        if d>dmax:
            u=dmax/d
            (xnear,ynear)=(self.x[nnear],self.y[nnear])
            (xrand,yrand)=(self.x[nrand],self.y[nrand])
            (px,py)=(xrand-xnear,yrand-ynear)   #Creating the node between 2 nodes(the new node creation)
            theta=math.atan2(py,px)
            (x,y)=(int(xnear+ dmax * math.cos(theta)),int(ynear+dmax*math.sin(theta)))
            self.remove_node(nrand)  #pop the old node.
            if abs(x-self.goal[0])<=dmax and abs(y-self.goal[1])<=dmax: #Check if we found the goal
                self.add_node(nrand,self.goal[0],self.goal[1])
                self.goalstate=nrand
                self.goalFlag=True
            else:
                self.add_node(nrand,x,y)
                                        
            
            
            
            
    def isFree(self): #To check if the node is located in free space
        n=self.number_of_nodes()-1#Node number starts from 0
        (x,y)=(self.x[n],self.y[n])
        obs=self.obstacles.copy()
        while len(obs)>0:
            rectang=obs.pop(0)
            if rectang.collidepoint(x,y):#Inbuilt function in pygame for calculating whether collision/overlap occurs
                self.remove_node(n)
                return False
        return True
    
    def crossObstacle(self,x1,x2,y1,y2):#Edge goes through obstacle or not
        obs=self.obstacles.copy()
        while(len(obs)>0):
            rectang=obs.pop(0)
            for i in range(0,101):   #Using interpolation to create sub points and check for collision
                u=i/100
                x=x1*u+x2*(1-u)
                y=y1*u+y2*(1-u)
                if rectang.collidepoint(x,y):
                    return True
        return False
    
    def connect(self,n1,n2):   #This is a major method as it creates a connection between nodes.Uses to previous function to check if connection is feasible
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        if self.crossObstacle(x1,x2,y1,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2) #n1 parent and n2 child
            return True
        
    
    def path_to_goal(self):   #Create the path node array
        if self.goalFlag:
            self.path=[]
            self.path.append(self.goalstate)
            newpos=self.parent[self.goalstate]
            while(newpos!=0):
                self.path.append(newpos)
                newpos=self.parent[newpos]
            self.path.append(0)
        return self.goalFlag

    #Finding the path coordinates
    def getPathCoords(self):
        pathCoords=[]
        for node in self.path:
            x,y=(self.x[node],self.y[node])
            pathCoords.append((x,y))
        return pathCoords

    
     #Traversal controllers(90% bias and 10% expansion)               
    def bias(self,ngoal):
        n=self.number_of_nodes()
        self.add_node(n,ngoal[0],ngoal[1])
        nnear=self.nearest(n)
        self.step(nnear,n)
        self.connect(nnear,n)
        return self.x,self.y,self.parent

    def expand(self):
        n=self.number_of_nodes()
        x,y=self.sample_envir()
        self.add_node(n,x,y)
        if self.isFree():
            xnearest=self.nearest(n)
            self.step(xnearest,n)
            self.connect(xnearest,n)
        return self.x,self.y,self.parent
    
    
    
    
    
