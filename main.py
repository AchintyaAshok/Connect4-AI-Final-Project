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
			print "Please enter numbers for x and y."
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

	print "You can choose a difficulty for your computer opponent. Pick (1, 2, 3) from easiest to hardest."
	print "Be careful! A smarter opponent will think farther ahead than you (and take more time to do so)! Choose Wisely"
	difficulty = 0
	while(True):
		difficulty = raw_input("Difficulty: ")
		try:
			difficulty = int(difficulty)
			if difficulty not in [1, 2, 3]:
				print "Please pick difficulty between 1 and 3!"
				continue
			break
		except:
			print "Choose a number value between 1 and 3!"

	comp = ComputerPlayer(difficulty)
	print "Welcome to Connect 4! You win the game by getting 4 in a row in any direction."
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
			nextState = comp.perform_move(currentState)
			states.append(nextState)
			currentState = nextState
			isUserTurn = True

		numberOfMoves += 1


def main():
	play_game()

main()	