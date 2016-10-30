import time, pickle
from ApproxRow import RowApproximator
from ApproxPageRank import approxPageRank

if __name__ == "__main__":
    loadStart = time.time()
    print "Load node list..."
    nodeList = pickle.load(open("node_list.p", "rb"))
    print "Load adjacency list..."
    adjList = pickle.load(open("adj_list.p", "rb"))
    print "Load complete in", time.time() - loadStart, "ms"

    alpha = 0.01
    threshold = len(nodeList)/2
    
    print "Init row approximator"
    rowApproximator = RowApproximator(adjList, nodeList, alpha)

    print "Start pagerank estimation"
    start = time.time()
    significantNodes = approxPageRank(threshold, nodeList, rowApproximator)
    print "Pagerank estimated in", time.time() - start, "ms"
    print significantNodes
