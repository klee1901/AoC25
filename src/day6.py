import os
import re
from functools import reduce
import operator

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day6.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()
numbers = [[int(num) for num in re.findall("\\d+", line)] for line in lines[:-1]]
operators = re.findall("\\*|\\+", lines[-1])
solutionSum = 0
for i in range(len(operators)):
    if operators[i] == '+':
        individualResult = reduce(operator.add, [numberSet[i] for numberSet in numbers])
    else:
        individualResult = reduce(operator.mul, [numberSet[i] for numberSet in numbers])
    solutionSum += individualResult

print("Part 1: ", solutionSum)
print("Part 2: ", "TBD")
