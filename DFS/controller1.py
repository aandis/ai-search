
EMPTY = 0
MUSKEETER = 1
SOLDIER = 2
DIAMOND = 3

def singleAgentSearch(board):
	""" Wrapper function for dfsSearch which calls dfsSearch for 
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

	musketeerPositions = getMusketeerPositions(board)
	if len(musketeerPositions) == 0:
		print "Where are my musketeers? How do I play? ANSWER ME!"
		return

	# (exploredNodes, searchQueue, shortestPath) = \
	# 	dfsSearch(board, musketeerPositions[0])
	for i in range(len(musketeerPositions)):
		(newExploredNodes, newSearchQueue, newShortestPath) = \
			dfsSearch(board, musketeerPositions[i])

		if  shortestPath == [] \
		or  (
				len(newShortestPath) < len(shortestPath) \
				and len(newShortestPath) > 0
			):
			(exploredNodes, searchQueue, shortestPath) = \
				(newExploredNodes, newSearchQueue, newShortestPath)

	return (exploredNodes,searchQueue,shortestPath)

def dfsSearch(board, musketeerPosition):
	""" Perform a dfs search on the game board.

	:param board: The game board.
	:param musketeerPosition: The [row, col] of musketeer on the board.
	:returns: A tuple containing exploredNodes, searchQueue, shortestPath.

	"""
	totalRows = totalColumns = len(board)
	exploredNodes, searchQueue, iterativeSearchQueue, shortestPath = [],[],[],[]
	# List of nodes visited and the position from which they were visited.
	# Used for calculating shortest path.
	visited = [[False for i in range(totalRows)] for i in range(totalColumns)]
	goalFound = False

	searchQueue.append(musketeerPosition)
	while len(searchQueue) != 0:
		[row, col] = searchQueue[0]
		exploredNodes.append([row, col])
		# Since we can end up adding a node to the queue multiple times,
		# we should remove all occurrences of the node as soon as it
		# is explored.
		searchQueue = [x for x in searchQueue if x != [row, col]]
		if board[row][col] == DIAMOND:
			# Diamong found! Append the remaining queue as part of this
			# iteration and break.
			goalFound = True
			iterativeSearchQueue.append(searchQueue[:])
			break
		neighbours = []
		if col != 0: # Left
			if (hasSoldierOrDiamond(board[row][col-1]) 
			and [row, col-1] not in exploredNodes):
				neighbours.append([row, col-1])
				visited[row][col-1] = [row, col]
		if row != totalRows - 1: # Down
			if (hasSoldierOrDiamond(board[row+1][col]) 
			and [row+1, col] not in exploredNodes):
				neighbours.append([row+1, col])
				visited[row+1][col] = [row, col]
		if col != totalColumns - 1: # Right
			if (hasSoldierOrDiamond(board[row][col+1]) 
			and [row, col+1] not in exploredNodes):
				neighbours.append([row, col+1])
				visited[row][col+1] = [row, col]
		if row != 0: # Up
			if (hasSoldierOrDiamond(board[row-1][col]) 
			and [row-1, col] not in exploredNodes):
				neighbours.append([row-1, col])
				visited[row-1][col] = [row,col]

		# Append to the front of the queue
		searchQueue = neighbours + searchQueue
		iterativeSearchQueue.append(searchQueue[:])

	if goalFound:
		shortestPath = getShortestPath(visited, musketeerPosition, [row, col])
		b = getShortestPathRecursive(visited, musketeerPosition, [row, col])
		assert shortestPath == b # becuase why not?

	return (exploredNodes, iterativeSearchQueue, shortestPath)

def getShortestPath(visited,  musketeerPosition, diamondPosition):
	""" Return shortest path from diamondPosition to musketeerPosition.
	We essentially backtrace from diamondPosition to musketeerPosition
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

def getShortestPathRecursive(visited, musketeerPosition, diamondPosition):
	""" Recursive version of getShortestPath.

	:param visited: The visited 2d list
	:param musketeerPosition: The [row, col] of musketeer on the board.
	:param diamondPosition: The [row, col] of the found diamond on the board. 
	:returns: A list containing the shortest path from musketeer's position
		to diamond's position.

	-- note::
		This should only be called if diamond is found else it will get
		stuck and only stop in the year 3052 which as we all know, is doomsday. 
		Stopping this function would be the least of your worries by then. 
		Hopefully.

	"""
	[x, y] = diamondPosition
	if [x, y] == musketeerPosition:
		return [[x, y]]
	b = getShortestPathRecursive(visited, musketeerPosition, visited[x][y])
	return b + [[x, y]]

def getMusketeerPositions(board):
	positions = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 1:
				positions.append([i,j])
	return positions

def hasSoldierOrDiamond(thing):
	return (thing == SOLDIER or thing == DIAMOND)

# board = [
# 			[0, 2, 2, 2, 1],
# 			[2, 2, 2, 0, 2],
# 			[2, 1, 0, 3, 2],
# 			[2, 2, 0, 2, 2],
# 			[1, 2, 2, 2, 0]
# 		]

# singleAgentSearch(board)