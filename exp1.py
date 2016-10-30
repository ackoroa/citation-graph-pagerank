from ApproxRow import RowApproximator
from ApproxPageRank import approxPageRank
import pickle


# This is equiv to call the main method in Java
if __name__ == "__main__":

	threshold = 1 # get the param
	row_approximator = RowApproximator('adjacency_list.p', 'node_list.p')

	node_list = pickle.load('node_list.p')
	
	sig_nodes = approxPageRank(threshold, node_list, row_approximator)

	print sig_nodes