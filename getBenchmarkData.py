from preprocessor import Preprocessor
import pickle as pk
from sets import Set

p = Preprocessor('citation-acm-v8.txt')
p.preprocess()
print "Done. adj_list length:", len(p.adjacency_list)

node_list = Set()
print "Load pickle for node_list.p"
new_nodes = Set([title[0] for title in pk.load(open('titles.p', 'rb'))[0:10]])
print "Done. len:", len(new_nodes)
print "sample:", next(iter(new_nodes))
parent = Set()
iter_count = 0


while len(new_nodes) > 0:
	print "iter:", iter_count
	iter_count += 1
	print "new nodes:", len(new_nodes)
	for key in p.adjacency_list:
		if not (key in new_nodes) and len(new_nodes.intersection(p.adjacency_list[key])) > 0:
			parent.add(key)
	print "parents found:", len(parent)
	node_list = node_list.union(new_nodes)
	length = len(node_list)
	print "node list grows to:", length
	if length > 40000:
		break;
	new_nodes = parent.copy()
	parent = Set()
	print "========="

print "Final:", len(node_list)

adj_list_cut = {}
for node in node_list:
	nbrs = list(Set(p.adjacency_list[node]).intersection(node_list))
	adj_list_cut[node] = nbrs


print "Dumping...."
pk.dump(node_list, open('node_list_cut.p', 'wb'))
pk.dump(adj_list_cut, open('adj_list_cut.p', 'wb'))



