import math, pickle, random

class rowApprocimater:	

	def __init__(self, adjacency_list_file, node_list_file):
		self.adj_list = pickle.load(open(adjacency_list_file, 'rb'))
		self.node_list = pickle.load(open(node_list_file, 'rb'))
		self.n = len(node_list_file)

	def initNodeCountTree():
		node_count_tree = {}
		for node in self.node_list:
			node_count_tree[node] = 0
		return node_count_tree

	def averageNodeCountTree(node_count_tree, r):
		for key in node_count_tree:
			node_count_tree[key] = node_count_tree[key] / r
		return node_count_tree

	def approxRow(rho, eps, alpha, v):
		length = math.log(4/eps, 1/(1-alpha))
		r = 1/(epi * rho * rho) * 16 * math.log2(self.n)

		node_count_tree = initNodeCountTree()

		for i in range(0, r):
			node_count_tree = walk(v, alpha, length, node_count_tree)

		node_count_tree = averageNodeCountTree(node_count_tree, r)
		return node_count_tree

	def walk(v, alpha, length, node_count_tree):
		count = 1
		cur_node = v
		next_node = ''

		while next_node != v and count < length:
			count += 1
			# get next node
			neighbours = adj_list[cur_node]
			if len(neighbours) < 1:
				next_node = random.choice(node_list)
			else:
				dice = random.random()
				if dice < alpha:
					next_node = v
				else:
					next_node = random.choice(neighbours)

		node_count_tree[cur_node] += 1


