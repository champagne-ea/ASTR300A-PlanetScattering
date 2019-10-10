import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
import random

class c: # C for constants
    #---- Units and constants ----#
    G = 6.67259e-11 #N m^2/kg^2
    mSun = 1.989e30 #kg
    mEarth = 5.972e24 #kg
    mJup = 1.898e27 #kg
    AU = 1.496e11 #m

class system:
    disco = False
    time = 0
    timeArray = []
    dt = 10000 # should this be global??
    planets = []
    barycenter = [0,0]
    baryUpToDate = False
    currentFarthestDist = 0    
    animation = plt.figure(constrained_layout = True)
    gs = animation.add_gridspec(2,3)
    paraPlot = animation.add_subplot(gs[0:2,0:2])
    xPlot = animation.add_subplot(gs[0,2])
    yPlot = animation.add_subplot(gs[1,2])
    
    allowedColors = ['b','g','r','c','m','y','k']
    @staticmethod
    def resetSystem():
        system.planets = []
        t = 0
    @staticmethod
    def drawAll():
        system.scatterX = []
        system.scatterY = []
        for i in system.planets:
            i.draw()
    @staticmethod
    def positAll():
        for i in system.planets:
            i.posit()
    @staticmethod
    def velocAll():
        for i in system.planets:
            i.veloc()
    @staticmethod
    def accelAll():
        for i in system.planets:
            i.accel()
    @staticmethod
    def updateAll():
        system.findBarycenter()
        for i in system.planets:
            i.update()
    @staticmethod
    def stepAll():
        system.accelAll()
        system.velocAll()
        system.positAll()
        system.updateAll()
        system.drawAll()
        system.time += system.dt  #beginning or end?
    @staticmethod
    def findBarycenter():
        mass, xCM, yCM = 0, 0, 0
        for i in system.planets:
            mass += i.mass
            xCM += i.mass * i.pos[0]
            yCM += i.mass * i.pos[1]
        xCM = xCM / mass
        yCM = yCM / mass
        system.barycenter = [xCM, yCM]
        system.baryUpToDate = True
    @staticmethod
    def distToPlanet(planet):
        delX = planet.pos[0] - system.barycenter[0]
        delY = planet.pos[1] - system.barycenter[1]
        dist = math.sqrt(delX*delX+delY*delY)
        return dist

class planet:
    #Technically this could also be a star...
    def __init__ (self, mass, pos, vel, color = None, name="Not named"):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.acc = [0,0] #2D or 3D?
        self.name = name
        self.point = plt.scatter([0],[0])
        if(system.disco):
            self.colorChar = None
        elif(color in system.allowedColors):
            self.colorChar = color
        else:
            randint = random.randint(0,7)
            self.colorChar = system.allowedColors[randint]
        #I think I need to change this to line objects??
        #self.radius, = [system.time,system.distToPlanet(self)] #Issues - I don't know line object syntax. Also, I can't add this
        #here in case other objects are added afterwards - need to check barycenter immediately before updating speed and radius
        #Can possibly add a system flag for motion that any posit flips
        #self.speed, = []
        system.planets.append(self)
        
        #if(system.time != 0): #in case we include the test mass feature
        #    n = system.time / system.dt
        #    for i in range n:
        #        self.radius.append(0)
        #        self.speed.append(0)
            
    def accel (self):
        aX = 0
        aY = 0
        for i in system.planets:
            if(i != self and i.mass != 0):
                #(i.mass != 0) rules out test particles. The if statement would work fine for massless objects,
                #(no division by 0), but why waste the time?
                delX = i.pos[0]-self.pos[0]
                delY = i.pos[1]-self.pos[1]
                dist = math.sqrt(delX*delX+delY*delY)
                a = c.G * i.mass / (dist * dist * dist)
                aX += a * delX
                aY += a * delY
        print("Acceleration for " + self.name + ": " + str([aX,aY]))
        self.acc = [aX,aY]
    def veloc (self):
        for i in range(2):
            self.vel[i] += self.acc[i]*system.dt
    def posit (self):
        system.baryUpToDate = False
        for i in range(2):
            self.pos[i] += self.vel[i]*system.dt
    def draw (self):
        self.point.remove()
        #system.scatterX.append(self.pos[0])
        #system.scatterY.append(self.pos[1])
        self.point = system.paraPlot.scatter([self.pos[0]],[self.pos[1]],10, self.colorChar)        
    def update (self):
        if(system.baryUpToDate == False):
            system.findBarycenter()
        currentRad = system.distToPlanet(self)
        currentSpeed = math.sqrt(self.vel[0]*self.vel[0]+self.vel[1]*self.vel[1])
        #add speed and pos to line graphs
        print("Update")
    @staticmethod
    def distBetween(p1,p2):
        dist = math.sqrt((p1.pos[0]-p2.pos[0])*(p1.pos[0]-p2.pos[0])+(p1.pos[1]-p2.pos[1])*(p1.pos[1]-p2.pos[1]))
        return dist
