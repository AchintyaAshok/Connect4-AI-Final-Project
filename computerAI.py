from state import *
import copy
import sys
import random


class ComputerPlayer:
	''' This is the Computer AI ''' 

	def __init__(self):
		print "Constructing the AI!"
		self.maxPlayer = Marking.ComputerPlayer	# we are trying to maximize the utility of the computer
		self.minPlayer = Marking.User

	''' This method make the computer calculate a move that it wishes to perform_move
	given a board configuration. The method returns the next state of the board once the
	computer has made a move. ''' 
	def perform_move(self, currentState):
		state = copy.deepcopy(currentState) # do not modify the original state
		print "Old Utility: ", self.__getUtility(state)
		bestMove = self.__minimaxDecision(state)
		state.addMarking(Marking.Computer, bestMove)
		print "New Utility: ", self.__getUtility(state)
		return state

	''' Given an initial state of the board configuration, this computes the action (a 
	x,y coordinate pair) that the AI will perform. This method returns a tuple of the 
	desired coordinate pair. This method will use the minimax algorithm to compute the decision.
	If alpha and beta values are provided, it will compute a decision using the alpha-beta algorithm.'''
	def __minimaxDecision(self, initialState):
		# returns the action that needs to be performed. A set of coordinates.
		# utility = self.__getUtility(initialState)
		# print "Original Utility: ", utility

		# # let's randomly pick a move to make for testing purposes:
		# possible = initialState.getAllPossibleMoves()
		# moveToMake = possible[random.randint(0, len(possible)-1)]
		# print "Will play this move: ", moveToMake
		# return moveToMake

		# return the best move we can make assuming the opponent is minimizing your utility:
		# apply all the actions to the state, return the one that gives you the highest utility
		playableMoves = initialState.getAllPossibleMoves()
		bestMove = None
		highestUtil = -1 * sys.maxint
		for move in playableMoves:
			nextPossibleState = copy.deepcopy(initialState)
			nextPossibleState.addMarking(Marking.Computer, move)	# the computer is the max player
			currUtil = self.__minimum(nextPossibleState)
			if currUtil > highestUtil:
				bestMove = move
				highestUtil = currUtil

		return bestMove

	def __minimum(self, state, alpha = None, beta = None):
		print "finding min"
		goalCheck = state.checkForGoalState()
		# terminal test
		if goalCheck[0]:
			if goalCheck[1] == Marking.Computer:
				return sys.maxint
			elif goalCheck[1] == Marking.User:
				return -1*sys.maxint
			else:
				return 0

		v = sys.maxint
		#stateToReturn = None
		# apply each action to the state that is possible and find the maximum of that
		playableMoves = state.getAllPossibleMoves()
		for move in playableMoves:
			newState = copy.deepcopy(state)
			newState.addMarking(self.minPlayer, move)	# perform the move for the min player, the user
			util = self.__maximum(newState)
			if util < v:	v = util
				#stateToReturn = newState

		return v
		#return stateToReturn

	def __maximum(self, state, alpha = None, beta = None):
		print "finding max"
		goalCheck = state.checkForGoalState()
		# terminal test
		if goalCheck[0]:
			if goalCheck[1] == Marking.Computer:
				return sys.maxint
			elif goalCheck[1] == Marking.User:
				return -1*sys.maxint
			else:
				return 0

		v = -1 * sys.maxint
		#stateToReturn = None
		# apply each action to the state that is possible and find the maximum of that
		playableMoves = state.getAllPossibleMoves()
		for move in playableMoves:
			newState = copy.deepcopy(state)
			newState.addMarking(self.maxPlayer, move)	# perform the move for the computer
			util = self.__minimum(newState)
			if util > v:	v = util
				#stateToReturn = newState

		return v
		#return stateToReturn

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
	Returns a Utility value for a state from the Computer's Perspective
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
		for colInd in range(state.getNumberColumns()):
			# start from the left of the matrix and iterate to the right checking each column
			topPtr = state.getNumberRows()-1 # start from the top of the column
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

		# CHECK THE DIAGONALS
		for rowInd in range(state.getNumberRows()-1, -1, -1):
			# start from the topmost row and work our way down
			# keep track of left and right pointers because we check from either corner of the row
			
			if rowInd < 3:	break # we need at least 4 elements of height for the diagonal

			leftPtr = 0
			rightPtr = len(matrix[rowInd]) - 1 # start from the right end of the row

			while (state.getNumberColumns() - 1 - leftPtr >= 3):
				# we need to have at least 4 columns for our diagonal to be 4 elements in width
				# thus, we stop when we have less than 4
				# move our left pointer rightwards and our right pointer leftwards in the row
				stoppedCheckingLeft = stoppedCheckingRight = False # if we have X and O in our diagonal, don't count it
				numUserLeft = numUserRight = numCompLeft = numCompRight = 0	# number of X's and O's in the diagonals
				#print "starting at row ", rowInd, "left column => ", leftPtr, "right column => ", rightPtr
				for i in range(4):
					leftYPos = rowInd - i
					rightYPos = rowInd - i
					# check the left
					leftElem = matrix[leftYPos][leftPtr + i]
					if leftElem == Marking.Computer:
						if numUserLeft > 0:
							numUserLeft = numCompLeft = 0
							stoppedCheckingLeft = True
						else:
							numCompLeft += 1
					elif leftElem == Marking.User:
						if numCompLeft > 0:
							numUserLeft = numCompLeft = 0
							stoppedCheckingLeft = True
						else:
							numUserLeft += 1

					rightElem = matrix[rightYPos][rightPtr - i]
					if rightElem == Marking.Computer:
						if numUserRight > 0:
							numUserRight = numCompRight = 0
							stoppedCheckingRight = True
						else:
							numCompRight += 1
					elif rightElem == Marking.User:
						if numCompRight > 0:
							numUserRight = numCompRight = 0
							stoppedCheckingRight = True
						else:
							numUserRight += 1

					#print "Left Elem: ", leftElem, "Right Elem: ", rightElem

					if stoppedCheckingLeft and stoppedCheckingRight:	break	# if we're checking neither loop, stop
				
				if not stoppedCheckingLeft:
					#print "adding some left thing!"
					if numCompLeft > 0:		numConsecutive[numCompLeft - 1] += 1
					elif numUserLeft > 0:	numConsecutiveUser[numUserLeft - 1] += 1
				if not stoppedCheckingRight:
					#print "adding some right thing!"
					if numCompRight > 0:	numConsecutive[numCompRight - 1] += 1
					elif numUserRight > 0:	numConsecutiveUser[numUserRight - 1] += 1

				leftPtr += 1
				rightPtr -= 1


			# colInd gets incremented, and we check the next column. The bottom and top pointers are reset
			

		# now we calculate our utility using our evaluation function
		stateUtil = 0
		for i in range(len(numConsecutive)):
			stateUtil += (i+1) * numConsecutive[i]
			stateUtil -= (i+1) * numConsecutiveUser[i]

		#print "Utility of State", stateUtil
		return stateUtil
