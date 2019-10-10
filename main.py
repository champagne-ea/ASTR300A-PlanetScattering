import math
from classes import *
from matplotlib import animation

def init():
    system.resetSystem()
    sun = planet(1*c.mSun,[0,0],[0,0], 'ciao', "Sun")
    earth = planet(1*c.mEarth,[c.AU,0],[0,0], 'b', "Earth")
    earth2 = planet(1*c.mEarth,[-c.AU,0],[0,0], 'g', "Earth2")
    system.stepAll()
    print("init")

def animate(i):
    #print(system.scatterX)
    system.stepAll()
    #return scatterPlot

#system.resetSystem()

#jup.accel()
#jup.veloc()
#jup.posit()
#system.findBarycenter()
#system.updateAll()
#system.drawAll()

#ax = plt.axes(xlim=(0,2), ylim=(-2,2))
#plot1 = plt.scatter(system.scatterX, system.scatterY)

anim = animation.FuncAnimation(system.animation, animate, init_func = init, interval = 33)
#init_func = init,

#I think either my acceleration or my velocity has a sign error

# I think I can remove system.scatterX and system.scatterY

system.animation.show()

