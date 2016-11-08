import time, math
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
    G = getSeqAdjList(adjList, idToSeq)
    C = np.array(range(len(G)))
    revAdjList = getReverseAdjList(G)
    print "graph initialized in", time.time() - initStart, "s"

    i = 0
    lowerBounds = np.zeros(len(G))
    upperBounds = np.ones(len(G))
    mask = np.ones(len(G), dtype=bool)
    r_prev = np.zeros(len(G))
    pruneMap = {}
    while len(C) > k:
        itStart = time.time()
        print "iteration", i, ": len(C) =", len(C), 
        if i != 0:
            R = computeReachableNodes(C, revAdjList)
            print "; len(R) =", len(R),
            G = computePrunedGraph(G, R)
            print "; len(G) =", len(G),
            C = np.array(range(len(G)))
            revAdjList = getReverseAdjList(G)
            mask = np.array(list(R))
            r_prev = np.copy(r)[mask]
        print "; compute r",
        r = computeR(G, i)
        print "; compute lb",
        lowerBounds = equation7(len(C), alpha, lowerBounds[mask], r, i)
        print "; compute ub",
        upperBounds = equation8(len(C), alpha, upperBounds[mask], r, r_prev, G, i)
        print "; compute C",
        eps_i = computeEps_i(lowerBounds, k)
        print "; eps_i =", eps_i,
        C = C[upperBounds >= eps_i]

        i = i + 1
        print ";", time.time() - itStart, "s"

#    topKNodes = []
#    for c in C:
#        topKNodes.append(seqToId[c])
    return []#topKNodes

def getSeqAdjList(adjList, idToSeq):
    seqAdjList = {}

    for u, vs in adjList.iteritems():
        uSeq = idToSeq[u]
        seqAdjList[uSeq] = []
        for v in vs:
            vSeq = idToSeq[v]
            seqAdjList[uSeq].append(vSeq)
    return seqAdjList

def getReverseAdjList(adjList):
    revAdjList = {}
    for u, vs in adjList.iteritems():
        for v in vs:
            if not v in revAdjList:
                revAdjList[v] = []
            revAdjList[v].append(u)
    return revAdjList

def computeReachableNodes(C, revAdjList):
    queue = deque(C)
    visited = set()
    while len(queue) > 0:
        u = queue.popleft()
        visited.add(u)
        if u in revAdjList:
            for v in revAdjList[u]:
                if v not in visited:
                    queue.append(v)
    return visited

def computePrunedGraph(G, R):
    pruneMap = {}
    seq = 0
    for r in R:
        pruneMap[r] = seq
        seq = seq + 1

    prunedG = {}
    for u, vs in G.iteritems():
        if u in R:
            prunedG[pruneMap[u]] = []
            for v in vs:
                if v in R:
                    prunedG[pruneMap[u]].append(pruneMap[v])
    return prunedG

def computeR(G, i):
    e = np.ones(len(G)) * 1.0/len(G)
    if i == 0:
        return e
    elif i == 1:
        r = np.zeros(len(G))
        for u, vs in G.iteritems():
            r[u] = float(len(vs)) / len(G)
        return r
    else :
        r = np.zeros((len(G), len(G)))
        for u, vs in G.iteritems():
            for v in vs:
                r[u][v] = 1
        return np.linalg.matrix_power(r, i).dot(e)

def equation7(N, alpha, prevLowerBounds, r, i):
    if i == 0:
        return np.ones(N) * (1 - alpha)/N
    else:
        return np.add(prevLowerBounds, (1 - alpha) * math.pow(alpha, i) * r)

def equation8(N, alpha, prevUpperBounds, r, prevR, W, i):
    Wbar = []
    for u, vs in W.iteritems():
        if len(vs) > 0:
            Wbar.append(1)
        else:
            Wbar.append(0)
    Wbar = np.array(Wbar)
    if i == 0:
        return np.ones(N) * alpha/(1 - alpha) * Wbar
    else:
        bigDelta = np.sum(np.maximum(np.subtract(r, prevR), 0))
        delta = math.pow(alpha, i+1) / (1 - alpha)
        return np.add(prevUpperBounds, np.add(math.pow(alpha, i) * r, bigDelta * delta * Wbar))

def computeEps_i(lowerBounds, k):
    lb = np.copy(lowerBounds)
    lb.sort()
    return lb[k]