'''
Object describes a celestial body that interacts with other bodies
by gravity
'''
import numpy as np

class Body(object):
    def __init__(self, readFromFile, filename):
        if readFromFile:
            self.readInfo(filename)

            #CurrForce gets added later
            #Dimention of Force vector is same as dimention of
            #position vector, same with acceleration and potential
            self.force = np.zeros(self.pos.size, dtype=float)
            self.acc = np.zeros(self.pos.size, dtype=float)
            self.pot = 0.

        self.prevAcc = self.acc


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
                self.name = str(data)
            elif i == 1:
                self.mass = float(data)
            elif i == 2:
                self.pos = np.fromstring(data, dtype=float, sep=',')
            elif i == 3:
                self.vel = np.fromstring(data, dtype=float, sep=',')
            elif i == 4:
                self.radius = float(data)
            elif i == 5:
                self.colour = str(data)

        filein.close()
