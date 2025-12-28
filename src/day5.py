import os

class freshRanges:

    def __init__(self, rangeList):
        self.__rangeList = rangeList

    def contains(self, potentialID):
    
        for IDRange in self.__rangeList:
            if IDRange[0] <= potentialID and potentialID <= IDRange[1]:
                return True
        return False

    def compressRanges(self):

        self.__rangeList.sort(key=lambda x: (x[0], x[1]))
        i = 0
        while i+2 <= len(self.__rangeList):
            if self.__rangeList[i][1] >= self.__rangeList[i+1][0]:
                if self.__rangeList[i][1] < self.__rangeList[i+1][1]:
                    self.__rangeList[i][1] = self.__rangeList[i+1][1]
                del self.__rangeList[i+1]
            else:
                i += 1

    def countAvailableIDs(self):
        rangeWidths = [IDRange[1] - IDRange[0] + 1 for IDRange in self.__rangeList]
        return sum(rangeWidths)

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day5.txt"
input_filepath = os.path.join(script_path, rel_filepath)

freshRangesList = []
with open(input_filepath) as file:
    line = file.readline().strip()
    while line != '':
        range = [int(endpt) for endpt in line.split('-')]
        freshRangesList.append(range)
        line = file.readline().strip()
    availableIDs = [int(line.strip()) for line in file.readlines()]
freshRangesObj = freshRanges(freshRangesList)
freshIDCount = sum([freshRangesObj.contains(availableID) for availableID in availableIDs])

freshRangesObj.compressRanges()

print("Part 1: ", freshIDCount)
print("Part 2: ", freshRangesObj.countAvailableIDs())
