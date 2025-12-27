import os

def maximiseJoltage(bankOfJoltages):

    maxTens = max(bankOfJoltages[:-1])
    startOfPotentialUnits = bankOfJoltages.index(maxTens) + 1
    maxUnit = max(bankOfJoltages[startOfPotentialUnits:])

    return 10*maxTens + maxUnit

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day3.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    banks = file.readlines()
joltages = [[int(joltage) for joltage in line.strip()] for line in banks]
maxJoltages = [maximiseJoltage(bank) for bank in joltages]

print("Part 1: ", sum(maxJoltages))
print("Part 2: ", "TBD")
