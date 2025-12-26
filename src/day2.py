import os
import math

def getIdLength(idInt):

    log10 = math.log(idInt,10)
    length = math.floor(log10) + 1

    return length

def getHalf(idInt, length, half):

    if half == 0:

        if length % 2 == 0:
            halfMagnitude = length/2
            return int(idInt // 10**halfMagnitude)

    else:

        if length % 2 == 0:
            halfMagnitude = length/2
            return idInt % 10**halfMagnitude

class Range:

    def __init__(self,rangeAsStr):

        endpoints = rangeAsStr.split('-')

        self.__start = int(endpoints[0])
        self.__end = int(endpoints[1])

    def sumInvalidIds(self):

        lengthStartID = getIdLength(self.__start)
        lengthEndID = getIdLength(self.__end)

        firstHalfStartID = getHalf(self.__start, lengthStartID, 0)
        firstHalfEndID = getHalf(self.__end, lengthEndID, 0)

        secondHalfStartID = getHalf(self.__start, lengthStartID, 1)
        secondHalfEndID = getHalf(self.__end, lengthEndID, 1)

        invalidIdSum = 0
        
        if lengthStartID == lengthEndID:
            # Should be most common case
            # All odd Ids valid
            if lengthStartID % 2 == 0:

                for i in range(firstHalfStartID+1, firstHalfEndID):
                    invalidIdSum += i* 10**(lengthStartID/2) + i
                
                if firstHalfEndID > firstHalfStartID:
                    if secondHalfStartID <= firstHalfStartID:
                        invalidIdSum += firstHalfStartID* 10**(lengthStartID/2) + firstHalfStartID
                    if secondHalfEndID >= firstHalfEndID:
                        invalidIdSum += firstHalfEndID* 10**(lengthEndID/2) + firstHalfEndID

                if firstHalfStartID == firstHalfEndID:
                    if secondHalfStartID <= firstHalfEndID and secondHalfEndID >= firstHalfEndID:
                        invalidIdSum += firstHalfEndID* 10**(lengthEndID/2) + firstHalfEndID
        
        else:
            
            for length in range(lengthStartID+1, lengthEndID):
                if length % 2 == 0:
                    halfMagnitude = 10**(length/2)
                    for invalidHalf in range(halfMagnitude):
                        invalidIdSum += invalidHalf* halfMagnitude**2 + invalidHalf

            if lengthStartID % 2 == 0:
                
                halfMagnitude = lengthStartID/2

                if firstHalfStartID >= secondHalfStartID:
                    invalidIdSum += firstHalfStartID* 10**halfMagnitude + firstHalfStartID
                for i in range(firstHalfStartID+1,int(10**halfMagnitude)):
                    invalidIdSum += i* 10**halfMagnitude + i
        
            if lengthEndID % 2 == 0:
                
                halfMagnitude = lengthEndID/2

                if firstHalfEndID <= secondHalfEndID:
                    invalidIdSum += firstHalfEndID* 10**halfMagnitude + firstHalfEndID
                for i in range(int(10**halfMagnitude),firstHalfEndID):
                    invalidIdSum += i* 10**halfMagnitude + i

        return invalidIdSum

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day2.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    productRangesRaw = file.readline().split(',')
productRanges = [Range(rangeStr) for rangeStr in productRangesRaw]
invalidIdsSum = [productRange.sumInvalidIds() for productRange in productRanges]

print("Part 1: ", sum(invalidIdsSum))
print("Part 2: ", "TBD")
