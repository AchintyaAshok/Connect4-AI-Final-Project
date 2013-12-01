from state import *
from computerAI import ComputerPlayer
import copy

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


def main():
	play_game()
	# newState = State()
	# print newState

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
	# newState.addMarking(Marking.User, 0, 0)
	# newState.addMarking(Marking.User, 1, 1)
	# newState.addMarking(Marking.User, 3, 1)
	# newState.addMarking(Marking.Computer, 1, 0)
	# newState.addMarking(Marking.Computer, 2, 0)
	# newState.addMarking(Marking.Computer, 4, 3)
	# newState.checkForGoalState()
	# print newState

main()	