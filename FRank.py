import numpy as np
from collections import deque

def fRank(k, adjList, alpha):
    seq = 0
    idToSeq = {}
    seqToId = {}
    for u, vs in adjList.iteritems():
        idToSeq[u] = seq
        seqToId[seq] = u
        seq = seq + 1
    G = getAdjMatrix(adjList, idToSeq)
    C = np.array(range(len(G)))
    revSeqAdjList = getReverseSeqAdjList(adjList, idToSeq)

    i = 0
    lowerBounds = np.zeros(len(G))
    upperBounds = np.ones(len(G))
    mask = np.ones(len(G), dtype=bool)
    while len(C) > k:
        if i != 0:
            R = computeReachableNodes(C, revAdjList)
            G = G[R][:,R]
        
        prevR = np.copy(r)[mask]
        r = np.linalg.matrix_power(G, i).dot(np.ones(len(G)) * 1.0/len(G))
        lowerBounds = equation7(len(G), alpha, lowerBounds[mask], r, i)
        upperBounds = equation8(len(G), alpha, upperBounds[mask], r, prevR, G, i)
        eps_i = np.copy(lowerBounds).sort()[k]
        mask = upperBounds >= eps_i
        C = C[mask]

        newSeqToId = {}
        seq = 0
        for idx in mask.nonzero():
            newSeqToId[seq] = seqToId[idx]
            seq = seq + 1
        seqToId = newSeqToId
        i = i + 1

    #This is wrong. After thr prunings the indices in the matrix 
    #no longer correspond to the initial indices
    topKNodes = []
    for c in C:
        topKNodes.append(seqToId[c])
    return topKNodes

def getAdjMatrix(adjList, idToSeq):
    adjMat = np.zeros((len(adjList), len(adjList)))
    for u, vs in adjList.iteritems():
        uSeq = idToSeq[u]
        for v in vs:
            vSeq = idToSeq[v]
            adjMat[uSeq][vSeq] = 1
    return adjMat

def getReverseSeqAdjList(adjList, idToSeq):
    revAdjList = {}
    for u, vs in adjList.iteritems():
        uSeq = idToSeq[u]
        for v in vs:
            vSeq = idToSeq[v]
            if not vSeq in revAdjList:
                revAdjList[vSeq] = []
            revAdjList[vSeq].append(uSeq)
    return revAdjList    

def computeReachableNodes(C, revSeqAdjList):
    R = []
    queue = deque(C)
    visited = set()
    while len(queue) > 0:
        u = queue.popLeft()
        visited.add(u)
        R.append(u)
        for v in revSeqAdjList[u]:
            if v not in visited:
                queue.append(v)
    return R

def equation7(N, alpha, prevLowerBounds, r, i):
    if i == 0:
        return np.ones(N) * (1 - alpha)/N
    else:
        return np.add(prevLowerBounds, (1 - alpha) * math.pow(alpha, i) * r)

def equation8(N, alpha, prevUpperBounds, r, prevR, W, i):
    Wbar = np.amax(W, axis=1) # max for each row
    if i == 0:
        return np.ones(N) * alpha/(1 - alpha) * Wbar
    else:
        bigDelta = np.sum(np.substract(r, prevR))
        delta = math.pow(alpha, i+1) * r
        return np.add(prevUpperBounds, math.pow(alpha, i) * r, bigDelta * delta * Wbar)
