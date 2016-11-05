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
        prevR = np.copy(r)
        r = computeProbabilityOfILengthRandomWalk(G, i, e)
        lowerBounds = equation7(N, alpha, lowerBounds, r, i)
        upperBounds = equation8(N, alpha, upperBounds, r, prevR, G, i)
       epsi = computeEpsi(C, lowerBounds, k)
       C = computeC(epsi, C, upperBounds)
        i = i + 1
    return C

def getAdjMatrix(adjList):
    adjMat = np.zeros((len(adjList), len(adjList)))

    for u, us in adjList.iteritems():
        for v in vs:
            adjMat[u][v] = 1
    return adjMat

def computeProbabilityOfILengthRandomWalk(W, i, e):
    return np.linalg.matrix_power(W, i).dot(e)

def equation7(N, alpha, prevLowerBounds, r, i):
    if i == 0:
        return np.ones(N) * (1 - alpha)/N
    else:
        return np.add(prevLowerBounds, (1 - alpha) * math.pow(alpha, i) * r)

def equation8(N, alpha, prevLowerBounds, r, prevR, W, i):
    Wbar = np.amax(W, axis=1) # max for each row, need to confirm with you
    if i == 0:
        return np.ones(N) * alpha/(1 - alpha) * Wbar
    else:
        bigDelta = np.sum(np.substract(r, prevR))
        delta = math.pow(alpha, i+1) * r
        return np.add(prevLowerBounds, math.pow(alpha, i) * r, bigDelta * delta * Wbar)

# These 2 are for eqn 6
def computeEpsi(C, lowerBounds, k):
    kthHighest = lowerBounds.sort()[k]
    return kthHighest

def computeC(epsi, C, upperBounds):
    mask = upperBounds > epsi
    C = [elm for (idx, elm) in C if mask[idx]]
    return C
