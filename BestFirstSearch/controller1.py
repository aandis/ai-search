import heapq

EMPTY = 0
MUSKEETER = 1
SOLDIER = 2
DIAMOND = 3

class Node(object):
	""" Represent a node on the game board.
	"""
	def __init__(self, position, val):
		""" Initalize a node.

		:param position: [row, col] describing a position on the board.
		:param val: Heuristic value from the position to goal.

		"""
		super(Node, self).__init__()
		self.position = position
		self.val = val

	def __cmp__(self, other):
		""" Method used by heapq to insert values into heap.
		"""
		return cmp(self.val, other.val)

def singleAgentSearch(board):
	""" Wrapper method for bestFirstSearch which calls bestFirstSearch for 
	each musketeer on the board and keeps track of the one which
	finds the diamond in shortest number of steps.

	:param board: The square game board which is a 2d list of integers.
	:returns: A tuple containing exploredNodes, searchQueue and the shortestPath
		corresponding to the musketeer which finds the diamond in the shortest 
		number of steps.

	"""
	exploredNodes = []
	searchQueue  = []
	shortestPath = []

	(musketeerPositions, diamondPosition) = getMusketeerAndDiamondPositions(board)
	if len(musketeerPositions) == 0:
		raise MusketeerNotFound

	if len(diamondPosition) == 0:
		raise DiamondNotFound

	for i in range(len(musketeerPositions)):
		(newExploredNodes, newSearchQueue, newShortestPath) = \
			bestFirstSearch(board, musketeerPositions[i], diamondPosition)

		if  shortestPath == [] \
		or  (
				len(newShortestPath) < len(shortestPath) \
				and len(newShortestPath) > 0
			):
			(exploredNodes, searchQueue, shortestPath) = \
				(newExploredNodes, newSearchQueue, newShortestPath)

	return (exploredNodes,searchQueue,shortestPath)

def bestFirstSearch(board, musketeerPosition, diamondPosition):
	""" Perform a best first search on the game board.

	:param board: The game board.
	:param musketeerPosition: The [row, col] of musketeer on the board.
	:param diamondPosition: The [row, col] of diamond on the board.
	:returns: A tuple containing exploredNodes, searchQueue, shortestPath.

	"""
	totalRows = totalColumns = len(board)
	exploredNodes, searchQueue, iterativeSearchQueue, shortestPath = [],[],[],[]
	# List of nodes visited and the position from which they were visited.
	# Used for calculating shortest path.
	visited = [[False for i in range(totalRows)] for i in range(totalColumns)]
	goalFound = False

	musketeerNode = Node(
		musketeerPosition,
		getHeuristicValue(musketeerPosition, diamondPosition)
	)
	heapq.heappush(searchQueue, musketeerNode)
	while len(searchQueue) != 0:
		[row, col] = heapq.heappop(searchQueue).position
		exploredNodes.append([row, col])
		if board[row][col] == DIAMOND:
			# Diamong found! Append the remaining queue as part of this
			# iteration and break.
			goalFound = True
			iterativeSearchQueue.append(getSortedQueue(searchQueue))
			break
		# Add all unvisited paths to heap queue.
		paths = numberOfPaths(board, [row, col], visited)
		for path in paths:
			heuristicVal = getHeuristicValue(path, diamondPosition)
			heapq.heappush(searchQueue, Node(path, heuristicVal))
			visited[path[0]][path[1]] = [row, col]

		iterativeSearchQueue.append(getSortedQueue(searchQueue))
	if goalFound:
		shortestPath = getShortestPath( visited,
										musketeerPosition, 
										diamondPosition)
	return (exploredNodes, iterativeSearchQueue, shortestPath)

def getSortedQueue(queue):
	""" Return the heap queue as a sorted list.

	:param queue: The heap queue.
	:return: A list of positions in the queue sorted on their heuristic value.

	-- note::
		This method uses a hack presently to get a list of sorted values
		from the heap queue which isn't necessarly optimal. It essentially
		fetches the n smallest element from the queue where n is the
		length of the queue.

	"""
	sortedNodeQueue = heapq.nsmallest(len(queue), queue)
	sortedQueue = [node.position for node in sortedNodeQueue]
	return sortedQueue

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


class MusketeerNotFound(Exception):
    pass

class DiamondNotFound(Exception):
	pass

# board = [
# 			[0, 2, 2, 2, 1],
# 			[2, 2, 2, 0, 2],
# 			[2, 1, 0, 3, 2],
# 			[2, 2, 0, 2, 2],
# 			[1, 2, 2, 2, 0]
# 		]

# singleAgentSearch(board)