
EMPTY = 0
MUSKEETER = 1
SOLDIER = 2
DIAMOND = 3

class Node(object):
	""" Represent a node on the game board.
	"""
	def __init__(self, position, heuristicVal, gVal):
		""" Initalize a node.

		:param position: [row, col] describing a position on the board.
		:param heuristicVal: Heuristic value from the position to goal.
		:param gVal: Cost from start state to this state.

		"""
		super(Node, self).__init__()
		self.position = position
		self.heuristicVal = heuristicVal
		self.gVal = gVal
		self.fVal = self.heuristicVal + self.gVal

def singleAgentSearch(board):
	""" Wrapper method for idaStar which calls idaStar for 
	each musketeer on the board and keeps track of the one which
	finds the diamond in shortest number of steps.

	:param board: The square game board which is a 2d list of integers.
	:returns: A tuple containing exploredNodes, searchQueue and the shortestPath
		corresponding to the musketeer which finds the diamond in the shortest 
		number of steps.

	"""
	exploredNodes, searchQueue, shortestPath  = [], [], []

	(musketeerPositions, diamondPosition) = getMusketeerAndDiamondPositions(board)
	if len(musketeerPositions) == 0:
		raise NoMusketeerFound

	if len(diamondPosition) == 0:
		raise NoDiamondFound

	# (exploredNodes, searchQueue, shortestPath) = \
	# 	idaStar(board, musketeerPositions[1], diamondPosition)
	for i in range(len(musketeerPositions)):
		(newExploredNodes, newSearchQueue, newShortestPath) = \
			idaStar(board, musketeerPositions[i], diamondPosition)

		if  shortestPath == [] \
		or  (
				len(newShortestPath) < len(shortestPath) \
				and len(newShortestPath) > 0
			):
			(exploredNodes, searchQueue, shortestPath) = \
				(newExploredNodes, newSearchQueue, newShortestPath)

	return (exploredNodes,searchQueue,shortestPath)

def idaStar(board, musketeerPosition, diamondPosition):
	""" Call idaStarIteration iteratively.

	Call idaStarIteration for each iteration with a new bound and aggregate 
	exploredNodes, searchQueue different iterations of the search.

	:param board: The game board.
	:param musketeerPosition: The [row, col] of musketeer on the board.
	:param diamondPosition: The [row, col] of diamond on the board.
	:returns: A tuple containing exploredNodes, searchQueue, shortestPath.

	"""
	exploredNodes, searchQueue = [], []

	# Use heuristic value from start node as the initial bound.
	bound = getHeuristicValue(musketeerPosition, diamondPosition)

	while True:
		(newExploredNodes, newSearchQueue, shortestPath, nextBound) = \
			idaStarIteration(board, musketeerPosition, diamondPosition, bound)

		exploredNodes.extend(newExploredNodes)
		searchQueue.extend(newSearchQueue)

		if len(shortestPath) == 0:
			# Increase the bound and restart search.
			bound = nextBound
		else:
			# Goal found.
			break

	return exploredNodes, searchQueue, shortestPath

def idaStarIteration(board, musketeerPosition, diamondPosition, bound):
	""" Perform a single iteration of IDA* search on the game board with
	the given bound.

	:param board: The game board.
	:param musketeerPosition: The [row, col] of musketeer on the board.
	:param diamondPosition: The [row, col] of diamond on the board.
	:param bound: The threshold on f value for this iteration. Neighbour
		nodes having f value greater than this aren't explored in this
		iteration.
	:returns: A tuple containing exploredNodes, searchQueue, shortestPath,
		and the next higher bound to start with in the next iteration in
		case the goal isn't found in this iteration.

	"""
	totalRows = totalColumns = len(board)
	exploredNodes, searchQueue, iterativeSearchQueue, shortestPath = [],[],[],[]
	# List of nodes visited and the position from which they were visited.
	# Used for calculating shortest path.
	visited = [[False for i in range(totalRows)] for i in range(totalColumns)]

	goalFound = False
	nextBound = -1

	musketeerNode = Node(
		musketeerPosition,
		getHeuristicValue(musketeerPosition, diamondPosition),
		0 # g value from start node.
	)
	searchQueue.append(musketeerNode)
	while len(searchQueue) != 0:
		currentNode = searchQueue[0]
		del(searchQueue[0])

		[row, col] = currentNode.position
		currentGVal = currentNode.gVal

		exploredNodes.append([row, col])

		if board[row][col] == DIAMOND:
			# Diamong found! Append the remaining queue as part of this
			# iteration and break.
			goalFound = True
			iterativeSearchQueue.append(getNodePositionsFromQueue(searchQueue))
			break

		paths = numberOfPaths(board, [row, col], visited)
		neighbours = []
		for path in paths:
			heuristicVal = getHeuristicValue(path, diamondPosition)
			pathNode = Node(path, heuristicVal, currentGVal + 1)
			if pathNode.fVal > bound:
				# Neighbouring node has greater f value. Don't explore it
				# in this search iteration.
				if nextBound == -1:
					# Remember to start with the next higher f value in next
					# iteration if goal isn't found in this iteration.
					nextBound = pathNode.fVal
				continue
			visited[path[0]][path[1]] = [row, col]
			neighbours.append(pathNode)

		# Append to the front of the queue.
		searchQueue = neighbours + searchQueue
		iterativeSearchQueue.append(getNodePositionsFromQueue(searchQueue))

	if goalFound:
		shortestPath = \
			getShortestPath(visited, musketeerPosition, diamondPosition)

	return (exploredNodes, iterativeSearchQueue, shortestPath, nextBound)

def getNodePositionsFromQueue(queue):
	""" Return the positions of the node presently in the queue.

	Extracts position from each Node object in the queue and puts in
	a list.

	:param queue: The queue.
	:return: A list of positions of the node in the queue.

	"""
	positions = [node.position for node in queue]
	return positions

def printSearchQueue(queue, bound):
	""" Print positions present in the queue
	"""
	for node in queue:
		print node.position, bound
	print

def getHeuristicValue(position, diamondPosition):
	""" Return the heuristic value of a position.

	:param position: The position whose heuristic value is to be calculated.
	:param diamondPosition: The position of the diamond on the board.
	:return: The heuristic value of the position.

	"""
	return (
		abs(position[0] - diamondPosition[0]) + 
		abs(position[1] - diamondPosition[1])
	)


def numberOfPaths(board, pos, visited):
	""" Return different possible paths from a given position.
	todo
	Return the different possible paths that can be taken from a
	given position excluding the one's which are already taken.

	:param board: The game board.
	:param pos: The [row, col] from which to calculate possible paths.
	:param visited: A 2d list containing a [row, col] for indexes 
		which are already visited describing the position they were visited
		from and False for unvisited indexes.
	:returns: A list containing the [row, col] of the possible direction
		to proceed in.

	"""
	[row, col] = pos
	totalRows = totalColumns = len(board)
	paths = []
	if col != 0:
		if visited[row][col-1] == False \
		and hasSoldierOrDiamond(board[row][col-1]):
			paths.append([row, col-1])
	if row != totalRows - 1:
		if visited[row+1][col] == False \
		and hasSoldierOrDiamond(board[row+1][col]):
			paths.append([row + 1, col])
	if col != totalColumns - 1:
		if visited[row][col+1] == False \
		and hasSoldierOrDiamond(board[row][col+1]):
			paths.append([row, col+1])
	if row != 0:
		if visited[row-1][col] == False \
		and hasSoldierOrDiamond(board[row-1][col]):
			paths.append([row-1, col])
	return paths

def getMusketeerAndDiamondPositions(board):
	""" Return the position of musketeers and diamond on the game board.

	:param board: The game board.
	:return: A tuple containing a list of muskeeter positions and [row, col]
		for the diamond position.

	"""
	muskeeterPositions = []
	diamondPosition = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 1:
				muskeeterPositions.append([i,j])
			elif board[i][j] == DIAMOND:
				diamondPosition = [i, j]
	return (muskeeterPositions, diamondPosition)

def getShortestPath(visited,  musketeerPosition, diamondPosition):
	""" Return shortest path from diamondPosition to musketeerPosition.

	This essentially backtraces from diamondPosition to musketeerPosition
	using the visited list.

	:param visited: The visited 2d list
	:param musketeerPosition: The [row, col] of musketeer on the board.
	:param diamondPosition: The [row, col] of the found diamond on the board. 
	:returns: A list containing the shortest path from musketeer's position
		to diamond's position.

	-- note::
		This should only be called if diamond is found else it might get stuck
		for time and beyond.

	"""
	shortestPath = []
	[x, y] = diamondPosition
	shortestPath.append([x, y])
	while [x, y] != musketeerPosition:
		[x, y] = visited[x][y]
		shortestPath.append([x, y])

	# Since we backtrace from the diamond's position to muskeeter position,
	# we need to reverse the list to return the path from muskeeter to diamond.
	return shortestPath[::-1]

def hasSoldierOrDiamond(thing):
	return (thing == SOLDIER or thing == DIAMOND)


class NoMusketeerFound(Exception):
    pass

class NoDiamondFound(Exception):
	pass

# board = [
# 			[0, 2, 2, 2, 1],
# 			[2, 2, 2, 0, 2],
# 			[2, 1, 0, 3, 2],
# 			[2, 2, 0, 2, 2],
# 			[1, 2, 2, 2, 0]
# 		]

# singleAgentSearch(board)