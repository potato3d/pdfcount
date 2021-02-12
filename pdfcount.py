import os, sys
import pdf2txt
import copy
from collections import OrderedDict

results = OrderedDict()
global_word_count = OrderedDict()
global_word_count["bim"] = 0
global_word_count["lean"] = 0
global_word_count["construction"] = 0
global_word_count["sustainable"] = 0
global_word_count["sustainability"] = 0

def create_word_count():	
	return copy.deepcopy(global_word_count)

def pdf_to_text(pdf, text):
	args = ["", "-o", text, pdf]
	pdf2txt.main(args)

def count_words(fp):
	print os.path.basename(fp)
	tfp = os.path.splitext(fp)[0] + ".txt"
	pdf_to_text(fp, tfp)
	with open(tfp, "r") as text:
		word_count = create_word_count()
		for word in text.read().split():
			w = word.lower()
			if w in word_count:
				word_count[w] += 1
		results[os.path.basename(fp)] = word_count

if __name__ == "__main__":
	# get input directory
	if len(sys.argv) < 2:
		print("Usage: python pdfcount.py [input_directory]")
		sys.exit(1)
	input_dir = sys.argv[1]
	if not os.path.isabs(input_dir):
		input_dir = os.path.abspath(input_dir)
	# process files
	for f in os.listdir(input_dir):
		fp = os.path.join(input_dir, f)
		if os.path.isfile(fp) and os.path.splitext(fp)[1] == ".pdf":
			count_words(fp)
	# output word counts
	with open("saida.csv", "w") as output:
		output.write("paper;")
		for k in global_word_count.keys():
			output.write(k + ";")
		output.write("\n")
		for rk, rv in results.iteritems():
			output.write(rk + ";")
			for wk, wv in rv.iteritems():
				output.write(str(wv) + ";")
			output.write("\n")