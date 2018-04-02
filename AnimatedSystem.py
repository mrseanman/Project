'''
For animation of a system in the x-y plane
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from System import System
import numpy as np

class AnimatedSystem(System):

    #finds what the extrema of the animation axis should be given the systemOfBodies
    def axisExtrema(self):
        maxX = 'notSet'
        maxY = 'notSet'
        minX = 'notSet'
        minY = 'notSet'
        for i in self.iterationsToAnimate:
            for body in self.pastSysStates[i]:
                if body.pos[0]>maxX or maxX == 'notSet':
                    maxX = body.pos[0]
                if body.pos[1]>maxY or maxY == 'notSet':
                    maxY = body.pos[1]
                if body.pos[0]<minX or minX == 'notSet':
                    minX = body.pos[0]
                if body.pos[1]<minY or minY == 'notSet':
                    minY = body.pos[1]

        #makes a pretty gap at the edges
        margins = float(maxX+maxY-minX-minY)/20.
        minCoords = [minX - margins, minY - margins]
        maxCoords = [maxX + margins, maxY + margins]
        return minCoords, maxCoords

    #initialiser animator in animateCars
    def init(self):
        return self.patches

    #for animateCars. describes the ith frame
    def animate(self, frame):
        for bodyIndex in range(len(self.patches)):
            xpos = self.pastSysStates[frame][bodyIndex].pos[0]
            ypos = self.pastSysStates[frame][bodyIndex].pos[1]
            self.patches[bodyIndex].center = (xpos,ypos)
        return self.patches

    #animates all the past positions of the bodies in the system
    def animateSystem(self, iterationsToAnimate, animationTimeStep):
        self.iterationsToAnimate = iterationsToAnimate
        #create plot elements
        fig = plt.figure()
        ax = plt.axes()
        #makes a circle patch for every body in the system
        self.patches = []
        for body in self.pastSysStates[self.iterationsToAnimate[0]]:
            initialx = body.pos[0]
            initialy = body.pos[1]
            #checks if user set radius, otherwise sets radius as default 1
            if body.radius != None:
                radius = body.radius
            else:
                radius = 1.
            #checks if user set colour, otherwise sets colour as default red
            if body.colour != None:
                colour = body.colour
            else:
                colour = 'r'
            self.patches.append(plt.Circle((initialx, initialy), radius = radius , color = colour , animated = True))

        #adds them as patches properly
        for i in self.patches:
            ax.add_patch(i)

        #makes x and y scales interlocked. so things dont get squished
        ax.axis('scaled')
        minCoords, maxCoords = self.axisExtrema()
        ax.set_xlim(minCoords[0], maxCoords[0])
        ax.set_ylim(minCoords[1], maxCoords[1])
        anim = FuncAnimation(fig, self.animate, init_func = self.init, frames = iterationsToAnimate, repeat = True, interval = animationTimeStep, blit = True)
        plt.show()

    #animates all the pastSysStates but only displays every Nth iteration
    #useful for speeding up slow systems
    def animateEveryNth(self, startTime, endTime, everyNth, animationTimeStep):
        iterationsToAnimate = []
        startIteration = int(round(startTime//self.delta_t))
        totalToAnimate = int(round((endTime-startTime)//(everyNth*self.delta_t)))
        for i in range(totalToAnimate):
            iterationsToAnimate.append(startIteration + i*everyNth)

        self.animateSystem(iterationsToAnimate, animationTimeStep)
