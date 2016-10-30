import math, random
from ApproxRow import RowApproximator

def approxPageRank(threshold, nodeList, rowApproximator):
    n = len(nodeList)

    chunks = {}
    h = math.log2(n / (4.0 * threshold))
    for t in range(0, h+1):
        epst = 2**-t
        S = 4 * n * epst * math.log2(n)**2 / threshold
        for s in range(0, S):
            v = nodeList[random.randrange(n)]
            neighbourList = rowApproximator.approxRow(v, epst/2.0, 0.5)
            for neighbour, eps in neighbourList.iteritems():
                if not (neighbour, eps) in chunks:
                    chunks[(neighbour, eps)] = 0
                chunks[(neighbour, eps)] += 1
    
    pageRankValues = {}
    for (node, eps), val in chunks.iteritems():
        if val >= math.log2(n)/2:
            if not node in pageRankValues:
                pageRankValus[node] = 0
            pageRankValus[node] += threshold / (2 * eps * math.log2(n)**2)
    
    significantNodes = []
    for node, pagerank in pageRankValues.iteritems():
        if pagerank >= threshold/4.0:
            significantNodes.append((node, pagerank))
    return significantNodes

if __name__=="__main__":
    nodeList = pickle.load(open("node_list.p", "rb"))
    adjList = pickle.load(open("adjacency_list.p", "rb"))
    alpha = 0.01
    threshold = len(nodeList)/2

    rowApproximator = RowApproximator(adjList, nodeList, alpha)
    significantNodes = approxPageRank(threshold, nodeList, rowApproximator)
