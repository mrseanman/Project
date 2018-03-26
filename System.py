'''
looks after a system of Bodies by calculating
the total force on each body and then using that info
to update each bodies position and Velocity using the
Beeman integration schemeself.
Any useful past info on a Body in the simulation is 
accessed through methods here.
'''
from Calculate import Calculate as calc
from Body import Body
from itertools import combinations
import numpy as np
import copy
import sys

class System(object):

    def __init__(self, systemOfBodies, delta_t):
        self.delta_t = delta_t
        #a list of body objects in the system
        self.currSysState = systemOfBodies
        self.calcAllForces()
        #initialising acc
        #to start, prevAcc = acc
        for body in self.currSysState:
            body.acc = body.force/body.mass
            body.prevAcc = copy.copy(body.acc)

        #initialise pastSysStates and pastTimes
        self.pastSysStates = [copy.deepcopy(self.currSysState)]
        #a list of times corresponding to each pastSysState
        self.pastTimes = [0.]

    #evaluates the force and potential due to gravity on every body in the
    #systemOfBodies. All at their most current position
    def calcAllForces(self):
        #each time force and potential need to be zeroed
        #because force and potential do not add over time
        for body in self.currSysState:
            body.force = 0.
            body.pot = 0.
        #this creates a list of distinct pairs of Bodies without any repeats
        #or pairs where both elements are same
        #since gravity is same for (1,2) and (2,1) but reversed
        #and gravity of (1,1) is zero
        pairsOfBodies = combinations(self.currSysState, 2)

        for pair in pairsOfBodies:
            #gravity acting on pair[1] due to pair[0]
            gravityActingOn2 = calc.gravityForce(pair[0].mass, pair[1].mass, pair[0].pos, pair[1].pos)
            #adds the force to the total force vector for each Body
            pair[1].force += gravityActingOn2
            pair[0].force += -gravityActingOn2

            #adds the potential due to this pair to its respecive Bodies
            potential = calc.gravityPotential(pair[0].mass, pair[1].mass, pair[0].pos, pair[1].pos)
            pair[0].pot += potential
            pair[1].pot += potential

    #implementation of Beeman integration using the methods in Calculate
    def updateSystemFull(self):
        for body in self.currSysState:
            body.pos = calc.nextPos(body.pos, body.vel, body.acc, body.prevAcc, self.delta_t)

        self.calcAllForces()
        for body in self.currSysState:
            nextAcc = body.force/body.mass
            body.vel = calc.nextVel(body.vel, body.prevAcc, body.acc, nextAcc, self.delta_t)
            body.prevAcc = copy.copy(body.acc)
            body.acc = nextAcc

        self.pastSysStates.append(copy.deepcopy(self.currSysState))
        self.pastTimes.append(self.pastTimes[-1]+self.delta_t)

    #runs updateSystemFull numIter times with a progress report
    def iterateSystemMany(self, numIter):
        print("Simulating:")
        for i in range(numIter):
            #shows a little progress indicator
            sys.stdout.write("\r" + str(100*i/numIter)[0:3] + "%")
            self.updateSystemFull()
            sys.stdout.flush()

        print("\n")

    def iterateTimeInterval(self, timeInterval):
        numIter = int(round((float(timeInterval)/self.delta_t)))
        self.iterateSystemMany(numIter)

    #returns the average angular velocity of a body about the origin
    def averageAngVel(self, bodyNum):
        runningSum = 0.
        for state in self.pastSysStates:
            vel = state[bodyNum].vel
            pos = state[bodyNum].pos
            angVel = np.linalg.norm(np.cross(pos,vel)) / (np.linalg.norm(pos)**2)
            runningSum += angVel

        return runningSum/len(self.pastSysStates)

    #finds the minimum displacement of bodiesOfInterest[0] from bodiesOfInterest[1]
    #returns that minimum vector and the time at which that ocurred
    def closestApproach(self, bodiesOfInterest):
        bodyIndex1 = bodiesOfInterest[0]
        bodyIndex2 = bodiesOfInterest[1]
        minDistance = np.linalg.norm(self.pastSysStates[0][bodyIndex2].pos-self.pastSysStates[0][bodyIndex1].pos)
        minDisplacement = self.pastSysStates[0][bodyIndex2].pos-self.pastSysStates[0][bodyIndex1].pos
        closestAprproachTime = 0.
        for i in range(len(self.pastSysStates)):
            currDisplacement = self.pastSysStates[i][bodyIndex2].pos - self.pastSysStates[i][bodyIndex1].pos
            currDistance = np.linalg.norm(currDisplacement)

            if currDistance < minDistance:
                minDistance = currDistance
                minDisplacement = currDisplacement
                closestAprproachTime = self.pastTimes[i]

        return minDisplacement, closestAprproachTime

    #pretty prints past parameters of the system in system.pastSysStates[iterationsOfInterest[i]]
    #bodiesOfInterest is what bodies we want to get info on
    #parametersOfInterest is what parameters we want to get info on
    def printInfoToFile(self, filename, iterationsOfInterest, bodiesOfInterest, parametersOfInterest):
        fileout = open(filename, 'w')
        #for the progress report
        print("Pretty Write:")
        progress = 0.
        numOfIterations = len(iterationsOfInterest)
        for i in iterationsOfInterest:
            sys.stdout.write("\r" + str(100*progress/numOfIterations)[0:3] + "%")
            fileout.write("======================\n")
            #always prints time
            fileout.write("Time: " + str(self.pastTimes[i]) + " \n----")
            for j in range(len(self.pastSysStates[i])):
                if j in bodiesOfInterest:
                    fileout.write("\n")
                    #name
                    if 0 in parametersOfInterest:
                        fileout.write(str(self.pastSysStates[i][j].name + ":\n"))

                    #position
                    if 1 in parametersOfInterest:
                        fileout.write("Position: " + str(self.pastSysStates[i][j].pos) + "\n")

                    #velocity
                    if 2 in parametersOfInterest:
                        fileout.write("Velocity: " + str(self.pastSysStates[i][j].vel) + "\n")

                    #acceleration
                    if 3 in parametersOfInterest:
                        fileout.write("Acceleration: " + str(self.pastSysStates[i][j].acc) + "\n")

                    #momentum
                    if 4 in parametersOfInterest:
                        fileout.write("Momentum: " + str(self.pastSysStates[i][j].vel * self.pastSysStates[i][j].mass) + "\n")

                    #force
                    if 5 in parametersOfInterest:
                        fileout.write("Force: " + str(self.pastSysStates[i][j].acc*self.pastSysStates[i][j].mass) + "\n")

                    #kinetic energy
                    if 6 in parametersOfInterest:
                        velocityMag = np.linalg.norm(self.pastSysStates[i][j].vel)
                        ke = 0.5 * self.pastSysStates[i][j].mass * velocityMag**2
                        fileout.write("Kinetic Energy: " + str(ke) + "\n")

                    #grav. pot. energy
                    if 7 in parametersOfInterest:
                        fileout.write("Potential Energy: " + str(self.pastSysStates[i][j].pot) + "\n")

                    #total energy
                    if 8 in parametersOfInterest:
                        velocityMag = np.linalg.norm(self.pastSysStates[i][j].vel)
                        ke = 0.5 * self.pastSysStates[i][j].mass * velocityMag**2
                        pe = self.pastSysStates[i][j].pot
                        fileout.write("Total Energy: " + str(ke + pe) + "\n")

                    #mass
                    if 9 in parametersOfInterest:
                        fileout.write("Mass: " + str(self.pastSysStates[i][j].mass) + "\n")

            sys.stdout.flush()
            progress += 1
        print("\n")
        fileout.close()

    #uses printInfoToFile to give info from startTime to endTime every timeStep
    #again, if timeStep is poorly chosen r.e delta_t then rounding occurs
    #because info does not exist at those times
    def printInfoTimeInterval(self, filename, startTime, endTime, timeStep, bodiesOfInterest, parametersOfInterest):
        startIteration = round(startTime/self.delta_t)
        endIteration = round(endTime/self.delta_t)
        everyNthIteration = round(timeStep/self.delta_t)
        iterationsOfInterest = np.arange(startIteration, endIteration+1, everyNthIteration, dtype = int).tolist()
        self.printInfoToFile(filename, iterationsOfInterest, bodiesOfInterest, parametersOfInterest)

    #dumps all the data from self.pastSysStates to a file to be read in later
    def dataDump(self, filename):
        fileout = open(filename, 'w')
        fileout.write(str(self.delta_t)+ '\n')
        #for progress info
        print("Save to file:")
        numOfPastStates = len(self.pastSysStates)
        for state in range(numOfPastStates):
            sys.stdout.write("\r" + str(100*state/numOfPastStates)[0:3] + "%")
            stateString = '$$\n'
            stateString += str(self.pastTimes[state]) + '\n'
            for body in self.pastSysStates[state]:
                stateString += str(body.name) + ' , '
                stateString += str(body.mass) + ' , '
                stateString += ' '.join(np.array_str(body.pos).split()) + ' , '
                stateString += ' '.join(np.array_str(body.vel).split()) + ' , '
                stateString += ' '.join(np.array_str(body.force).split()) + ' , '
                stateString += ' '.join(np.array_str(body.acc).split()) + ' , '
                stateString += ' '.join(np.array_str(body.prevAcc).split()) + ' , '
                stateString += str(body.pot) + ' , '
                stateString += str(body.radius) + ' , '
                stateString += str(body.colour) + '\n'

            fileout.write(stateString + '\n')
            sys.stdout.flush()

        fileout.close()
        print("\n")

    #reads in from a file created by dataDump. All pastSysStates replaced by
    #those in the file.
    def readFromFile(self, filename):
        filein = open(filename, 'r')
        lines = filein.readlines()
        self.delta_t = lines[0]
        self.pastSysStates=[]
        self.pastTimes=[]
        print("Read from file:")
        numOfLines = len(lines)
        for lineNum in range(1,numOfLines):
            sys.stdout.write("\r" + str(100*(lineNum-1)/numOfLines)[0:3] + "%")
            if lines[lineNum] == '$$\n':
                self.pastTimes.append(float(lines[lineNum+1]))
                systemOfBodies = []
                bodyIndex = 2
                #wether there are any more bodies to read in for this past state
                noMoreBodies = False
                while not(noMoreBodies):
                    bodyData = lines[lineNum+bodyIndex].split(' , ')
                    body = Body(False, '')
                    body.name = str(bodyData[0])
                    body.mass = float(bodyData[1])
                    body.pos = np.asarray(bodyData[2][1:-1].split(), dtype = np.float64)
                    body.vel = np.asarray(bodyData[3][1:-1].split(), dtype = np.float64)
                    body.force = np.asarray(bodyData[4][1:-1].split(), dtype = np.float64)
                    body.acc = np.asarray(bodyData[5][1:-1].split(), dtype = np.float64)
                    body.prevAcc = np.asarray(bodyData[6][1:-1].split(), dtype = np.float64)
                    body.pot = float(bodyData[7])
                    body.radius = float(bodyData[8])
                    body.colour = str(bodyData[9])
                    systemOfBodies.append(copy.deepcopy(body))
                    bodyIndex += 1
                    if lines[lineNum+bodyIndex] == '\n':
                        noMoreBodies = True

                self.pastSysStates.append(copy.deepcopy(systemOfBodies))

            sys.stdout.flush()

        self.currSysState = self.pastSysStates[-1]
        print("\n")
