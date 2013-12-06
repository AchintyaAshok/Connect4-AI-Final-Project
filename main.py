from state import *
from computerAI import ComputerPlayer
import copy
import sys

'''	Gets user input for the move he wishes to play on the board . The function keeps polling for a response until 
the user gives valid input for the given board configuration. ''' 
def get_user_input():
	user_input = []
	while(True):
		xVal = raw_input("X Position:\t")
		yVal = raw_input("Y Position:\t")
		try:
			x = int(xVal)
			y = int(yVal)
		except:
			print "Please enter integer values for x and y."
			continue
		if x not in range(NUM_COLUMNS) or y not in range(NUM_ROWS):
			print "Invalid Values!"
			print "X has to be in the range: 0 .. ", (NUM_COLUMNS-1)
			print "Y has to be in the range: 0 .. ", (NUM_ROWS-1)
		else:	
			user_input = {"x": x, "y": y}
			return user_input
			
	
''' This function performs a User Move on the board. The function accepts a state and returns the next
state once the user's valid action has been performed. '''
def perform_user_move(BoardState):
	nextState = copy.deepcopy(BoardState)
	while(True):
		# attempt to add it to the board. If the space is occupied, notify the user.
		userMove = get_user_input()
		userX = userMove["x"]
		userY = userMove["y"]
		print "You chose to play -> (", userX, ", ", userY, ")"
		addedToBoard = nextState.addMarking(Marking.User, userX, userY)
		if addedToBoard:
			print "Added your mark to the board!"
			return nextState
		else:
			print "That spot is occupied! Please Try Again."


''' Simulates a game by alternating play between a user and the computer AI'''
def play_game():
	initialState = State()
	currentState = copy.deepcopy(initialState)
	numberOfMoves = 0
	isUserTurn = True # keep track of whose turn it is
	states = []	
	states.append(currentState)

	comp = ComputerPlayer()
	print "Welcome to Connect 4! I hope you lose."
	while(True):
		print "=== Round ", numberOfMoves, " ==="
		print currentState

		testGoalState = currentState.checkForGoalState() # check to see if we've reached a goal state
		if testGoalState[0]:
			print "The Game is finished!"
			if testGoalState[1] == Marking.User:	print "You Won!"
			else:									print "The Computer Won!"
			break
		elif currentState.numberOfPossibleMoves() == 0:	# check to see if it's a draw
			print "The Game resulted in a draw! There is no winner."
			break

		if isUserTurn:
			# it is the User's turn, so we perform his/her move
			print "--USER TURN--"
			nextState = perform_user_move(currentState)
			states.append(nextState)
			currentState = nextState
			isUserTurn = False
		else:
			# it is the computer's turn. We simulate the computer's choice of move
			print "--COMPUTER TURN--"
			# DO SOMETHING
			nextState = comp.perform_move(currentState)
			states.append(nextState)
			currentState = nextState
			isUserTurn = True

		numberOfMoves += 1
		# control-test, remove this 
		#if numberOfMoves > 4: break

	# print "States in Succession:\n"
	# for i in range(len(states)):
	# 	print (i+1), "->\n", states[i]


def utility(state):
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
		topPtr = state.getNumberRows() - 1 # start from the top of the column
		btmPtr = topPtr - 3

		while (topPtr >= 3):
			# we need at least 4 indicies to check for a 4 in a row
			numComp = numUser = 0
			stoppedChecking = False
			for i in range(4):
				# check each of the marks in our 4 elements from top to bottom
				mark = matrix[topPtr - i][colInd]
				print "column", colInd, "saw this-> ", mark
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
				print "someone got some score!"
				if numComp > 0:		numConsecutive[numComp - 1] += 1
				elif numUser > 0:	numConsecutiveUser[numUser - 1] += 1

			topPtr -= 1
			btmPtr -= 1


	# CHECK DIAGONAL
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
			print "starting at row ", rowInd, "left column => ", leftPtr, "right column => ", rightPtr
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

				print "Left Elem: ", leftElem, "Right Elem: ", rightElem

				if stoppedCheckingLeft and stoppedCheckingRight:	break	# if we're checking neither loop, stop
			
			if not stoppedCheckingLeft:
				print "adding some left thing!"
				if numCompLeft > 0:		numConsecutive[numCompLeft - 1] += 1
				elif numUserLeft > 0:	numConsecutiveUser[numUserLeft - 1] += 1
			if not stoppedCheckingRight:
				print "adding some right thing!"
				if numCompRight > 0:	numConsecutive[numCompRight - 1] += 1
				elif numUserRight > 0:	numConsecutiveUser[numUserRight - 1] += 1

			leftPtr += 1
			rightPtr -= 1


		# colInd gets incremented, and we check the next column. The bottom and top pointers are reset
	
	print "User Score => ", numConsecutiveUser
	print "Comp Score => ", numConsecutive

	# now we calculate our utility using our evaluation function
	stateUtil = 0
	for i in range(len(numConsecutive)):
		stateUtil += (i+1) * numConsecutive[i]
		stateUtil -= (i+1) * numConsecutiveUser[i]

	print "Utility of State", stateUtil


def utility2(state):
	ended = state.checkForGoalState()
	if ended[0]: 
		if ended[1] == Marking.Computer: # if the game has ended & the computer has won
			return sys.maxint 			# our simulated +infinity
		elif ended[1] == Marking.User:
			return (-1 * sys.maxint) 	# simulated -infinity
		else:
			return 0 # the game has ended and it's a draw
	
	matrix = state.getMatrix()
	# rows, columns, diagonals that have x*, o* without any of the opposing markings
	x1, x2, x3, o1, o2, o3 = 0, 0, 0, 0, 0, 0

	numConsecutive = [0, 0, 0] # we can have up to 3 in a row. 4 in a row and the state has already ended.
	numConsecutiveUser = [0, 0, 0]

	for colInd in range(len(matrix)):
		if len(matrix[colInd]) < 4:	break	# if we have less than 4 spaces in a row, we shouldn't continue

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
					numComp += 1
					numUser = 0
				elif mark == Marking.User:	
					if numComp > 0: # we have an X and an O in the interval, neither player wins
						numUser = numComp = 0
						stoppedChecking = True # break out of the loop	
					numUser += 1
					numComp = 0

			# indicate the number of markings in a row the user or computer accrued (for this section)
			if stoppedChecking == False: 	# if this seciton wasn't stopped check because of X's and O's, 
								# a player has a chance of winning and we record it
				if numComp > 0:		numConsecutive[numComp - 1] += 1
				elif numUser > 0: 	numConsecutiveUser[numUser - 1] += 1

			# check next 4 consecutive spots, shift the interval rightwards
			leftPtr += 1
			rightPtr += 1

	print "User Consecs: ", numConsecutiveUser
	print "Comp Consecs: ", numConsecutive


def main():
	#s = State()
	#print s
	play_game()

	# s.addMarking(Marking.Computer, 0, 0)
	# s.addMarking(Marking.Computer, 1, 0)
	# s.addMarking(Marking.User, 2, 0)
	# s.addMarking(Marking.User, 3, 0)
	# s.addMarking(Marking.Computer, 4, 0)
	# s.addMarking(Marking.Computer, 0, 1)
	# s.addMarking(Marking.User, 3, 3)
	# play_game()

main()	