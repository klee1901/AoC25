import os
from functools import reduce
import operator

def getPerimeter(points):
    """
    Input
    -----
    points : list[list[int]]
        Vertices of the perimeter
    Outputs
    -------
    rows : dict{int : list[int]}
        Column coords (values) of perimeter vetices for each row (key)
    columns : dict{int : list[int]}
        Row coords (values) of perimeter vetices for each column (key)
    """
    points.sort()
    columns = {}
    for point in points:
        if point[0] in columns:
            columns[point[0]].append(point[1])
        else:
            columns[point[0]] = [point[1]]
    points.sort(key = lambda x: (x[1], x[0]))
    rows = {}
    for point in points:
        if point[1] in rows:
            rows[point[1]].append(point[0])
        else:
            rows[point[1]] = [point[0]]
    return (rows, columns)

def getFirstLastPerimeter(perimLines, last = False):
    """
    Inputs
    ------
    perimLines : dict{int : list[int]}
        Coords of each perimeter vetex for each row or column
    last : boolean
        Get maximum perimeter location for each row or column (min otherwise)
    Output
    ------
    dict{int : list[int]}
        Coords of first/last perimeter for each column or row
    """
    linesWithPerim = [key for key in perimLines]
    linesWithPerim.sort(reverse = last)
    firstBorder = {}
    for lineInd in linesWithPerim:
        borders = perimLines[lineInd]
        for i in range(0,len(borders),2):
            for j in range(borders[i],borders[i+1]+1):
                if j not in firstBorder:
                    firstBorder[j] = lineInd
    return firstBorder

def getBorders(perimRows, perimColumns):
    """
    Inputs
    ------
    perimRows : dict{int : list[int]}
        Column coords (values) of perimeter vetices for each row (key)
    perimColumns : dict{int : list[int]}
        Row coords (values) of perimeter vetices for each column (key)
    Output
    ------
    list[dict{int : list[int]}]
        First dict contains first and last perimeter line for each row (key), second for each col (key)
    """
    topPerimeter = getFirstLastPerimeter(perimRows)
    leftPerimeter = getFirstLastPerimeter(perimColumns)
    rightPerimeter = getFirstLastPerimeter(perimColumns, True)
    bottomPerimeter = getFirstLastPerimeter(perimRows, True)
    verticalBorders = {row: [topPerimeter[row], bottomPerimeter[row]] for row in topPerimeter}
    horizontalBorders = {col: [leftPerimeter[col], rightPerimeter[col]] for col in leftPerimeter}
    return [verticalBorders, horizontalBorders]

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

def isValid(corner1, corner2, startEndPoints):
    """
    Inputs
    ------
    corner1 : list[int]
        Coords of one corner of rectangle
    corner2 : list[int]
        Coords of opposite corner of rectangle
    startEndPoints : list[dict{int : list[int]}]
        First and last perimeter lines for each row (index 0) and column (index 1)
    Output
    ------
    bool
        Are any first/last perimeter lines beyond the rectangle?
    """
    xLimits = [corner1[0], corner2[0]]
    yLimits = [corner1[1], corner2[1]]
    xLimits.sort()
    yLimits.sort()
    # Check most likely edge case (floating corners) first
    if yLimits[xLimits.index(corner1[0])] == corner1[1]:
        if (yLimits[0] < startEndPoints[0][xLimits[1]][0] or
            yLimits[1] > startEndPoints[0][xLimits[0]][1] or
            xLimits[0] < startEndPoints[1][yLimits[1]][0] or
            xLimits[1] > startEndPoints[1][yLimits[0]][1]
            ):
            return False
    elif (yLimits[0] < startEndPoints[0][xLimits[0]][0] or
            yLimits[1] > startEndPoints[0][xLimits[1]][1] or
            xLimits[0] < startEndPoints[1][yLimits[0]][0] or
            xLimits[1] > startEndPoints[1][yLimits[1]][1]
            ):
            return False
    for i in range(xLimits[0]+1, xLimits[1]):
        if yLimits[0] < startEndPoints[0][i][0] or yLimits[1] > startEndPoints[0][i][1]:
            return False
    for j in range(yLimits[0]+1, yLimits[1]):
        if xLimits[0] < startEndPoints[1][j][0] or xLimits[1] > startEndPoints[1][j][1]:
            return False
    return True

def getLargestRect(loc, otherLocs, startEndPoints=[]):
    """
    Inputs
    ------
    loc : list[int]
        Point to treat as fixed corner of potential rectangles
    otherLocs : list[list[int]]
        Points to consider as opposite corner of potential rectangle
    startEndPoints : list[dict{int : list[int]}]
        Perimeter outline to check validity of potential rectangles (no checks will be applied if empty)
    Output
    ------
    int
        Area of largest rectangle that can be drawn between loc and one element of otherLocs
    """
    areas = [[other, getArea(loc, other)] for other in otherLocs]
    areas.sort(key = lambda x: x[1], reverse=True)

    if startEndPoints:
        for rect in areas:
            if isValid(loc, rect[0], startEndPoints):
                return rect[1]
        return 0

    return areas[0][1]

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day9.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()
coords = [[int(num) for num in line.strip().split(',')] for line in lines]

maxRectangles = [getLargestRect(coords[i], coords[(i+1):]) for i in range(len(coords)-1)]
perimeterRows, perimeterColumns = getPerimeter(coords)
borders = getBorders(perimeterRows,perimeterColumns)
maxRectanglesConstrained = [getLargestRect(coords[i], coords[(i+1):], borders)
                            for i in range(len(coords)-1)]

print("Part 1: ", max(maxRectangles))
print("Part 2: ", max(maxRectanglesConstrained))
