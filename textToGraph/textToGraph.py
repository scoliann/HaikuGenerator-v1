import math
import os
import inspect
import dill as pickle
import shutil
import sys


'''
Input:	the name of a .txt file
Output:	a graph implemented using dictionaries in the form G[word1][word2] = the number of times that word2 is seen alongside word1 the lines of the input file

Example:	'the quick brown fox is a fox'	->	G[quick][fox] = 2.0	as the word 'fox' is seen alongside 'quick' twice in the input
'''


# Get the path to the location of textToMarkov.py
basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def setup():

	# Create corpuses folder if it does not already exist
	if not os.path.isdir(basePath + '/corpuses'):
		os.makedirs('/corpuses')

	# Create pickles folder if it does not already exist
	if not os.path.isdir(basePath + '/pickles'):
		os.makedirs(basePath + '/pickles')


def loadData(fileName, ireload=False):

	# Check if folder for fileName exists in "pickles"
	if (os.path.isdir(basePath + '/pickles/' + fileName.split('.txt')[0])) and (ireload == False):
		
		# Check if files for each of the necessary data structures exist
		if os.path.isfile(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + 'Graph.p'):
			G = pickle.load(open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + 'Graph.p', 'rb'))

	# If a folder for fileName does not exist in "pickles"
	else:

		# Read in text, turn into a graph, remove self cycles, and apply tfidf
		G = textToGraph(fileName)
		G = removeSelfCycles(G)
		G = applyTfIdf(G)

		# Save to pickle
		try:
			shutil.rmtree(basePath + '/pickles/' + fileName.split('.txt')[0])
			os.makedirs(basePath + '/pickles/' + fileName.split('.txt')[0])
		except:
			os.makedirs(basePath + '/pickles/' + fileName.split('.txt')[0])
		pickle.dump(G, open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + 'Graph.p', 'wb'))

	# Return values
	return G


def textToGraph(fileName):

	# Initialize graph
	G = {}

	# Read in file line by line
	with open(basePath + '/corpuses/' + fileName, "r") as ifile:
		for line in ifile:
			line = line.rstrip().split()

			# Clean words in line
			cleanedLine = []
			alphabet = 'abcdefghijklmnopqrstuvwxyz'
			for word in line:
				cleanedWord = ''.join([x for x in word.lower() if x in alphabet]).encode('ascii', 'ignore')
				if len(cleanedWord) > 0:
					cleanedLine.append(cleanedWord)

			# If cleanedLine is not empty
			if len(cleanedLine) > 0:

				# Increment edge weights according to the ajacencies of the words in line
				for indexI in range(len(cleanedLine)):
					for indexJ in range(len(cleanedLine)):
						if indexI != indexJ:
							wordI = cleanedLine[indexI]
							wordJ = cleanedLine[indexJ]

							# Manage keys in G according to ajacencies
							if wordI not in G:
								G[wordI] = {}
							if wordJ not in G[wordI]:
								G[wordI][wordJ] = 1.0
							else:
								G[wordI][wordJ] += 1.0

	# Return graph
	return G


def removeSelfCycles(G):
	newG = {}
	for node in G:
		for ajNode in G[node]:
			if node != ajNode:
				if node not in newG:
					newG[node] = {}
				newG[node][ajNode] = G[node][ajNode]
	return newG


def applyTfIdf(G):

	# Calculate the idf for each node in G
	idfDict = {}
	for idfNode in G:
		idfDict[idfNode] = 0.0
		for node in G:
			if idfNode in G[node]:
				idfDict[idfNode] += 1.0
		idfDict[idfNode] = math.log(len(G) / idfDict[idfNode], 2)

	# Calculate the tfidf for each ajacent-node to node in G
	for node in G:
		for ajNode in G[node]:
			ajNodeTf = 1.0 + math.log(G[node][ajNode], 2)
			ajNodeIdf = idfDict[ajNode]
			ajNodeTfIdf = ajNodeTf * ajNodeIdf
			G[node][ajNode] = ajNodeTfIdf

	# Return modified G
	return G
			

if __name__ == '__main__':

	# Get a graph of the complete works of shakespeare
	fileName = 'shakespeare.txt'
	G = textToGraph(fileName)









