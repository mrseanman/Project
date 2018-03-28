'''
runs the required experiment
'''
from Experiment import Experiment

def main():
    experimenter=Experiment()
    #experimenter.testInfoWrite()
    #experimenter.simpleOrbit()
    #experimenter.threeBodies()
    #experimenter.testWrite()
    #experimenter.testRead()
    #experimenter.innerSystem('experiments/innerSolarSystem/infoFiles/experimentInfo/calcYearLen')
    #experimenter.sateliteToMars('experiments/innerSolarSystem/infoFiles/experimentInfo/marsSatelite')
    #experimenter.sateliteToJupiter('experiments/innerSolarSystem/infoFiles/experimentInfo/jupiterSatelite')
    #experimenter.meteorRisk('experiments/innerSolarSystem/infoFiles/experimentInfo/meteorRisk')
    experimenter.energyConservationSolarSystem('experiments/innerSolarSystem/infoFiles/experimentInfo/energyConservation')
main()
