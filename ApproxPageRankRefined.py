import math, random, time

def approxPageRankRefined(c, threshold, delta, nodeList, rowApproximator):
    n = len(nodeList)
    print "n =", n

    beta = (c - 1.0) / (5.0 * c)
    tao = math.ceil(math.log(2.0*n/delta, 2))
    h = math.ceil(3.0*n / (threshold*beta*beta))
    L = int(tao * h)
    p = delta / (2 * L)
    lmbda = beta / 2.0
    psi = beta / 2.0
    rho = 1 - lmbda - psi
    print "beta =", beta, "; tao = ", tao, "; h = ", h, "; L = ", L, "; p = ", p, "; psi = ", psi, "; rho = ", rho   
    print "eps =", math.ceil(1/tao) / h, "; lambda = ", lmbda

    pageranks = {}
    for t in range(1, L+1):
        epst = math.ceil(t/tao) / h
        
        tStart = time.time()
        #if t % 100 == 0:
        print "t =", t, "-", min(t,L), "/", L, "; epst =", epst,

        v = nodeList[random.randrange(n)]
        neighbourList = rowApproximator.approxRowRefined(v, psi * epst, lmbda, p)
        for neighbour, q in neighbourList.iteritems():
            if q >= epst and q <= 1/rho:
                if not neighbour in pageranks:
                    pageranks[neighbour] = 0
                pageranks[neighbour] += q

        #if t % 100 == 99:
        print "; time/sample = ", (time.time() - tStart) #/ 100.0
        tStart = time.time()
    #print "; time/sample = ", (time.time() - tStart) / (L % 100)
    
    significantNodes = []
    for node, pagerank in pageranks.iteritems():
        if pagerank >= (1 - 2*beta) * L * threshold / n and pagerank <= L:
            significantNodes.append((node, pagerank))
    return significantNodes
