import os

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day7.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    lines = file.readlines()

beams = [lines[0].index('S')]
rowNum = 0
splits = 0
while rowNum < len(lines):
    nxtBeams = []
    for beam in beams:
        if lines[rowNum][beam] == '^':
            splits += 1
            if beam - 1 not in nxtBeams:
                nxtBeams.append(beam - 1)
            nxtBeams.append(beam + 1)
        else:
            if beam not in nxtBeams:
                nxtBeams.append(beam)
    rowNum += 1
    beams = nxtBeams

width = len(lines[1].strip())
timelines = [1]*width
for i in range(1, len(lines)):
    splitterInds = [j for j, x in enumerate(lines[len(lines)-i-1]) if x=='^']
    for j in splitterInds:
        timelines[j] = timelines[j-1]+timelines[j+1]


print("Part 1: ", splits)
print("Part 2: ", timelines[lines[0].index('S')])
