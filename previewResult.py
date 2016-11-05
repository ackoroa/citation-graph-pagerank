import pickle, sys

if __name__ == "__main__":
	# a = pickle.load(open('article_store.p', 'rb'))
	a = article_store

	print "Article store loaded."
	input_text = ""
	while input_text != "exit":
		input_text = raw_input("Input list.p or article index: ")
		input_text = input_text.strip()
		if input_text.endswith('.p'):
			print "Reading input index list..."
			
			index_list = pickle.load(open(input_text, 'rb'))

			out_file = open('titles_result.txt', 'w+')
			out_string = ''
			for index in index_list:
				out_string += a[index.strip()]['@'] + '\t' + a[index.strip()]['*'] + '\n'
			out_file.write(out_string)
			out_file.close()
			print "Titles written to", 'titles' + input_text + '.txt'
		else:
			print a[input_text]['@'] + '\t' + a[input_text]['*']




