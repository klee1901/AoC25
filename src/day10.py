import os
import re
import numpy as np
from scipy.optimize import linprog

def processButtons(buttonList):
    """
    Input
    -----
    buttonList : list[str]
        List of lights switched on/off by each button
    Output
    ------
    list[list[str]]
        Indices of lights / joltages affected by each button
    """
    return [re.findall("\\d+", button) for button in buttonList]

def processJoltages(joltages):
    """
    Input
    -----
    joltages : str
        Target joltages in form {x,y}
    Output
    ------
    list[int]
        Target joltages, e.g. [x,y]
    """
    return [int(joltage) for joltage in re.findall("\\d+", joltages)]

def minButtonPresses(lightsToFlip, buttonsAvailable):
    """
    Inputs
    ------
    lightsToFlip : list[int]
        Indices of lights that need switching on or off to reach target arangement
    buttonsAvailable : list[list[str]]
        Each element contains indices of lights affected by an individual button
    Output
    ------
    int
        Number of button presses required to reach target state (flip all lights in argument)
    """
    if not lightsToFlip:
        return 0
    if not buttonsAvailable:
        return None
    # Determine how many buttons (key) would affect each target light
    buttonOptions = {}
    for light in lightsToFlip:
        possButtons = sum([light in button for button in buttonsAvailable])
        if possButtons in buttonOptions:
            buttonOptions[possButtons].append(light)
        else:
            buttonOptions[possButtons] = [light]
    if 0 in buttonOptions:
        return None
    if 1 in buttonOptions:
        lightTarget = buttonOptions[1][0]
    else:
        buttonOption = min([val for val in buttonOptions])
        lightTarget = buttonOptions[buttonOption][0]
    buttonChoices = [i for i in range(len(buttonsAvailable)) if lightTarget in buttonsAvailable[i]]
    nextMin = []
    # Step through permutations if multiple buttons affect target light
    for buttonInd in buttonChoices:
        lightsFlipped = buttonsAvailable[buttonInd]
        lightsToFlipNext = ([light for light in lightsToFlip if light not in lightsFlipped] +
                            [light for light in lightsFlipped if light not in lightsToFlip])
        buttonsAvailableNext = buttonsAvailable[:buttonInd] + buttonsAvailable[(buttonInd+1):]
        nextMin.append(minButtonPresses(lightsToFlipNext, buttonsAvailableNext))
    nextMin = [minPressN for minPressN in nextMin if type(minPressN) is int]
    if nextMin:
        return min(nextMin) + 1
    return None

def minPressesForJoltages(joltagesToAchieve, buttonsAvailable):
    """
    Inputs
    ------
    joltagesToAchieve : np.array(int)
        Target joltages to hit
    buttonsAvailable : np.array(np.array(int))
        Binary matrix where each row represents a button and each element is the increase (1 or 0) that
        button makes to the joltage sharing that column index
    Output
    ------
    int
        Minimum number of button presses required to hit joltage target
    """
    optimalSolution = linprog(np.ones(len(buttonsAvailable)), A_eq=buttonsAvailable.transpose(),
                                b_eq=joltagesToAchieve, integrality=1)
    return sum(optimalSolution['x'])

class Machine:

    def __init__(self, inputConditions):
        """
        Input
        -----
        inputConditions : str
            Light and joltage targets seperated by button mappings in perscribed format
        """
        inputConditions = inputConditions.split(' ')
        indicatorLightDiagram = inputConditions[0]
        self.__lightsToSwitchOn = [str(i) for i, x in enumerate(indicatorLightDiagram[1:-1]) if x == '#']
        self.__buttons = processButtons(inputConditions[1:-1])
        self.__joltages = processJoltages(inputConditions[-1])
    
    def minButtonPresses(self, switchedOn=False):
        """
        Input
        -----
        switchedOn : bool
            Has machine been actived? Is target joltages (instead of light sequence)?
        Output
        ------
        int
            Minimum number of button presses required to change machine state to target state
        """
        if switchedOn:
            joltageArray = np.array(self.__joltages)
            numJoltages = len(joltageArray)
            buttonMat = np.array([[1 if str(j) in button else 0 for j in range(numJoltages)]
                                    for button in self.__buttons])
            return minPressesForJoltages(joltageArray, buttonMat)
        else:
            return minButtonPresses(self.__lightsToSwitchOn, self.__buttons)

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day10.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()
machines = [Machine(line.strip()) for line in lines]
buttonPresses = [machine.minButtonPresses() for machine in machines]
buttonPressesAfterSwitchOn = [machine.minButtonPresses(True) for machine in machines]

print("Part 1: ", sum(buttonPresses))
print("Part 2: ", sum(buttonPressesAfterSwitchOn))
