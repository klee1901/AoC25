import os

def getNeighbours(rowN, colN, height, width):
    """
    Inputs
    ------
    rowN - integer
        row ind of current loc
    colN - integer
        col ind of current loc
    height - integer
        Num rows on grid
    width - integer
        Num cols on grid
    Output
    ------
    list of lists of integers
        [rowN, colN] coords of neighbours on grid (no wrapping)
    """
    neighbourCols = [colN]
    if colN > 0: neighbourCols.append(colN-1)
    if colN < width-1: neighbourCols.append(colN+1)
    neighbourRows = [rowN]
    if rowN > 0: neighbourRows.append(rowN-1)
    if rowN < height-1: neighbourRows.append(rowN+1)
    neighbours = [[j,i] for j in neighbourRows for i in neighbourCols if j != rowN or i != colN]

    return neighbours

def getLocationOfReams(grid):
    """
    Input
    -----
    grid : list
        list of strings of '.' or '@' characters
    Output
    ------
    list
        list of list of integers, coordinates (rowN, colN) of '@' chars
    """
    reamLocs =  []
    gridWidth = len(grid[0])
    for rowN in range(len(grid)):
        for reamInd in [i for i in range(gridWidth) if grid[rowN][i]=='@']:
            reamLocs.append([rowN, reamInd])

    return reamLocs

def getNAccessibleReams(reamLocs, grid):
    """
    Input
    -----
    reamLocs - list of list of ints
        coords of '@' characters in grid
    grid - list of strings (containing '@' or '.' characters)
        grid to search surroundings of '@' characters
    Output
    ------
    integer
        number of '@' characters surrounded by 4 or less '@' characters
    """
    height = len(grid)
    width = len(grid[0])
    nAccessibleReams = 0
    for reamLoc in reamLocs:
        neighbourLocs = getNeighbours(reamLoc[0], reamLoc[1], height, width)
        neighbours = [grid[neigh[0]][neigh[1]] for neigh in neighbourLocs]
        if neighbours.count('@') < 4:
            nAccessibleReams += 1

    return nAccessibleReams

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day4.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    rows = file.readlines()
rows = [row.strip() for row in rows]
paperLocs = getLocationOfReams(rows)

print("Part 1: ", getNAccessibleReams(paperLocs, rows))
print("Part 2: ", "TBD")
