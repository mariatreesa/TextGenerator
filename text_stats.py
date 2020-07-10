# File: text_stats.py

import sys
from collections import OrderedDict
import string
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords 
import csv



# Defining functions


# function to print a dictionary
def printdictionary(dict):
	for k,v in dict.items():
		print(' ', k, '     :  ', v,)

# Function to write a dictionary in table format
def writedictionary(dict,w):
	for k,v in dict.items():
		w.writerow([k,v])

# Open file
def fileopen(filename):
	with open(filename,'r', encoding='utf-8') as f:
			inputfile = f.read()
	inputtext = inputfile.lower()
	return inputtext

def texttowords(inputtext):
	text_words = re.split(r"[\s\.,\?\]\:\;\!\*]+",inputtext)
	return text_words

	
 # Function to return frequency table for alphabetic letters from inputfile 
def charfrequency(inputtext):
	alphabet_set = set(string.ascii_lowercase)
	text_characters = inputtext.strip()
	charfreq = {}
	for i in alphabet_set:
		charfreq[i] = text_characters.count(i)
	sorted_byfreq = OrderedDict(sorted(charfreq.items(), key=lambda x: x[1], reverse = True))
	return sorted_byfreq

# Function to return unique words and frequency of each word in inputfile
def wordfrequency(inputtext):
	wordfreq = {}
	text_words = texttowords(inputtext)
	for w in text_words:
	       if w in wordfreq:
	           wordfreq[w] = wordfreq[w] + 1
	       else:
	           wordfreq[w] = 1
	sorted_wordfreq = OrderedDict(sorted(wordfreq.items(), key=lambda x: x[1], reverse = True))
	return sorted_wordfreq


# returns all suceeding words of a word along with the frequency
def suceedingwords(word,text_words):
	l = [text_words[i+1] for i in range(len(text_words)) if text_words[i] == word]
	c =  Counter(l)
	sorteddict = OrderedDict(sorted(c.items(), key=lambda x: x[1], reverse = True))
	return(sorteddict)



# Function to return n suceeding words of a word
def n_suceedingwords(worddictionary, inputtext, n):
	followingwords = {}
	for key,value in worddictionary.items():
		sorteddict = suceedingwords(key,inputtext)
		topn = {k: sorteddict[k] for k in list(sorteddict)[:n]}
		followingwords[key] = topn
	return followingwords




def main():
	try:
		script = sys.argv[0]
		filename = sys.argv[1]
		inputtext = fileopen(filename)

		sorted_byfreq = charfrequency(inputtext)
		print(' ', "Char", '  :  ', "Freq")
		printdictionary(sorted_byfreq)

		wordfreq = wordfrequency(inputtext)
		print("\nTotal words: ",  sum(wordfreq.values()))
		print("Unique Words: ", len(wordfreq))

		stop_words = set(stopwords.words('english'))
		wordfreq_nostopwords = {k:v  for k,v in wordfreq.items() if k not in stop_words}
		top_words_nostopwords  = {k: wordfreq_nostopwords[k] for k in list(wordfreq_nostopwords)[:5]}

		print("\n Top Words Ignoring stopwords:\n")
		printdictionary(top_words_nostopwords)

		top3_followingwords = n_suceedingwords(top_words_nostopwords,texttowords(inputtext),3)

		print("\nTop 3 words following the most common words")
		for key,value in top3_followingwords.items():
			print(f'{key} ({top_words_nostopwords[key]} occurrences)')
			printdictionary(value)

		if len(sys.argv) == 3:
			outfile = sys.argv[2]r
			with open(outfile,'a', encoding='utf-8') as outf:
				w = csv.writer(outf)
				outf.write("Characters in text file  and corresponsing frequencies\n")
				writedictionary(sorted_byfreq,w)
				outf.write('\nTotal Words:')
				outf.write(str(sum(wordfreq.values())))
				outf.write("\n\nUnique Words: ")
				outf.write(str(len(wordfreq)))
				outf.write("\n\nTop Words Ignoring stopwords:\n")
				writedictionary(top_words_nostopwords,w)
				outf.write("\nTop 3 words following the most common words\n\n")
				for key,value in top3_followingwords.items():
					outf.write(str(key))
					outf.write(": occurrences - ")
					outf.write(str(top_words_nostopwords[key]))
					outf.write("\n")
					writedictionary(value,w)
					outf.write("\n")

	except IndexError:
		print("Please provide an Input text file")
	except FileNotFoundError:
		print("The file does not Exist")

if __name__ == '__main__':
    main()