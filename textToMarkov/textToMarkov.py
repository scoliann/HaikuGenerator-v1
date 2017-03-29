import random
import collections as cl
import dill as pickle
import os
import shutil
import sys
import inspect


# Get the path to the location of textToMarkov.py
basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def setup():

	# Create corpuses folder if it does not already exist
	if not os.path.isdir(basePath + '/corpuses'):
		os.makedirs('/corpuses')

	# Create pickles folder if it does not already exist
	if not os.path.isdir(basePath + '/pickles'):
		os.makedirs(basePath + '/pickles')


def generateDicts(fileName):

	# Initialize data structures
	oneGram_noPunct = cl.defaultdict(lambda: cl.Counter())
	oneGram_punct = cl.defaultdict(lambda: cl.Counter())
	twoGram_noPunct = cl.defaultdict(lambda: cl.Counter())
	twoGram_punct = cl.defaultdict(lambda: cl.Counter())
	
	# Read in from text file
	loading = 1
	with open(basePath + '/corpuses/' + fileName, "r") as ifile:
		for line in ifile:
			line = line.rstrip().split()
			
			# Print loading
			print "Processing Line: \t" + str(loading)
			loading += 1

			# Populate data structures with data
			for i in range(len(line)):

				# Try to add info to data structures
				try:
					# Add to 1-gram models
					alphabet = 'abcdefghijklmnopqrstuvwxyz'
					if i < (len(line) - 1):

						# Encode to ascii characters
						wordI = line[i].encode('ascii', 'ignore')
						wordJ = line[i+1].encode('ascii', 'ignore')
						wordI_noPunct = ''.join([ichar for ichar in line[i].lower() if ichar in alphabet]).encode('ascii', 'ignore')
						wordJ_noPunct = ''.join([ichar for ichar in line[i+1].lower() if ichar in alphabet]).encode('ascii', 'ignore')

						# Add to data structures
						oneGram_punct[wordI][wordJ] += 1.0
						oneGram_noPunct[wordI_noPunct][wordJ_noPunct] += 1.0

					# Add to 2-gram models
					if i < (len(line) - 2):

						# Encode to ascii characters
						wordK = line[i+2].encode('ascii', 'ignore')
						wordK_noPunct = ''.join([ichar for ichar in line[i+2].lower() if ichar in alphabet]).encode('ascii', 'ignore')

						# Add to data structures
						twoGram_punct[(wordI, wordJ)][wordK] += 1.0
						twoGram_noPunct[(wordI_noPunct, wordJ_noPunct)][wordK_noPunct] += 1.0

				# If an encoding error happens, pass
				except:
					pass

	# Save to pickle
	try:
		shutil.rmtree(basePath + '/pickles/' + fileName.split('.txt')[0])
		os.makedirs(basePath + '/pickles/' + fileName.split('.txt')[0])
	except:
		os.makedirs(basePath + '/pickles/' + fileName.split('.txt')[0])
	pickle.dump(oneGram_noPunct, open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_oneGram_noPunct.p', 'wb'))
	pickle.dump(oneGram_punct, open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_oneGram_punct.p', 'wb'))
	pickle.dump(twoGram_noPunct, open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_twoGram_noPunct.p', 'wb'))
	pickle.dump(twoGram_punct, open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_twoGram_punct.p', 'wb'))

	# Return values
	return (oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct)


def loadData(fileName, ireload=False):

	# Check if folder for fileName exists in "pickles"
	numFiles = 0
	if (os.path.isdir(basePath + '/pickles/' + fileName.split('.txt')[0])) and (ireload == False):
		
		# Check if files for each of the necessary data structures exist
		if os.path.isfile(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_oneGram_noPunct.p'):
			numFiles += 1
		if os.path.isfile(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_oneGram_punct.p'):
			numFiles += 1
		if os.path.isfile(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_twoGram_noPunct.p'):
			numFiles += 1
		if os.path.isfile(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_twoGram_punct.p'):
			numFiles += 1

		# If all necessary files are found, load data
		if numFiles == 4:
			oneGram_noPunct = pickle.load(open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_oneGram_noPunct.p', 'rb'))
			oneGram_punct = pickle.load(open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_oneGram_punct.p', 'rb'))
			twoGram_noPunct = pickle.load(open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_twoGram_noPunct.p', 'rb'))
			twoGram_punct = pickle.load(open(basePath + '/pickles/' + fileName.split('.txt')[0] + '/' + fileName.split('.txt')[0] + '_twoGram_punct.p', 'rb'))

	# If a folder for fileName does not exist in "pickles"
	else:

		# Create the data from scratch
		(oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct) = generateDicts(fileName)

	# Return values
	return (oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct)


def getNextWord(nGram_dict, key):

	# Run until next word is found
	while True:

		# Get the total for the key
		total = sum(nGram_dict[key].values())

		# Choose a random subKey
		subKey = random.choice(nGram_dict[key].keys())

		# Calculate subKey probability
		subKeyProb = nGram_dict[key][subKey] / total

		# Pick random value between 0 and 1
		randValue = random.uniform(0.0, 1.0)

		# If the probability is acceptable, use subKey
		if randValue <= subKeyProb:
			return subKey


def addNextWord(nGram_dict, key, sentence):

	# Get next word and update sentence
	nextWord = getNextWord(nGram_dict, key)
	sentence = sentence + ' ' + nextWord

	# Update key
	if type(key) == str:
		key = (key, nextWord)
	elif type(key) == tuple:
		key = (key[1], nextWord)

	# Return values
	return (key, sentence)


def createSentence(oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct, seedNode = ''):

	# If a seedNode is provided, use it as the start of a sentence
	terminationPunctuation = ['.', '?', '!']
	if seedNode != '':
		key = ('', seedNode)
		sentence = str(seedNode)

	# Else, choose a random key form which to start the sentence
	else:

		# Initialize sentence variable and choose starting point
		while True:

			# Initialize the termination flag to True
			noTerminationPunctuation = True

			# Get a key and create the starting sentence
			key = random.choice(twoGram_punct.keys())
			sentence = ' '.join(key)

			# Check if the key contains termination punctuation
			for punctuation in terminationPunctuation:
				if (punctuation in key[0]) or (punctuation in key[1]):
					noTerminationPunctuation = False

			# Break when a key with no termination punctuation is found
			if noTerminationPunctuation:
				break

	# Construct markov sentence
	keyDict = {}
	while True:

		# Add key to keyDict to prevent infinite key cycles
		if str(key) not in keyDict:
			keyDict[str(key)] = 1
		else:
			keyDict[str(key)] += 1
		if keyDict[str(key)] >= 20:
			key = random.choice(twoGram_punct.keys())
			sentence = ' '.join(key)
			keyDict = {}
			keyDict[str(key)] = 1

		# Attempt #1 - try to determine the next word using the 2-gram w/ punct model
		if key in twoGram_punct:
			(key, sentence) = addNextWord(twoGram_punct, key, sentence)

		else:
			
			# Attempt #2 - try to determine the next word using the 1-gram w/ punct model
			if key[1] in oneGram_punct:
				(key, sentence) = addNextWord(oneGram_punct, key[1], sentence)

			else:

				# Attempt #3 - try to determine the next word using the 2-gram w/o punct model
				if key in twoGram_noPunct:
					(key, sentence) = addNextWord(twoGram_noPunct, key, sentence)

				else:

					# Attempt #4 - try to determine the next word using the 1-gram w/o punct model
					if key[1] in oneGram_noPunct:
						(key, sentence) = addNextWord(oneGram_noPunct, key[1], sentence)

					# If a next word couldn't be found, restart
					else:
						key = random.choice(twoGram_punct.keys())
						sentence = ' '.join(key)
						
		# Check for sentence termination 
		for punctuation in terminationPunctuation:
			if punctuation in sentence:
			
				# Capitalize the first letter
				sentence = sentence.capitalize()

				# Return values
				return sentence


if __name__ == "__main__":

	# Get command line arguments
	inputFile = sys.argv[1]
	try:
		if sys.argv[2] == 'true':
			ireload = True
		elif sys.argv[2] == 'false':
			ireload = False
	except:
		ireload = False

	# Setup
	setup()
	
	# Load Data
	(oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct) = loadData(inputFile, ireload)

	# Create X Sentence
	text_file = open('output_' + inputFile, "a")
	for i in range(1000):

		# Get sentence
		sentence = createSentence(oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct)

		# Print progress
		print sentence + '\n'

		# Save data to file
		text_file.write(sentence + '\n')
	text_file.close()
	




