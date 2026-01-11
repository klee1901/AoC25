import os

def getPathsTo(targets, numPaths, lastUpdated):
    """
    Inputs
    ------
    targets : list[str]
        Nodes to stop when first has all paths from identified
    numPaths : dict{str: list[int]}
        Number of paths through each link from a given node (key)
    lastUpdated : list[str]
        Nodes for which number of paths have just been determined
    Outputs
    -------
    numPaths : dict{str: list[int]}
    lastUpdated : list[str]
    """
    while True not in [len(numPaths[target]) == len(forwardPaths[target]) for target in targets]:
        updated = []
        for node in lastUpdated:
            for link in reversePaths[node]:
                numPaths[link].append(sum(numPaths[node]))
                if len(numPaths[link]) == len(forwardPaths[link]):
                    if link in reversePaths:
                        updated.append(link)
        lastUpdated = updated
    return (numPaths, lastUpdated)

def blankPathCounts(pathCounts, nodeToNotBlank):
    """
    Inputs
    ------
    pathCounts : dict{str : list[int]}
        Number of paths through each link from a given node (key)
    nodeToNodeBlank : str
        Node for which to retain the path counts
    Output
    ------
    dict{str : list[int]}
        Number of paths possible that lead through nodeToNodeBlank. 0 indicates a possible path not
        leading through nodeToNodeBlank.
    """
    return {node: ([0 for _ in pathCounts[node]] if node != nodeToNotBlank else pathCounts[node]) for node in pathCounts}


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

startPaths = {node: [] for node in forwardPaths}
startPaths["out"] = [1]
prt1 = getPathsTo(["you"], startPaths, ["out"])

startPaths = {node: [] for node in forwardPaths}
startPaths["out"] = [1]
prt2a = getPathsTo(["dac", "fft"], startPaths, ["out"])
if "dac" in prt2a[1]:
    firstIntermediateHit = "dac"
    secondIntermediateToHit = "fft"
else:
    firstIntermediateHit = "fft"
    secondIntermediateToHit = "dac"
intermediatePaths = blankPathCounts(prt2a[0], firstIntermediateHit)
prt2b = getPathsTo([secondIntermediateToHit], intermediatePaths, prt2a[1])
intermediatePaths = blankPathCounts(prt2b[0], secondIntermediateToHit)
prt2c = getPathsTo(["svr"], intermediatePaths, prt2b[1])

print("Part 1: ", sum(prt1[0]["you"]))
print("Part 2: ", sum(prt2c[0]["svr"]))
