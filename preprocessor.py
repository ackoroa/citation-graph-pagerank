import sys, os
import pickle

article_store = {}
adjacency_list = {}
node_list = []
property_list = ['*','@','t','c','!']

def preprocess(data_file_path):
	count = 0
	with open(data_file_path) as input_file:
		temp_store = ""
		for line in input_file:
			if not line.startswith('#'):
				processArticle(temp_store)
				temp_store = ""
				count +=1 
				if count % 10000 == 0:
					print "Processed", count, "articles..."
			else:
				temp_store += line
			
def processArticle(temp_store):
	lines = [item for item in temp_store.split('\n') if len(item.strip()) > 0]
	articleDict = {}
	neighbours = []
	idx = ""
	for line in lines:
		line = line.strip()[1:]
		if line[0] in property_list:
			articleDict[line[0]] = line[1:]
		elif line[0] == '%':
			neighbours.append(line[1:])
		elif line.startswith('index'):
			idx = line[5:]
		else:
			continue
	if len(idx) < 1:
		return

	#print "Process article", idx, "# of source:", len(neighbours)
	article_store[idx] = articleDict
	adjacency_list[idx] = neighbours		


if __name__ == "__main__":
	data_file_path = sys.argv[1]
	preprocess(data_file_path)
	print "Article Stored:", len(article_store)
	# print "Dumping article_store..."
	# pickle.dump(article_store, open('article_store.p','w+'))
	# print "Dumping node_list..."
	# pickle.dump(adjacency_list.keys(), open('node_list.p','w+'))
	# print "Done.\nDumping adjacency_list..."
	# pickle.dump(adjacency_list, open('adj_list.p','w+'))
	# print "Done."

	a = article_store

	print "Article store loaded."
	input_text = ""
	while input_text != "exit":
		input_text = 'titles.p'
		# input_text = raw_input("Input list.p or article index: ")
		input_text = input_text.strip()
		if input_text.endswith('.p'):
			print "Reading input index list..."
			
			index_list = pickle.load(open(input_text, 'rb'))

			out_file = open('titles_result.txt', 'w+')
			out_string = ''
			for index in index_list:
				index = index[0]
				print "index:", index
				if '@' in a[index] and '*' in a[index]:
					out_string += a[index]['@'] + '\t' + a[index]['*'] + '\n'
			out_file.write(out_string)
			out_file.close()
			print "Titles written to", 'titles' + input_text + '.txt'
		else:
			print a[input_text]['@'] + '\t' + a[input_text]['*']

	
