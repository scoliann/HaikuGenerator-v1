import math
import sys
import random


'''
Program to find the next node that should be added to a cluster.
'''


def initializeDataStructures(G, startingNodes):

	# Calculate sum of edge weights from startingNodes to each node ajacent to and outside of startingNodes
	externalAjacentNodeDict = {}
	for node in startingNodes:
		for key in G[node]:
			if key not in startingNodes:
				if key not in externalAjacentNodeDict:
					externalAjacentNodeDict[key] = 0.0
				externalAjacentNodeDict[key] += G[node][key]
	
	# Calculate sum of edge weights from nodes ajacent to and outside of startingNodes to startingNodes
	externalDejacentNodeDict = {}
	for key in externalAjacentNodeDict:
		externalDejacentNodeDict[key] = 0.0
		for node in startingNodes:
			if node in G[key]:
				externalDejacentNodeDict[key] += G[key][node]

	# Calculate sum of outgoing edge weights from startingNodes
	totalOutgoingFromClusterEdgeWeight = 0.0
	for node in startingNodes:
		for key in G[node]:
			totalOutgoingFromClusterEdgeWeight += G[node][key]

	# Calculate sum of outgoing edge weights for each node in G
	totalOutgoingFromNodeEdgeWeight = {}
	for node in G:
		totalOutgoingFromNodeEdgeWeight[node] = 0.0
		for ajNode in G[node]:
			totalOutgoingFromNodeEdgeWeight[node] += G[node][ajNode]

	# Return data structures
	return (externalAjacentNodeDict, externalDejacentNodeDict, totalOutgoingFromClusterEdgeWeight, totalOutgoingFromNodeEdgeWeight)


def getDictMax(idict):
	maxValueInDict = max(idict.values())
	maxKeys = []
	for key in idict:
		if idict[key] == maxValueInDict:
			maxKeys.append(key)
	keyToReturn = random.choice(maxKeys)
	return keyToReturn


def findNextNode(G, startingNodes):

	# Initialize data structures needed to find a cluster
	(externalAjacentNodeDict, externalDejacentNodeDict, totalOutgoingFromClusterEdgeWeight, totalOutgoingFromNodeEdgeWeight) = initializeDataStructures(G, startingNodes)

	# Calculate the connectivity metric for the contender nodes
	connectivityMetric = {}
	for node in externalAjacentNodeDict:
		outgoingConnectivity = externalAjacentNodeDict[node] / (totalOutgoingFromClusterEdgeWeight + totalOutgoingFromNodeEdgeWeight[node])
		incomingConnectivity = externalDejacentNodeDict[node] / (totalOutgoingFromClusterEdgeWeight + totalOutgoingFromNodeEdgeWeight[node])
		connectivityMetric[node] = math.sqrt(outgoingConnectivity * incomingConnectivity)

	# Choose the best contender node
	contenderNode = getDictMax(connectivityMetric)

	# Return contenderNode
	return contenderNode

	
if __name__ == '__main__':

	# Example graph
	G = {'a': {'a': 1, 'b': 1, 'c': 1, 'z': 1},	'b': {'a': 1, 'c': 1},	'c': {'b': 1, 'd': 1},	'd': {'c': 1, 'a': 1}, 'z': {'a': 1, 'b': 1}}

	# Choose some starting nodes
	startingNodes = ['a']

	# Get the next node that goes with startingNodes
	contenderNode = findNextNode(G, startingNodes)
	print str(contenderNode)

	



