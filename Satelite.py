'''
simulates a satelite 'boosting' off from a near earth orbit at a certain
phi and theta angle
phi measured from z
theta measured from x
'''

from Body import Body
import numpy as np

class Satelite(Body):

    def __init__(self, earthFilename, sateliteFilename):
        earth = Body(True, earthFilename)
        self.readSateliteInfo(sateliteFilename)

        self.pos = earth.pos + self.distanceFromEarth * np.array([np.sin(self.phi)*np.cos(self.theta), np.sin(self.phi)*np.sin(self.theta), np.cos(self.phi)])
        self.vel = earth.vel + self.initialSpeed * np.array([np.sin(self.phi)*np.cos(self.theta), np.sin(self.phi)*np.sin(self.theta), np.cos(self.phi)])

        self.force = np.zeros(self.pos.size, dtype=float)
        self.acc = np.zeros(self.pos.size, dtype=float)
        self.pot = 0.
        self.prevAcc = self.acc

    def readSateliteInfo(self, filename):
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
                self.mass = float(data)
            elif i == 2:
                self.distanceFromEarth = float(data)
            elif i == 3:
                self.theta = float(data)
            elif i == 4:
                self.phi = float(data)
            elif i ==5:
                self.initialSpeed = float(data)
            elif i == 6:
                self.radius = float(data)
            elif i == 7:
                self.colour = str(data)

        filein.close()
