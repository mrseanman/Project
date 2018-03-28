'''
Object describes a random meteor entering the inner solar system
'''
from Body import Body
import numpy as np

class Meteor(Body):

    def __init__(self, meteorFilename):
        self.readMeteorInfo(meteorFilename)
        self.mass = np.random.normal(self.massMean, self.massDev)
        velocity = np.random.normal(self.velMean, self.velDev)
        #where on the outer perimeter of the inner solar system it enters
        posAngleOfEntry = 2.* np.pi * np.random.random()
        velAngleOfEntry = posAngleOfEntry + np.pi *(0.5+np.random.random())

        self.pos = self.entranceRad * np.array([np.sin(posAngleOfEntry), np.cos(posAngleOfEntry), 0.])
        self.vel = velocity * np.array([np.sin(velAngleOfEntry), np.cos(velAngleOfEntry), 0.])

        self.force = np.zeros(self.pos.size, dtype=float)
        self.acc = np.zeros(self.pos.size, dtype=float)
        self.pot = 0.
        self.prevAcc = self.acc



    def readMeteorInfo(self, filename):
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
                self.name = str(data)
            elif i == 1:
                self.entranceRad = float(data)
            elif i == 2:
                self.massMean = float(data)
            elif i == 3:
                self.massDev = float(data)
            elif i == 4:
                self.velMean = float(data)
            elif i == 5:
                self.velDev = float(data)
            elif i == 6:
                self.radius = float(data)
            elif i == 7:
                self.colour = str(data)

        filein.close()
