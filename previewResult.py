import pickle, sys

if __name__ == "__main__":
	a = pickle.load(open('article_store.p', 'rb'))

	print "Article store loaded."
	input_text = ""
	while input_text != "exit":
		input_text = raw_input("Input list.p or article index: ")
		input_text = input_text.strip()
		if input_text.endswith('.p'):
			print "Reading input index list..."
			
			index_list = pickle.load(open(input_text, 'rb'))

			out_file = open(input_text+'.txt', 'w+')
			out_string = ''
			for index in index_list:
				index_clean = index[0].strip()
				if index_clean in a and '@' in a[index_clean] and '*' in a[index_clean]:
					out_string += a[index_clean]['@'] + '\t' + a[index_clean]['*'] + '\n'
			out_file.write(out_string)
			out_file.close()
			print "Titles written to", 'titles' + input_text + '.txt'
		else:
			print a[input_text]['@'] + '\t' + a[input_text]['*']




