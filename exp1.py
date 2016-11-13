import time, pickle
from ApproxRow import RowApproximator
from ApproxPageRank import approxPageRank
from ApproxPageRankRefined import approxPageRankRefined

if __name__ == "__main__":
    loadStart = time.time()
    print "Load node list..."
    nodeList = pickle.load(open("node_list.p", "rb"))
    print "Load adjacency list..."
    adjList = pickle.load(open("adj_list.p", "rb"))
    print "Load complete in", time.time() - loadStart, "s"

    alpha = 0.15
    threshold = len(nodeList)/2
    #c = 6
    #delta = 0.5
    print "alpha =", alpha, "; threshold = ", threshold

    rowApproximator = RowApproximator(adjList, nodeList, alpha)
    print "Row approximator initialized."

    print "Start pagerank estimation"
    start = time.time()
    significantNodes = approxPageRank(threshold, nodeList, rowApproximator)
    #significantNodes = approxPageRank(c, threshold, delta, nodeList, rowApproximator)
    print "Pagerank estimated in", time.time() - start, "s"
    print "Found", len(significantNodes), "significant nodes."

    significantNodes.sort(key=lambda (node, pagerank): pagerank, reverse=True)
    for i in range(10):
        print significantNodes[i]

    print "Dumping significant nodes..."
    pickle.dump(significantNodes, open('exp1_85.p','wb'))
    print "Done."
