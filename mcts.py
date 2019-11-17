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

def expand(node):
    """
    Expand unexplored child node. Fails if node has no more unexplored
    children.
    """
    # Get the next unexplored state
    nextState = node.exploreChildNode()

    # If all states are already explored, recurse
    if nextState is not None:
        return nextState
    else:
        return expand(node.UCB1())


def rollout(problem, state):
    """
    Run a simulated playout from current state until it reaches a terminal
    state.
    """
    problem.setState(state)
    while not problem.isTerminal():
        action = random.choice(problem.legalMoves())
        problem.move(action)

    return problem.finalScore()


def backprop(node, result):
    """
    Update current move sequence with simulation result
    """
    while node:
        node.addOutcome(result)
        node = node.getParent()
