'''
class that initialises Bodies and Systems and calls System methods to do useful things
'''
from Body import Body
from Satelite import Satelite
from AnimatedSystem import AnimatedSystem
import numpy as np

class Experiment(object):

    def readInfo(self, filename):
        filein = open(filename, "r")
        lines = filein.readlines()
        #list of lines without the comment lines
        noCommentLines = []
        for i in lines:
            if i[0] != "#":
                noCommentLines.append(i)
        for i in range(len(noCommentLines)):
            #splits the line on ": " disregards the first bit
            tokens = noCommentLines[i].split(": ")
            #removes trailing \n and whitespace
            data = tokens[1].rstrip()
            if i == 0:
                self.delta_t = float(data)
            elif i == 1:
                self.timeInterval = float(data)
            elif i == 2:
                self.animationTimeStep = float(data)
            elif i == 3:
                self.animateEveryNth = int(data)
        self.numIter = int(round(self.timeInterval/self.delta_t))
        filein.close()


    def innerSystem(self, filename):
        self.readInfo(filename)

        sun = Body(True, 'experiments/innerSolarSystem/infoFiles/sun')
        mercury = Body(True, 'experiments/innerSolarSystem/infoFiles/mercury')
        venus = Body(True, 'experiments/innerSolarSystem/infoFiles/venus')
        earth = Body(True, 'experiments/innerSolarSystem/infoFiles/earth')
        mars = Body(True, 'experiments/innerSolarSystem/infoFiles/mars')

        innerBodies = [sun, mercury, venus, earth, mars]
        innerSystem = AnimatedSystem(innerBodies, self.delta_t)

        innerSystem.iterateTimeInterval(self.timeInterval)
        #prints the number of earth days in an average orbit
        print(0.000072722/innerSystem.averageAngVel(1))
        print(0.000072722/innerSystem.averageAngVel(2))
        print(0.000072722/innerSystem.averageAngVel(3))
        print(0.000072722/innerSystem.averageAngVel(4))
        #innerSystem.printInfoTimeInterval('experiments/innerSolarSystem/data/innerBodyData1.dat', 0, timeInterval, delta_t, [0,1,2,3,4], [0,1,6,7,8])
        #innerSystem.animateTimeInterval(0., timeInterval, timewarp, jumpFrames)

        innerSystem.animateEveryNth(self.animateEveryNth, self.animationTimeStep)

    def energyConservation(self, filename):
        self.readInfo(filename)

    def sateliteToJupiter(self, filename):
        self.readInfo(filename)

        sun = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/sun')
        mercury = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/mercury')
        venus = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/venus')
        earth = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/earth')
        mars = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/mars')
        jupiter = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/jupiter')
        satelite = Satelite('experiments/innerSolarSystem/infoFiles/bodyInfo/earth', 'experiments/innerSolarSystem/infoFiles/bodyInfo/jupiterSatelite')

        systemOfBodies = [sun, mercury, venus, earth, mars, jupiter, satelite]
        system = AnimatedSystem(systemOfBodies, self.delta_t)

        system.iterateTimeInterval(self.timeInterval)

        print(system.averageAngVel(5))
        system.animateEveryNth(0., self.timeInterval, self.animateEveryNth, self.animationTimeStep)


    def sateliteToMars(self, filename):
        self.readInfo(filename)

        sun = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/sun')
        mercury = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/mercury')
        venus = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/venus')
        earth = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/earth')
        mars = Body(True, 'experiments/innerSolarSystem/infoFiles/bodyInfo/mars')

        satelite = Satelite('experiments/innerSolarSystem/infoFiles/bodyInfo/earth', 'experiments/innerSolarSystem/infoFiles/bodyInfo/marsSatelite')

        innerBodies = [sun, mercury, venus, earth, mars, satelite]
        innerSystem = AnimatedSystem(innerBodies, self.delta_t)

        innerSystem.iterateTimeInterval(self.timeInterval)
        closestSatMarsDisp, closestAprproachTime = innerSystem.closestApproach([5,4])

        '''
        initSatState = innerSystem.pastSysStates[0][5]
        print("Initial speed: " + str(initSatState.initialSpeed))
        print("Theta: " + str(initSatState.theta))
        print("Phi: " + str(initSatState.phi))
        print("")
        '''
        innerSystem.printInfoTimeInterval('experiments/innerSolarSystem/outputData/sateliteInfo.dat', 0., self.timeInterval, 1000., [5], [0,6,7,8])

        print(closestSatMarsDisp)
        print(np.linalg.norm(closestSatMarsDisp))
        print(closestAprproachTime)
        print("")
        #innerSystem.printInfoTimeInterval('experiments/innerSolarSystem/data/sateliteInfo.dat', 0, self.timeInterval, self.delta_t, [3,5], [0,1,2])

        innerSystem.animateEveryNth(closestAprproachTime-self.timeInterval/60, closestAprproachTime+self.timeInterval/60, self.animateEveryNth, self.animationTimeStep)

    def simpleOrbit(self):
        delta_t = 0.001
        timeInterval = 5.
        timewarp = 1.
        fps = 50
        mars = Body(True, 'experiments/simpleOrbit/infoFiles/marsInfo')
        phobos = Body(True, 'experiments/simpleOrbit/infoFiles/phobosInfo')

        marsAndMoon = AnimatedSystem([mars, phobos], delta_t)

        marsAndMoon.iterateTimeInterval(timeInterval)
        marsAndMoon.printInfoTimeInterval('experiments/simpleOrbit/data/test1.dat', 0., timeInterval, 0.01, [1], [0,1,8])

        marsAndMoon.animateTimeInterval(0.,timeInterval,fps,timewarp)


    def threeBodies(self):
        delta_t = 0.01
        timeInterval = 5.0
        timewarp = 1.
        fps = 50
        bodyA = Body(True, 'experiments/3Bodies/infoFiles/bodyA')
        bodyB = Body(True, 'experiments/3Bodies/infoFiles/bodyB')
        bodyC = Body(True, 'experiments/3Bodies/infoFiles/bodyC')

        threeSystem = AnimatedSystem([bodyA,bodyB,bodyC], delta_t)

        threeSystem.iterateTimeInterval(timeInterval)
        #threeSystem.dataDump('experiments/3Bodies/data/3bodyDump.dat')
        #threeSystem.printInfoTimeInterval('experiments/3Bodies/data/3bodydata.dat', 0., timeInterval, 0.1, [0,1,2], [0,1,8])
        threeSystem.animateTimeInterval(0., timeInterval, fps, timewarp)
