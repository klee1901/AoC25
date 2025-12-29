import os
import re
from functools import reduce
import operator

def getCheckSum(numberSets, operatorsList):
    """
    Inputs
    ------
    numberSets : list of list of ints
        Each element is a list of operands
    operatorsList : list of strs
        Same length as numberSets; Each element is either a plus or multiply operator
    Output
    int
        Sum of all operations
    """
    solutionSum = 0
    for i in range(len(operatorsList)):
        if operatorsList[i] == '+':
            individualResult = reduce(operator.add, numberSets[i])
        else:
            individualResult = reduce(operator.mul, numberSets[i])
        solutionSum += individualResult
    return solutionSum

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day6.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()
operators = re.findall("\\*|\\+", lines[-1])

numbersTable = [[int(num) for num in re.findall("\\d+", line)] for line in lines[:-1]]
tableRows = len(numbersTable)
# Rearrange numbers into sets of operands
numbers = [[numbersTable[i][j] for i in range(tableRows)] for j in range(len(numbersTable[0]))]
part1Check = getCheckSum(numbers, operators)

numberGrid = [[char for char in line.strip('\n')] for line in lines[:-1]]
# Compile digits accross rows
numbersStr = reduce(lambda x, y: [x[i] + y[i] for i in range(len(x))], numberGrid)
# Group operands into sets
numbers = [[]]
for numStr in numbersStr:
    if re.search('\\d',numStr) is None:
        numbers.append([])
    else:
        numbers[-1].append(int(numStr))
part2Check = getCheckSum(numbers, operators)

print("Part 1: ", part1Check)
print("Part 2: ", part2Check)
