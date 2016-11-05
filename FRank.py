import numpy as np

def fRank(k, adjList, alpha):
    i = 0
    N = len(adjList)
    C = adjList.keys()
    G = getAdjMatrix(adjList)
    e = np.ones(N) * 1.0/len(N)

    lowerBounds = np.zeros(N)
    upperBounds = np.ones(N)
    while len(C) > k:
#        if i != 0:
#            R = computeR(C, G)
#            G = computeG(R)
        r = computeProbabilityOfILengthRandomWalk(G, i, e)
        lowerBounds = equation7(N, alpha, lowerBounds, r)
        upperBounds = equation8(N, alpha, upperBounds, r, G)
#        epsi = computeEpsi(C, lowerBounds)
#        C = computeC(epsi, C, upperBounds)
        i = i + 1
    return C

def getAdjMatrix(adjList):
    adjMat = np.zeros((len(adjList), len(adjList)))

    for u, vs in adjList.iteritems():
        for v in vs:
            adjMat[u][v] = 1
    return adjMat

def computeProbabilityOfILengthRandomWalk(W, i, e):
    return np.linalg.matrix_power(W, i).dot(e)

def equation7(N, alpha, prevLowerBounds, r):
    pass

def equation8(N, alpha, prevLowerBounds, r, W):
    pass
