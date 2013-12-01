class State_other:
	''' each state describes the state of the conenct 4 game. This means it will have
	have a 2 dimensional list (a grid) that describes the 4x5 game configuration. '''

	matrix = []

	def __init__(self):
		''' initialize the matrix with all empty markings '''
		for x in range(0, NUM_COLUMNS):
			newColumn = []
			for y in range(0, COLUMN_DEPTH):
				newColumn.append(Marking.Empty)
			self.matrix.append(newColumn)

		# we will have GRID_COLUMN_SIZE number of stacks in a list. This will represent each of the
		# places a player can insert a marking piece


	def addMarking(self, mark, columnNumber):
		''' adds a marking piece to a given slot. If the given column is full, the marking will not be
		added. If a slot number is our of range, [0...4], the marking will not be added. If a marking
		piece is successfully added, the method returns true or otherwise returns false. ''' 

		if columnNumber not in range(0, NUM_COLUMNS):
			return False

		for i in range(0, COLUMN_DEPTH):
			if self.matrix[columnNumber][i] == Marking.Empty:
				self.matrix[columnNumber][i] = mark
				return True

		return False

	def __str__(self):
		''' prints the currents state of the board '''

		# we iterate through every column. This means we need to iterate row by row, printing the element
		# in each column given that corresponding row number. 
		board = ""
		depthIndex = COLUMN_DEPTH - 1
		while depthIndex >= 0:
			rowStr = ""
			for colIndex in range(0, NUM_COLUMNS):
				rowStr +=  "[" + str(self.matrix[colIndex][depthIndex]) + "] "
			board += rowStr + "\n"
			depthIndex -= 1

		return board