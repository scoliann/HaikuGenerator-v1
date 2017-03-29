import string
import sys
sys.path.insert(0, 'textToMarkov')
import textToMarkov as ttm
sys.path.insert(0, 'textToGraph')
import textToGraph as ttg
sys.path.insert(0, 'clusterRecommender')
import clusterRecommender as cr


# The implementation of this function is stolen from the textstat python module
#	(https://pypi.python.org/pypi/textstat/0.1.4)
def syllable_count(text):
        """
        Function to calculate syllable words in a text.
        I/P - a text
        O/P - number of syllable words
        """
        count = 0
        vowels = 'aeiouy'
        text = text.lower()
        text = "".join(x for x in text if x not in list(string.punctuation))

        if text is None:
            return 0
        elif len(text) == 0:
            return 0
        else:
            if text[0] in vowels:
                count += 1
            for index in range(1, len(text)):
                if text[index] in vowels and text[index-1] not in vowels:
                    count += 1
            if text.endswith('e'):
                count -= 1
            if text.endswith('le'):
                count += 1
            if count == 0:
                count += 1
            count = count - (0.1*count)
            return round(count)


def createLine(syllableTotal, oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct, seedNode = ''):

	# Find a single valid haiku line
	sentenceDict = {}
	completeLine = ''
	startPoint = 0
	validLineFound = False
	while (validLineFound == False):

		# Generate sentence using textToMarkov
		sentence = ttm.createSentence(oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct, seedNode).split()

		# Keep track of sentences to see if one is repeating
		if str(sentence) not in sentenceDict:
			sentenceDict[str(sentence)] = 1
		else:
			sentenceDict[str(sentence)] += 1
		if sentenceDict[str(sentence)] >= 20:
			sentenceDict = {}
			seedNode = ''
			continue

		# Iterate through the sentence from the first word looking for the proper number of consecutive syllables, then from the second word, etc.
		while (startPoint < len(sentence)) and (validLineFound == False):
			syllableCounter = 0
			wordList = []
			for i in range(startPoint, len(sentence)):

				# Get the word and number of syllables
				word = ''.join(x for x in sentence[i] if x not in list(string.punctuation))
				numSyllables = syllable_count(word)

				# Add values to data structures
				syllableCounter += numSyllables
				wordList.append(word)

				# Check if an appropriate line has been found
				if syllableCounter == syllableTotal:
					completeLine = ' '.join(wordList)
					validLineFound = True
					break
				elif syllableCounter > syllableTotal:
					break					

			# Increment the starting point
			startPoint += 1

	# Return complete line of the haiku
	return completeLine


if __name__ == '__main__':

	# Set up textToMarkov
	ttm.setup()
	(oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct) = ttm.loadData('shakespeare.txt')

	# Set up textToGraph
	ttg.setup()
	G = ttg.loadData('shakespeare.txt')

	# Generate haikus
	counter = 0
	attemptNumber = 0
	text_file = open('shakespeareMarkovClusterHaikus.txt', "a")
	while counter < 100:

		print 'Attempt: \t' + str(attemptNumber + 1) + '\n'
		attemptNumber += 1

		# Generate a markov sentence with 5 syllables
		firstLine = createLine(5, oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct)

		# Get seed node for next line
		firstSeedNodes = firstLine.lower().split()
		firstSeed = cr.findNextNode(G, firstSeedNodes)
		if (firstSeed not in oneGram_noPunct) and (firstSeed not in oneGram_punct):
			continue

		# Generate a markov sentence with 7 syllables
		secondLine = createLine(7, oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct, firstSeed)
		if firstSeed != secondLine.split()[0].lower():
			continue

		# Get the seed node for next line
		secondSeedNodes = firstLine.lower().split() + secondLine.lower().split()
		secondSeed = cr.findNextNode(G, secondSeedNodes)
		if (secondSeed not in oneGram_noPunct) and (secondSeed not in oneGram_punct):
			continue

		# Generate a markov sentence with 5 syllables
		thirdLine = createLine(5, oneGram_noPunct, oneGram_punct, twoGram_noPunct, twoGram_punct, secondSeed)
		if secondSeed != thirdLine.split()[0].lower():
			continue

		# Increment counter
		counter += 1

		# Write lines to file
		text_file.write(str(counter) + '\n')
		text_file.write(str(firstLine) + '\n')
		text_file.write(str(secondLine) + '\n')
		text_file.write(str(thirdLine) + '\n\n')
		text_file.write(str(firstSeed) + '\n')
		text_file.write(str(secondSeed) + '\n')
		text_file.write('\n\n')

		print '\n\n'
		print '--SUCCESS #: \t' + str(counter) + '\n'
		print '--firstLine: \t' + str(firstLine)
		print '--secondLine: \t' + str(secondLine)
		print '--thirdLine: \t' + str(thirdLine)
		print '\n'
		print '--firstSeed: \t' + str(firstSeed)
		print '--secondSeed: \t' + str(secondSeed)
		print '\n\n'

	# Close file
	text_file.close()


	

	














