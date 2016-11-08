import time
import numpy as np
from collections import deque

def fRank(k, adjList, alpha):
    print "initialize graph"
    initStart = time.time()
    seq = 0
    idToSeq = {}
    seqToId = {}
    for u, vs in adjList.iteritems():
        idToSeq[u] = seq
        seqToId[seq] = u
        seq = seq + 1
    G = getAdjMatrix(adjList, idToSeq)
    C = np.array(range(len(G)))
    revAdjList = getReverseSeqAdjList(adjList, idToSeq)
    print "graph initialized in", time.time() - initStart, "s"

    i = 0
    lowerBounds = np.zeros(len(G))
    upperBounds = np.ones(len(G))
    mask = np.ones(len(G), dtype=bool)
    r_prev = np.zeros(len(G))
    while len(C) > k:
        itStart = time.time()
        print "iteration", i, ": len(C) =", len(C), 
        if i != 0:
            R = computeReachableNodes(C, revAdjList)
            G = computePrunedGraph(G, R)
            r_prev = np.copy(r)[mask]
        r = computeR(G, i)
        lowerBounds = equation7(len(G), alpha, lowerBounds[mask], r, i)
        upperBounds = equation8(len(G), alpha, upperBounds[mask], r, r_prev, G, i)
        eps_i = computeEps_i(lowerBounds, k)
        mask = upperBounds >= eps_i
        C = C[mask]

        newSeqToId = {}
        seq = 0
        for idx in mask.nonzero()[0]:
            newSeqToId[seq] = seqToId[idx]
            seq = seq + 1
        seqToId = newSeqToId
        i = i + 1
        print ";", time.time() - itStart, "s"

    topKNodes = []
    for c in C:
        topKNodes.append(seqToId[c])
    return topKNodes

def getAdjMatrix(adjList, idToSeq):
    adjMat = []
    for _ in range(len(adjList)):
        adjMat.append([])

    for u, vs in adjList.iteritems():
        uSeq = idToSeq[u]
        for v in vs:
            vSeq = idToSeq[v]
            adjMat[uSeq].append(vSeq)
    return np.array(adjMat)

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
        u = queue.popleft()
        visited.add(u)
        R.append(u)
        for v in revSeqAdjList[u]:
            if v not in visited:
                queue.append(v)
    return R

def computePrunedGraph(G, R):
    G = G[R]
    rSet = set(R)
    for u in G:
        vs = G[u]
        mask = []
        for v in vs:
            mask.append(v in R)
        G[u] = G[u][mask]
    return G

def computeR(G, i):
    if i == 0:
        return np.ones(len(G)) * 1.0/len(G)
    else:
        r = []
        for u in G:
            r.append(float(len(G[u]))/len(G))
        return r

def equation7(N, alpha, prevLowerBounds, r, i):
    if i == 0:
        return np.ones(N) * (1 - alpha)/N
    else:
        return np.add(prevLowerBounds, (1 - alpha) * math.pow(alpha, i) * r)

def equation8(N, alpha, prevUpperBounds, r, prevR, W, i):
    Wbar = []
    for w in W:
        if len(w) > 0:
            Wbar.append(1)
        else:
            Wbar.append(0)
    Wbar = np.array(Wbar)
    if i == 0:
        return np.ones(N) * alpha/(1 - alpha) * Wbar
    else:
        bigDelta = np.sum(np.substract(r, prevR))
        delta = math.pow(alpha, i+1) * r
        return np.add(prevUpperBounds, math.pow(alpha, i) * r, bigDelta * delta * Wbar)

def computeEps_i(lowerBounds, k):
    lb = np.copy(lowerBounds)
    lb.sort()
    return lb[k]