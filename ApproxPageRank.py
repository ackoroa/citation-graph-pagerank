import math.log as log
import random

def approxPageRank(nodeList, threshold):
    n = len(nodeList)
    
    chunks = {}
    h = log(n / (4.0 * threshold), 2)
    for t in range(0,h+1):
        epst = 2**-t
        S = 4 * n * epst * log(n,2)**2 / threshold
        for s in range(0:S):
            v = nodeList[random.randrange(n)]
            neighbourList = approxRow(v, epst/2.0, 0.5)
            for neighbour, eps in neighbourList.iteritems():
                if (neighbour, eps) in chunks:
                    chunks[(neighbour, eps)] = chunks[(neighbour, eps)] + 1
                else:
                    chunks[(neighbour, eps)] = 1
    
    pageRankValues = {}
    for (node, eps), val in chunks:
        if val >= log(n)/2.0:
            if not node in pageRankValues:
                pageRankValus[node] = 0
            pageRankValus[node] = pageRankValus[node] + threshold / (2 * eps * log(n)**2)
    significantNodes = []
    for node, pagerank in pageRankValues:
        if pagerank >= threshold/4.0:
            significantNodes.append((node, pagerank))
    return significantNodes
