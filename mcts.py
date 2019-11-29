import random

from statenode import StateNode, nodes


def mcts(problem):
    """
    Takes a 2-player game and uses Monte Carlo Tree Search to calculate and return
    a strategy for the game.

    Adapted from
    https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
    """

    # Settings
    iters = 1000
    useSaved = True

    if problem.isTerminal():
        return (0, problem.finalScore())

    savestate = problem.getState()

    if useSaved and problem.getState() in nodes:
        tree = nodes[problem.getState()]
    else:
        tree = StateNode(problem, None)

    tree.expand()

    for i in range(iters):
        leaf = expand(tree)
        score = rollout(problem, leaf.getState())
        backprop(leaf, score)

    problem.setState(savestate)
    return tree.nextMove()


def expand(node):
    """
    Expand unexplored child node. Fails if node has no more unexplored
    children.
    """
    if node.isTerminal():
        return node

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
