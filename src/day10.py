import os
import re

def processButtons(buttonList):
    return [re.findall("\\d+", button) for button in buttonList]

def minButtonPresses(lightsToFlip, buttonsAvailable):
    if not lightsToFlip:
        return 0
    if not buttonsAvailable:
        return None
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

class Machine:

    def __init__(self, inputConditions):
        inputConditions = inputConditions.split(' ')
        indicatorLightDiagram = inputConditions[0]
        self.__lightsToSwitchOn = [str(i) for i, x in enumerate(indicatorLightDiagram[1:-1]) if x == '#']
        self.__buttons = processButtons(inputConditions[1:-1])
        self.__joltages = inputConditions[-1]
    
    def minButtonPresses(self):
        return minButtonPresses(self.__lightsToSwitchOn, self.__buttons)

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day10.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()
machines = [Machine(line.strip()) for line in lines]
buttonPresses = [machine.minButtonPresses() for machine in machines]

print("Part 1: ", sum(buttonPresses))
print("Part 2: ", "TBD")
