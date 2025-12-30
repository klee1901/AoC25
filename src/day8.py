import os
from functools import reduce
import operator

def calcDist(loc, other):
    """
    Inputs
    ------
    loc : list[int]
        Coordinate
    ------
    other : list[int]
        Coordinate of same dimension as loc
    Output
    ------
    int
        Square of straight-line distance between the 2 input coordinates
    """
    squareDists = [(loc[i] - other[i])**2 for i in range(3)]
    sumSquareDists = reduce(operator.add, squareDists)

    return sumSquareDists

def getCircuits(connectionMatrix):
    """
    Input
    -----
    connectionMatrix : list[list[int]]
        Symmetrical adjacency matrix (elements are either 0 or 1)
    Output
    list[list[int]]
        Each member is a list of the indices of connected nodes
    """
    numCoords = len(connectionMatrix)
    circuits = []
    connected = []

    for i in range(numCoords):
        if i not in connected:
            circuit = [i] + [j for j in range(i+1, numCoords) if connectionMatrix[i][j] == 1]
            cirInd = 1
            while cirInd < len(circuit):
                j = circuit[cirInd]
                boxConns = [k for k in range(numCoords) if connectionMatrix[j][k] == 1]
                for boxConn in boxConns:
                    if boxConn not in circuit:
                        circuit.append(boxConn)
                cirInd += 1
            circuits.append(circuit)
            connected += circuit

    return circuits

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day8.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()
coords = [[int(num) for num in line.strip().split(',')] for line in lines]
# Get dist between all pairs of coords and arrange shortest first
pairDists = []
for i in range(len(coords)):
    for j in range(i+1, len(coords)):
        pairDists.append([i, j, calcDist(coords[i], coords[j])])
pairDists.sort(key = lambda x: x[2])

# Calculate adjacency matrix after perscribed number of (shortest) connections made
cables = 1000
adjacencyMatrix = [[0 for i in range(len(coords))] for j in range(len(coords))]
for pair in pairDists[:cables]:
    adjacencyMatrix[pair[0]][pair[1]] = 1
    adjacencyMatrix[pair[1]][pair[0]] = 1

curCurcuits = getCircuits(adjacencyMatrix)
circuitSizes = [len(circuit) for circuit in curCurcuits]
circuitSizes.sort(reverse=True)
sizeMult = reduce(operator.mul, circuitSizes[:3])

# Set the maximum number of cables that can be connected before all boxes are connected
multiGroupIndex = cables + len(curCurcuits) - 1
for pair in pairDists[cables:multiGroupIndex]:
    adjacencyMatrix[pair[0]][pair[1]] = 1
    adjacencyMatrix[pair[1]][pair[0]] = 1
# Calculate the minimum number of cables that are guaranteed to connect all boxes
singleGroupIndex = len(pairDists) - len(coords) + 1
# Perform binary search to identify the cross over point
while singleGroupIndex > multiGroupIndex+1:
    testIndex = int((multiGroupIndex+singleGroupIndex)/2)
    tempAdjacencyMatrix = [[val for val in row] for row in adjacencyMatrix]
    for pair in pairDists[multiGroupIndex:testIndex]:
        tempAdjacencyMatrix[pair[0]][pair[1]] = 1
        tempAdjacencyMatrix[pair[1]][pair[0]] = 1
    curCurcuits = getCircuits(tempAdjacencyMatrix)
    if len(curCurcuits) > 1:
        adjacencyMatrix = tempAdjacencyMatrix
        multiGroupIndex = testIndex
    else:
        singleGroupIndex = testIndex
xMult = coords[pairDists[multiGroupIndex][0]][0] * coords[pairDists[multiGroupIndex][1]][0]

print("Part 1: ", sizeMult)
print("Part 2: ", xMult)
