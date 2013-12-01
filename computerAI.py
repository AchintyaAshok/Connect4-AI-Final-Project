from state import *
import copy


class ComputerPlayer:
	''' This is the Computer AI ''' 

	def __init__(self):
		print "Constructing the AI!"

	''' This method make the computer calculate a move that it wishes to perform_move
	given a board configuration. The method returns the next state of the board once the
	computer has made a move. ''' 
	def perform_move(self, currentState):
		initState = copy.deepcopy(currentState) # do not modify the original state
		nextState = self.__computeMinimaxDecision(initState)
		return nextState

	''' Given an initial state of the board configuration, this computes the action (a 
	x,y coordinate pair) that the AI will perform. This method returns a tuple of the 
	desired coordinate pair. This method will use the minimax algorithm to compute the decision.
	If alpha and beta values are provided, it will compute a decision using the alpha-beta algorithm.'''
	def __computeMinimaxDecision(self, initialState):
		

	def __minimum(self, state, alpha = None, beta = None):


	def __maximum(self, state, alpha = None, beta = None):


	def __computeUtility(self, state):