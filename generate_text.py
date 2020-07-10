# File: generate_text.py

import sys
from text_stats import suceedingwords
from text_stats import fileopen
from text_stats import texttowords
import random

def main():
	try:
		script = sys.argv[0]
		filename = sys.argv[1]
		cur_word = sys.argv[2]
		max_words = sys.argv[3]

		message = cur_word
		max_words = int(max_words)
		inputtext = fileopen(filename)
		text_words = texttowords(inputtext)

		l = 0
		while(l < max_words):
			next_words = suceedingwords(cur_word,text_words)
			if len(next_words) == 0:
				break
			else:
				choice = random.choices(tuple(next_words.keys()), tuple(next_words.values()), k=1)
				message = " ".join((message, str(choice[0])))
				l = l+1
		print(message)
	except IndexError:
		print("Please provide an Input text file, current word and length of text to be generated as inputs")
	except FileNotFoundError:
		print("The file does not Exist")
		
if __name__ == '__main__':
    main()