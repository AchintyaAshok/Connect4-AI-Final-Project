from state import *
import copy
import sys


class ComputerPlayer:
	''' This is the Computer AI ''' 

	def __init__(self):
		print "Constructing the AI!"

	''' This method make the computer calculate a move that it wishes to perform_move
	given a board configuration. The method returns the next state of the board once the
	computer has made a move. ''' 
	def perform_move(self, currentState):
		state = copy.deepcopy(currentState) # do not modify the original state
		moveCoordinates = self.__computeMinimaxDecision(state)
		state.addMarking(Marking.Computer, moveCoordinates['x'], moveCoordinates['y'])
		return state

	''' Given an initial state of the board configuration, this computes the action (a 
	x,y coordinate pair) that the AI will perform. This method returns a tuple of the 
	desired coordinate pair. This method will use the minimax algorithm to compute the decision.
	If alpha and beta values are provided, it will compute a decision using the alpha-beta algorithm.'''
	def __minimaxDecision(self, initialState):
		# returns the action that needs to be performed. A set of coordinates.
		print "doing minimax"

	def __minimum(self, state, alpha = None, beta = None):
		print "min"

	def __maximum(self, state, alpha = None, beta = None):
		print "max"

	''' This method returns the utility from the perspective of the computer, given a state. 
	The utility for a terminal winning state is +infinity. The utility for a losing terminal state
	is -infinity. The utility for all other terminal states (that end in a draw) is 0. 

	Finally, utility for non terminal states is computed using a linear evaluation function:
		Eval(s) = 3(X3) + 2(X2) + X1 - (3(O3) + 2(O2) + O1) -- In this example, the computer plays X.
	Winning/Losing states are when there are 4 x's in a row.

	If we need at least 4 in a row to win, a given row, column or diagonal should have enough empty
	spaces such that a player can win by placing consecutive markings. 

	For example, X O O O _ X -> in this row, we can place another O to win the game.
	If it is like this, O O O X X X, there is no purpose in counting the 3 O's, there is no way to win.

	'''
	def __getUtility(self, state):
		ended = state.checkForGoalState()
		if ended[0]: 
			if ended[1] == Marking.Computer: # if the game has ended & the computer has won
				return sys.maxint 			# our simulated +infinity
			elif ended[1] == Marking.User:
				return (-1 * sys.maxint) 	# simulated -infinity
			else:
				return 0 # the game has ended and it's a draw
		
		matrix = state.getMatrix()	# get a copy of the state's matrix, so that we don't modify it

		numConsecutive = [0, 0, 0] # we can have up to 3 in a row. 4 in a row and the state has already ended.
		numConsecutiveUser = [0, 0, 0]

		# CHECK THE ROWS
		# consecutively checks a 4 element range of markings to see if any patterns can be made. It iterates
		# through rows in the matrix.
		for colInd in range(len(matrix)):
			# keep track of elements between a range of 4. We see what combinations can be made between them.
			leftPtr = 0
			rightPtr = 3
			while (rightPtr < len(matrix[colInd])):
				numComp = numUser = 0
				stoppedChecking = False
				for i in range(4):
				# start at the left pointer and iterate to the right
					if stoppedChecking:	break
					mark = matrix[colInd][leftPtr + i]
					if mark == Marking.Computer:
						if numUser > 0: # we have an X and an O in the interval, neither player wins
							numUser = numComp = 0
							stoppedChecking = True # break out of the loop
							break
						else:
							numComp += 1
							numUser = 0
					elif mark == Marking.User:	
						if numComp > 0: # we have an X and an O in the interval, neither player wins
							numUser = numComp = 0
							stoppedChecking = True # break out of the loop
							break	# if we have both user and computer markings in the row, neither can win
						else:	
							numUser += 1
							numComp = 0

				# indicate the number of markings in a row the user or computer accrued (for this section)
				if not stoppedChecking: 	# if this seciton wasn't stopped check because of X's and O's, 
											# a player has a chance of winning and we record it
					if numComp > 0:		numConsecutive[numComp - 1] += 1
					elif numUser > 0: 	numConsecutiveUser[numUser - 1] += 1

				# check next 4 consecutive spots, shift the interval rightwards
				leftPtr += 1
				rightPtr += 1

		# CHECK THE COLUMNS
		for colInd in range(state.numColumns()):
			# start from the left of the matrix and iterate to the right checking each column
			topPtr = state.numRows()-1 # start from the top of the column
			btmPtr = topPtr - 3

			while (topPtr >= 3):
				# we need at least 4 indicies to check for a 4 in a row
				numComp = numUser = 0
				stoppedChecking = False
				for i in range(4):
					# check each of the marks in our 4 elements from top to bottom
					mark = matrix[colInd][topPtr - i]
					if mark == Marking.Computer:
						if numUser > 0:
							numUser = numComp = 0
							stoppedChecking = True
							break
						else:
							numComp += 1
					elif mark == Marking.User:
						if numComp > 0:
							numComp = numUser = 0
							stoppedChecking = True
							break
						else:
							numUser += 1

				if not stoppedChecking:
					# if we weren't prematurely halted when checking our 4 element range because
					# there are both user and computer markings, we update our arrays with the
					# number of consecutive markings that exist in that row for either user
					if numComp > 0:		numConsecutive[numComp - 1] += 1
					elif numUser > 0:	numConsecutiveUser[numUser - 1] += 1

				topPtr -= 1
				btmPtr -= 1

			# colInd gets incremented, and we check the next column. The bottom and top pointers are reset


			


