import math


class StateNode:
    def __init__(self, state, parent, problem):
        ''' Initialize a new state-node '''
        self.__state = state
        self.__parent = parent
        self.__problem = problem

        self.__sumOutcomes = 0
        self.__numVisited = 0

    def expand(self):
        ''' Expand this node so that it is no longer a leaf node '''
        # Compute the transition dictionary
        self.__problem.setState(self.__state)
        self.__transD = {self.getChild(move): move
                         for move in self.__problem.legalMoves()}

        # for the sake of not iterating through all children every time
        self.__unexplored = list(self.__transD.keys())
        self.__explored = []

    def getChild(self, move):
        ''' Get the child of the given state '''
        self.__problem.setState(self.__state)
        self.__problem.move(move)
        return StateNode(self.__problem.getState(), self, self.__problem)

    def exploreChildNode(self):
        ''' Returns a child node to explore, if there are still unexplored
        nodes, otherwise returns None
        '''

        # If there are still some nodes to explore, explore them
        if self.__unexplored != []:
            child = self.__unexplored.pop()
            self.__explored.append(child)
            child.expand()
            return child
        else:
            return None

    def averageOutcomes(self):
        ''' Average outcomes seen so far '''
        return self.__sumOutcomes / self.__numVisited

    def getState(self):
        ''' Get the state node's state '''
        return self.__state

    def getParent(self):
        ''' Get the state node's parent '''
        return self.__parent

    def getChildren(self):
        ''' Get the state node's children '''
        return self.__transD.values()

    def getSumOutcomes(self):
        ''' Get the state node's sumOutcomes '''
        return self.__sumOutcomes

    def addOutcome(self, outcome):
        ''' Set the sumOutcomes '''
        self.__sumOutcomes += outcome
        self.__numVisited += 1

    def getNumVisited(self):
        ''' Get the state node's numVisited '''
        return self.__numVisited

    def getExplored(self):
        ''' Get the state node's explored '''
        return self.__explored

    def isTerminal(self):
        ''' Return true if this is a terminal node '''

        # Ask the problem whether or not it is terminal
        self.__problem.setState(self.__state)
        isT = self.__problem.isTerminal()

        return isT

    def terminalValue(self):
        ''' Get the outcome of the terminal node '''

        # Get the value from the problem
        self.__problem.setState(self.__state)
        value = self.__problem.finalScore()

        return value

    def UCB1(self):
        curMax = (-float('inf'), None)

        # For each of our explored children
        for child in self.__explored:
            val = child.averageOutcomes() + \
                2 * math.sqrt(math.log(self.getNumVisited()) /
                              child.getNumVisited())

            if val > curMax[0]:
                curMax = (val, child)

        return curMax[1]

    def nextMove(self):
        child = self.UCB1()
        return (self.__transD[child], child.averageOutcomes())
