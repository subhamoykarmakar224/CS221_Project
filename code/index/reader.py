from bs4 import BeautifulSoup
import os, json, sys, time
from Posting import Posting
from nltk.tokenize import word_tokenize
def reader():
	inv_index = {}

	start = time.time()
	for root, subdir, files in os.walk("../DEV"):

		for f in files:

			# print("PARSING FILE: ", f)
			tokenCount = {}
			if os.path.isfile(os.path.join(root, f)):
				f = open(os.path.join(root, f), "r")
				data = json.load(f)
				soup = BeautifulSoup(data["content"], "html.parser")
				tokens = word_tokenize(soup.get_text(separator="\n", strip=True))

				# loop and count tokens
				for token in tokens:
					token = token.lower()
					if token in tokenCount:
						tokenCount[token] += 1
					else:
						tokenCount[token] = 1
			
			f.close()
			# loop through token, freq pairs and add to the inverted index
			for token in tokenCount:
				index = Posting(f.name, tokenCount[token]) 
				if token in inv_index:
					inv_index[token].append(index)
				else:
					inv_index[token] = [index]

	end = time.time()
	print(inv_index)
	print(f"size of index (KB): {sys.getsizeof(inv_index)/1000}")
	print("Elapsed time (seconds): ", end-start)

if __name__ == "__main__":
	reader()
