import random


def mcts(problem):
    """
    Takes a 2-player game and uses Monte Carlo Tree Search to calculate and return
    a strategy for the game.

    Adapted from https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
    """

    savestate = problem.getState()

    strategy = {}
    tree = StateNode(problem.getState(), None, problem)
    strategy[savestate] = 0

    # do stuff here

    problem.setState(savestate)
    return strategy


# not sure if this is necessary
# def selection(problem, strategy, tree):
#     # tree
#     return

def expand(state):
    """
    Expand unexplored child node. Fails if node has no more unexplored
    children.
    """
    # Get the next unexplored state
    nextState = state.exploreChildNode()

    # If all states are already explored, recurse
    if nextState is not None:
        return nextState
    else:
        return expand(state.UCB1())


def rollout(state, action):
    """
    Run a simulated playout from current state until it reaches a terminal
    state.
    """
    while not state.isTerminal():
        action = random.choice(state.getActions())
        # take this action
        # TODO: transition
        state = t(state, action)  # ???

    return state.getValue()


def backprop(state, result):
    """
    Update current move sequence with simulation result
    """
    while state:
        state.addOutcome(result)
        state = state.getParent()
