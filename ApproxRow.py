import math, pickle, random, time

class RowApproximater:	

	def __init__(self, adjacency_list_file, node_list_file, alpha=0.2):
		print "Loading adjacency list..."
		start_time = time.time()
		self.adj_list = pickle.load(open(adjacency_list_file, 'rb'))
		print "Loading node list..."
		self.node_list = pickle.load(open(node_list_file, 'rb'))
		self.n = len(node_list_file)
		self.alpha = alpha
		print "Row approximator initiated. Time cost:", time.time() - start_time

	def initNodeCountTree(self):
		node_count_tree = {}
		for node in self.node_list:
			node_count_tree[node] = 0
		return node_count_tree

	def getAverageNodeCountTree(self, node_count_tree, r):
		for key in node_count_tree:
			node_count_tree[key] = node_count_tree[key] / r

	def approxRow(self, v, eps, rho):
		start_time = time.time()
		print "approxRow: ", v
		length = int(math.ceil(math.log(4/eps, 1/(1-self.alpha))))
		r = int(math.ceil(1/(eps * rho * rho) * 16 * math.log(self.n, 2)))
		print "r =",r, "length =", length

		node_count_tree = self.initNodeCountTree()

		# print "Node_count_tree inited. length:", len(node_count_tree)

		for i in range(0, r):
			print "i =", i
			self.walk(v, self.alpha, length, node_count_tree)
		
		self.getAverageNodeCountTree(node_count_tree, r)
		print "approxRow ok. Time cost:", time.time() - start_time
		return node_count_tree

	def walk(self, v, alpha, length, node_count_tree):
		print "walk form v", v
		count = 1
		cur_node = v

		while count <= length:
			count += 1
			dice = random.random()
			# print "cur node is", cur_node
			# print "rolling dice...", dice
			if dice < alpha:
				# print "dice < alpha. Stop."
				break
			else:
				neighbours = self.adj_list[cur_node]
				if len(neighbours) < 1:
					cur_node = random.choice(self.node_list)
				else:
					cur_node = random.choice(neighbours)

		# print "walk stopped, cur_node is:", cur_node
		node_count_tree[cur_node] += 1
		return node_count_tree

if __name__=="__main__":
	rowApproximater = RowApproximater('adjacency_list.p', 'node_list.p')
	v = '53908b1820f70186a0db3fdc'
	row_result = rowApproximater.approxRow(v, 0.2, 0.2)
	print "Calculation finished. Dumping..."
	pickle.dump(row_result, open('result.p', 'w+'))
	print "Done."


