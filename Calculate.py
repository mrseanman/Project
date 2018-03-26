'''
Where all the integration and calculation of forces and potentials goes on
Methods all working with numpy arrays
'''
import numpy as np

class Calculate(object):
    #grav. constant
    global G
    G = 6.67408E-11

    #returns force on mass2 due to mass1
    @staticmethod
    def gravityForce(mass1, mass2, position1, position2):


        relativePosition = position2 - position1
        #magnitude of relativePosition
        relativePositionMag = np.linalg.norm(relativePosition)
        force = (-G*mass1*mass2*relativePosition)/(relativePositionMag**3.)
        return force


    #returns the grav. potential of mass2 compared to mass1
    @staticmethod
    def gravityPotential(mass1, mass2, position1, position2):
        relativePosition = position2 - position1
        #magnitude of relativePosition
        relativePositionMag = np.linalg.norm(relativePosition)
        potential = -G*mass1*mass2/relativePositionMag
        return potential


    #uses beeman integration scheme
    @staticmethod
    def nextVel(currVel, prevAcc, currAcc, nextAcc, delta_t):
        return currVel + 1./6.*(2.*nextAcc+5.*currAcc-prevAcc)*delta_t
    @staticmethod
    def nextPos(currPos, currVel, currAcc, prevAcc, delta_t):
        return currPos + currVel*delta_t + 1./6.*(4.*currAcc-prevAcc)*delta_t**2.
