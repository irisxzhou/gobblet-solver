import math


class StateNode:
    def __init__(self, state, parent, children):
        ''' '''
        # tree :: state : [sum of outcomes, # visits, explored actions, unexplored actions]
        self.__state = state
        self.__parent = parent
        self.__children = children

        self.__sumOutcomes = 0
        self.__numVisited = 0
        self.__explored = 0

    def average_outcomes(self):
        ''' Average outcomes seen so far '''
        return self.__sumOutcomes / self.__numVisited

    def getState(self):
        ''' Get the state node's state '''
        return self.__state

    def setState(self, state):
        ''' Set the state '''
        self.__state = state

    def getParent(self):
        ''' Get the state node's parent '''
        return self.__parent

    def setParent(self, parent):
        ''' Set the parent '''
        self.__parent = parent

    def getChildren(self):
        ''' Get the state node's children '''
        return self.__children

    def setChildren(self, children):
        ''' Set the children '''
        self.__children = children

    def getSumOutcomes(self):
        ''' Get the state node's sumOutcomes '''
        return self.__sumOutcomes

    def setSumOutcomes(self, sumOutcomes):
        ''' Set the sumOutcomes '''
        self.__sumOutcomes = sumOutcomes

    def getNumVisited(self):
        ''' Get the state node's numVisited '''
        return self.__numVisited

    def setNumVisited(self, numVisited):
        ''' Set the numVisited '''
        self.__numVisited = numVisited

    def getExplored(self):
        ''' Get the state node's explored '''
        return self.__explored

    def setExplored(self, explored):
        ''' Set the explored '''
        self.__explored = explored

    def ucb1(self):
        currentMax = (-float('inf'), None)
        for child in self.__children:
            val = child.averageOutcomes() + \
                2 * math.sqrt(math.log(tree.getNumVisited) /
                              child.getNumVisited)
        # outcomes = tree
        # visits = tree[state[1]]
