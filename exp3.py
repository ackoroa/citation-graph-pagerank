import pickle as pk
import networkx as nx
import time
k = 100

node_list = pk.load(open('node_list.p', 'rb'))
adj_list = pk.load(open('adjacency_list.p', 'rb'))

print "Node and adj are loaded..."

start = time.time()

G = nx.DiGraph()

G.add_nodes_from(node_list)

for node in adj_list:
	for nbr in adj_list[node]:
		G.add_edge(node, nbr)

passed = time.time() - start;

print "Graph is inited..in", passed, "seconds."

inverse_dict =[ (key, val) for key, val in nx.pagerank(G).iteritems()]

passed2 = time.time() - start;

print "Page rank is ready...in", passed2, "seconds."

inverse_dict.sort(key=lambda x: x[1], reverse=True)

print "Top K is:", [key for (key, val)in inverse_dict][:k]

print "Dumping...."

pk.dump(inverse_dict, open('exactResult.p', 'wb'))

print "Done."



