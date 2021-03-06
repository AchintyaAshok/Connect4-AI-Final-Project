import copy
from enum import Enum

NUM_ROWS = 4
NUM_COLUMNS = 5

class Marking(Enum):
	User = 'O'
	Computer = 'X'
	Empty = '_'

class State:
	matrix = []
	possibleMoves = 0
	numColumns = 0
	numRows = 0

	def __init__(self):
		for x in range(0, NUM_ROWS):
			row = [] # add a new row
			for i in range(0, NUM_COLUMNS):
				row.append(Marking.Empty)
			self.matrix.append(row)

		self.possibleMoves = NUM_COLUMNS*NUM_ROWS
		self.numColumns = int(NUM_COLUMNS)
		self.numRows = int(NUM_ROWS)

	def getNumberRows(self):
		return self.numRows

	def getNumberColumns(self):
		return self.numColumns

	''' Override of the deep copy constructor for the class. This ensures that references are not made
	to mutable types inside this class when the deepcopy constructor is invoked. That way the state that
	is being copied remains preserved. ''' 
	def __deepcopy__(self, memo):
		newState = State()
		newState.matrix = copy.deepcopy(self.matrix)
		newState.possibleMoves = self.possibleMoves
		newState.numRows = self.numRows
		newState.numColumns = self.numColumns
		return newState

	''' checks the position indexed by (x, y). If the position is out of range, the 
	method will return false, otherwise the marking in that position.'''
	def getMarking(self, x, y):
		if x in range(0, NUM_COLUMNS) and y in range(0, NUM_ROWS):
			return self.matrix[y][x]
		else: 
			return False

	def addMarking(self, mark, x, y):
		if self.possibleMoves == 0 or x not in range(0, NUM_COLUMNS) or y not in range(0, NUM_ROWS):
			return False
		elif self.matrix[y][x] != Marking.Empty:
			return False

		self.matrix[y][x] = mark
		self.possibleMoves -= 1
		return True # indicate that the move was sucessfully made

	''' Accepts a hash containing the location '''
	def addMarkingWithHash(self, mark, locationHash):
		x = locationHash['x']
		y = locationHash['y']
		return self.addMarking(mark, x, y)

	''' Returns whether a space on the Grid is occupied. If the space is occupied by a move (the User's
		or the Computer), the method will return True. If the space is unoccupied or the move is invalid
		because of out-of-range coordinates, the method returns False.'''
	def isOccupied(self, x, y):
		if x not in range(NUM_COLUMNS-1) or y not in range(NUM_ROWS-1):	return False
		if self.matrix[y][x] == Marking.Empty:	return True # if the space is unoccupied, return True
		else:									return False

	''' Returns the number of possible moves left available on the board ''' 
	def numberOfPossibleMoves(self):
		return self.possibleMoves

	''' Returns a list of all the possible coordinates that a move can be played on. '''
	def getAllPossibleMoves(self):
		moves = []
		for y in range(self.numRows):
			for x in range(self.numColumns):
				if self.matrix[y][x] == Marking.Empty:
					coordinate = {'x': x, 'y': y}
					moves.append(coordinate)
		return moves

	def checkForGoalState(self):
		''' This method checks if the state is in a goal state. It will return a list containing
		2 parameters. The first parameter will be a true/false value indicating if it is in a goal state
		and the second parameter will indicate the winning marking. 
		If, for example, the User has won, the method will return [True, 'X']. 
		If the computer has won, the method will return [True, 'O']
		and if nobody has won the method returns [False, '__'].'''

		# we need to check for horizontal, diagonal and vertical goal states. 
		horizontalCheck = self.__checkHorizontal()
		if horizontalCheck[0]:
			return horizontalCheck
		verticalCheck = self.__checkVertical()
		if verticalCheck[0]:
			return verticalCheck
		diagonalCheck = self.__checkDiagonal()
		if diagonalCheck[0]:
			return diagonalCheck

		return [False, Marking.Empty]

	def __checkHorizontal(self):
		numbX = 0 # keep track of the number of consecutives X's
		numbO = 0 # number of consecutives O's
		for row in self.matrix:
			for elem in range(0, len(row)):
				marking = row[elem]
				if marking == Marking.User:
					numbX += 1
					numbO = 0
				elif marking == Marking.Computer:
					numbO += 1
					numbX = 0
				else:
					numbO = numbX = 0
	
				# now check if numbO or numbX indicate 4 in a row were found
				if numbX == 4:
					return [True, Marking.User]
				elif numbO == 4:
					return [True, Marking.Computer]

			numbX = numbO = 0	# reset the values for the next row

		return [False, Marking.Empty]	# no four in a row were found

	def __checkVertical(self):
		for colIndex in range(self.numColumns):
			rowIndex = self.numRows - 1
			if rowIndex < 3:	break

			while rowIndex >= 3:	
				stoppedCheckingColumn = False
				numUser = numComp = 0

				for i in range(4):
					# we need at least 4 elements to check
					mark = self.matrix[rowIndex - i][colIndex]
					if mark == Marking.User:
						if numComp > 0:
							numUser = numComp = 0
							stopCheckingColumn = True
							break
						else:
							numUser += 1
					elif mark == Marking.Computer:
						if numUser > 0:
							numComp = numUser = 0
							stopCheckingColumn = True
							break
						else:
							numComp += 1

				if not stoppedCheckingColumn:
					if numUser == 4:
						return [True, Marking.User]
					elif numComp == 4:
						return [True, Marking.Computer]

				rowIndex -= 1

		return [False, Marking.Empty]

	def __checkDiagonal(self):
		#print "checking diagonal"
		# for diagonal checks, we only need to begin checking at y positions that are greater
		# than or equal to 4, because we need to descend diagonally that amount to find a goal
		# Example: 	X - - - - 
		#			- X - - -
		#			- - X - -
		#			- - - X - 
		# Here the starting Y position must be at least 4 and our amount of descent needed must not exceed
		# the amount of x positions we can possibly traverse in our graph
		rowIndexLeft = 0
		rowIndexRight = NUM_COLUMNS - 1
		numbXLeft = 0
		numbOLeft = 0
		numbORight = 0
		numbXRight = 0
		for yPosition in (NUM_ROWS - 1, 3, -1): # we only decrement down to 3 because we need 
													# marked items in y positions 3, 2, 1, 0 
			# check left to right diagonals
			if (NUM_COLUMNS - rowIndexLeft >= 4):	# we need at least 4 horizontal slots 
				localX = rowIndexLeft
				localY = yPosition
				mark = self.getMarking(localX, localY)
				while(mark):
					if mark == Marking.User:
						numbXLeft += 1
						numbOLeft = 0
					elif mark == Marking.Computer:
						numbOLeft += 1
						numbXLeft = 0
					else:
						numbXLeft = numbOLeft = 0

					if numbXLeft >= 4: return [True, Marking.User]
					if numbOLeft >= 4: return [True, Marking.Computer]

					# traverse right -> x+1 and down -> y-1 to the next cell
					localX += 1 
					localY -= 1
					mark = self.getMarking(localX, localY)

			# check right to left diagonals
			if (rowIndexRight >= 3):
				localX = rowIndexRight
				localY = yPosition
				mark = self.getMarking(localX, localY)
				while(mark):
					mark = self.getMarking(localX, localY)
					if mark == Marking.User:
						numbXRight += 1
						numbORight = 0
					elif mark == Marking.Computer:
						numbORight += 1
						numbXRight = 0
					else:
						numbXRight = numbORight = 0

					if numbXRight >= 4: return [True, Marking.User]
					if numbORight >= 4: return [True, Marking.Computer]

					# traverse down and right to the next cell
					localX -= 1 
					localY -= 1
					mark = self.getMarking(localX, localY)

			rowIndexLeft += 1
			rowIndexRight -= 1
			numbXLeft = numbOLeft = numbXRight = numbORight = 0 #reset all our counters for the next row

		return [False, Marking.Empty]

	''' Returns a copy of the matrix describing the state of the game ''' 
	def getMatrix(self):
		return copy.deepcopy(self.matrix)

	def __str__(self):
		board = ""
		for rowIndex in range(NUM_ROWS - 1, -1, -1):
			rowStr = str(self.matrix[rowIndex])
			board += str(rowIndex) + " " + rowStr + "\n"

		xIndexStr = "   "
		prefix = ""
		for i in range(NUM_COLUMNS):
			xIndexStr += prefix + " " + str(i) + " "
			prefix = "  "
		xIndexStr += " "
		board += xIndexStr	
		return board



