import time, pickle
from FRank import fRank

if __name__ == "__main__":
    loadStart = time.time()
    print "Load node list..."
    nodeList = pickle.load(open("node_list.p", "rb"))
    print "Load adjacency list..."
    adjList = pickle.load(open("adj_list.p", "rb"))
    print "Load complete in", time.time() - loadStart, "s"

    alpha = 0.5
    k = 100
    print "alpha =", alpha, "; k = ", k

    print "Start computing top-k nodes"
    start = time.time()
    topKNodes = fRank(k, adjList, alpha)
    print "Top-k nodes computed in", time.time() - start, "s"
    print "Found", len(topKNodes), " nodes."

    for i in range(10):
        print topKNodes[i]

    print "Dumping top-k nodes..."
    pickle.dump(topKNodes, open('exp2.p','w+'))
    print "Done."
