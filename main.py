from state import *
from computerAI import ComputerPlayer
import copy
import sys

'''	Gets user input for the move he wishes to play on the board . The function keeps polling for a response until 
the user gives valid input for the given board configuration. ''' 
def get_user_input():
	user_input = []
	while(True):
		x = int(raw_input("Welcome. Please give an x position for the move you desire to make:\t"))
		y = int(raw_input("Give the y position for the move you desire to make:\t"))
		if x not in range(NUM_COLUMNS) or y not in range(NUM_ROWS):
			print "Incorrect Input. Please make sure your X value is in the range: 0 .. ", (NUM_COLUMNS-1)
			print "Please make sure your Y value is in the range: 0 .. ", (NUM_ROWS-1)
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

	while(True):
		print "=== Round ", numberOfMoves, " ==="
		print currentState
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

		testGoalState = currentState.checkForGoalState() # check to see if we've reached a goal state
		if testGoalState[0]:
			print "The Game is finished!"
			if testGoalState[1] == Marking.User:	print "You Won!"
			else:									print "The Computer Won!"
			break
		elif currentState.numberOfPossibleMoves() == 0:	# check to see if it's a draw
			print "The Game resulted in a draw! There is no winner."
			break

		numberOfMoves += 1
		# control-test, remove this 
		if numberOfMoves > 4: break

	print "States in Succession:\n"
	for i in range(len(states)):
		print (i+1), "->\n", states[i]


def utility(state):
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
	# s = State()
	# print s
	# s.addMarking(Marking.User, 0, 0)
	# s.addMarking(Marking.User, 1, 0)
	# s.addMarking(Marking.User, 2, 0)
	# s.addMarking(Marking.Computer, 4, 0)
	# s.addMarking(Marking.Computer, 5, 0)
	# s.addMarking(Marking.Computer, 6, 0)
	# print s
	# utility(s)

	# s2 = State()
	# print s2
	# s2.addMarking(Marking.Computer, 0, 0)
	# s2.addMarking(Marking.Computer, 1, 0)
	# s2.addMarking(Marking.Computer, 3, 0)
	# s2.addMarking(Marking.Computer, 4, 0)
	# print s2
	# utility(s2)

	play_game()
	newState = State()
	print newState

	# -- testing horizontal check
	# newState.addMarking(Marking.Computer, 0, 0)
	# newState.addMarking(Marking.User, 1, 0)
	# newState.addMarking(Marking.User, 2, 0)
	# newState.addMarking(Marking.User, 3, 0)
	# newState.addMarking(Marking.User, 4, 0)

	# -- testing vertical check
	# newState.addMarking(Marking.User, 0, 0)
	# newState.addMarking(Marking.User, 0, 1)
	# newState.addMarking(Marking.User, 0, 2)
	# newState.addMarking(Marking.User, 0, 3)

	# Testing Diagonals 1
	# newState.addMarking(Marking.User, 0, 0)
	# newState.addMarking(Marking.User, 1, 1)
	# newState.addMarking(Marking.User, 2, 2)
	# newState.addMarking(Marking.User, 3, 3)
	# newState.addMarking(Marking.Computer, 0, 3)
	# newState.addMarking(Marking.Computer, 1, 2)
	# newState.addMarking(Marking.Computer, 2, 1)
	# newState.addMarking(Marking.Computer, 3, 0)

	# Testing Diagonals 2
	newState.addMarking(Marking.User, 0, 0)
	newState.addMarking(Marking.User, 1, 1)
	newState.addMarking(Marking.User, 3, 1)
	newState.addMarking(Marking.Computer, 1, 0)
	newState.addMarking(Marking.Computer, 2, 0)
	newState.addMarking(Marking.Computer, 4, 3)
	newState.checkForGoalState()
	print newState

main()	