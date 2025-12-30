import os
from functools import reduce
import operator

def getArea(loc, other):
    """
    Inputs
    ------
    loc : list[int]
        Point to treat as fixed corner of rectangle
    other : list[int]
        Point to consider as opposite corner of rectangle
    Output
    ------
    int
        Area of rectangle
    """
    sideLengths = [abs(loc[i]-other[i])+1 for i in range(len(loc))]
    area = reduce(operator.mul, sideLengths)
    return area

def getLargestRect(loc, otherLocs):
    """
    Inputs
    ------
    loc : list[int]
        Point to treat as fixed corner of potential rectangles
    otherLocs : list[list[int]]
        Points to consider as opposite corner of potential rectangle
    Output
    ------
    int
        Area of largest rectangle that can be drawn between loc and one element of otherLocs
    """
    areas = [getArea(loc, other) for other in otherLocs]
    return max(areas)

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day9.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()
coords = [[int(num) for num in line.strip().split(',')] for line in lines]

maxRectangles = [getLargestRect(coords[i], coords[(i+1):]) for i in range(len(coords)-1)]

print("Part 1: ", max(maxRectangles))
print("Part 2: ", "TBD")
