import os

script_path = os.path.dirname(__file__)
rel_filepath = "../Input/day11.txt"
input_filepath = os.path.join(script_path, rel_filepath)

with open(input_filepath) as file:
    paths = file.readlines()
forwardPaths = {}
reversePaths = {}
for path in paths:
    node, links = path.strip().split(": ")
    forwardPaths[node] = links.split(" ")
    for link in forwardPaths[node]:
        if link in reversePaths:
            reversePaths[link].append(node)
        else:
            reversePaths[link] = [node]
numPaths = {node: [] for node in forwardPaths}
numPaths["out"] = [1]
lastUpdated = ["out"]
while lastUpdated:
    updated = []
    for node in lastUpdated:
        for link in reversePaths[node]:
            numPaths[link].append(sum(numPaths[node]))
            if len(numPaths[link]) == len(forwardPaths[link]):
                if link in reversePaths:
                    updated.append(link)
    lastUpdated = updated

print("Part 1: ", sum(numPaths["you"]))
print("Part 2: ", "TBD")
