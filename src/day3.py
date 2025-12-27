import os

def maximiseJoltage(bankOfJoltages, batteriesToSwitchOn):
    """
    Input
    -----
    bankOfJoltages : list
        integer values
    batteriesToSwitchOn : int
        Number (<= length bankOfJoltages) of joltages that can be selected
    Output
    ------
    int
        Maximum output joltage than can be acheived by selecting batteriesToSwitchOn joltages
    """
    if batteriesToSwitchOn == 1:
        return max(bankOfJoltages)
    # Maximum joltage that can be added by turning on a single battery
    maxJoltage = max(bankOfJoltages[:1-batteriesToSwitchOn])
    startOfRemaining = bankOfJoltages.index(maxJoltage) + 1
    maxAdditionalJoltage = maximiseJoltage(bankOfJoltages[startOfRemaining:], batteriesToSwitchOn-1)

    return maxJoltage* 10**(batteriesToSwitchOn-1) + maxAdditionalJoltage

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day3.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    banks = file.readlines()
joltages = [[int(joltage) for joltage in line.strip()] for line in banks]
maxJoltages2Batteries = [maximiseJoltage(bank,2) for bank in joltages]
maxJoltages12Batteries = [maximiseJoltage(bank,12) for bank in joltages]

print("Part 1: ", sum(maxJoltages2Batteries))
print("Part 2: ", sum(maxJoltages12Batteries))
