import math, pickle, random, time

class RowApproximator:	

	def __init__(self, adjacency_list, node_list, alpha=0.2):
		# start_time = time.time()
		self.adj_list = adjacency_list
		self.node_list = node_list
		self.n = len(node_list)
		self.alpha = alpha
		print "Row approximator initiated."
		# print "Time cost:", time.time() - start_time

	def initNodeCountTree(self):
		node_count_tree = {}
		for node in self.node_list:
			node_count_tree[node] = 0
		return node_count_tree

	def getAverageNodeCountTree(self, node_count_tree, r):
		# print "Get average of tree over", r, "rounds."
		for key in node_count_tree:
			node_count_tree[key] = 1.0 * node_count_tree[key] / r
		return node_count_tree

	def approxRow(self, v, eps, rho):
		# start_time = time.time()
		# print "approxRow: ", v
		length = int(math.ceil(math.log(4/eps, 1/(1-self.alpha))))
		r = int(math.ceil(1/(eps * rho * rho) * 16 * math.log(self.n, 2)))
		# print "r =",r, "length =", length

		node_count_tree = self.initNodeCountTree()

		for i in range(0, r):
			node_count_tree = self.walk(v, self.alpha, length, node_count_tree)
		
		node_count_tree = self.getAverageNodeCountTree(node_count_tree, r)
		# print "approxRow ok. Time cost:", time.time() - start_time
		return node_count_tree

	def walk(self, v, alpha, length, node_count_tree):
		count = 1
		cur_node = v
		next_node = v
		while count <= length:
			cur_node = next_node
			count += 1
			dice = random.random()
			if dice < alpha:    
				break
			else:
				neighbours = self.adj_list[cur_node]
				if len(neighbours) < 1:
					next_node = random.choice(self.node_list)
				else:
					next_node = random.choice(neighbours)

		node_count_tree[cur_node] += 1
		return node_count_tree

if __name__=="__main__":
	#This is just a demo to show how to use the rowApprox
	node_list = pickle.load(open("node_list.p", "rb"))
	adj_list = pickle.load(open("adjacency_list.p", "rb"))

	rowApproximator = RowApproximator(adj_list, node_list)
	v = '53908b1820f70186a0db3fdc'
	row_result = rowApproximator.approxRow(v, 0.2, 0.2)
	print "Calculation finished."

	#Just to get some sense of the result
	f = open('result.txt', 'w+')
	result = ""
	count = 0
	for key in row_result:
		if row_result[key] > 0:
			count += 1
			result +=  key + '\t ' + str(row_result[key]) + '\n'
	f.write(result)
	f.close()
	print "Done. count:", count


