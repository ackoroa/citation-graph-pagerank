import math, random, time

def approxPageRank(threshold, nodeList, rowApproximator):
    n = len(nodeList)
    print "n =", n

    chunks = {}
    h = int(math.ceil(math.log(n / (4.0 * threshold),2)))
    for t in range(0, h+1):
        epst = 2**-t
        print "t =", t, "/", h, "; epst =", epst
        S = int(math.ceil(4 * n * epst * math.log(n,2)**2 / threshold))
        for s in range(0, S):
            print "s =", s, "/", S,
            sStart = time.time()
            v = nodeList[random.randrange(n)]
            neighbourList = rowApproximator.approxRow(v, epst/2.0, 0.5)
            for neighbour, eps in neighbourList.iteritems():
                if not (neighbour, eps) in chunks:
                    chunks[(neighbour, eps)] = 0
                chunks[(neighbour, eps)] += 1
            print ";", time.time() - sStart, "s"

    pageRankValues = {}
    for (node, eps), val in chunks.iteritems():
        if val >= math.log(n,2)/2:
            if not node in pageRankValues:
                pageRankValus[node] = 0
            pageRankValus[node] += threshold / (2 * eps * math.log2(n)**2)
    
    significantNodes = []
    for node, pagerank in pageRankValues.iteritems():
        if pagerank >= threshold/4.0:
            significantNodes.append((node, pagerank))
    return significantNodes
