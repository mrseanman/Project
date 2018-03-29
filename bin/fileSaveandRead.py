'''
for writing and reading all of pastSysStates to a file
Turns out this is slower than simulating the system, but felt like a shame
to delete it all
'''

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
