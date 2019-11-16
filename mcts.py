import random 

def mcts(problem):
    """
    Takes a 2-player game and uses Monte Carlo Tree Search to calculate and return
    a strategy for the game.

    Adapted from https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
    """
    strategy = {}
    # tree :: state : [sum of outcomes, # visits, explored actions, unexplored actions]
    tree = StateNode(problem.getState(), None, [])
    # TODO: psuedocode until transition function established
    for action in state.actions:
        tree.children.append(StateNode((t(state, action), tree, [])))

    savestate = problem.getState() 
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
    nextState = state.exploreChildNode()
    # TODO: not sure how this will be structured so the
    # rest of this is psuedocode for now
    # how do we transition to new state? 
    for action in availableActions:
        next_state.children.append(StateNode(t(nextState,a), nextState, []))
    return nextState

def rollout(stateNode, action):
    """
    Run a simulated playout from current state until it reaches a terminal
    state.
    """
    while not state.isTerminal():
        action = random.choice(state.getActions())
        # take this action
        # TODO: transition 
        state = t(state,action) #??? 

    return state.getValue()

def backprop(state, result):
    """
    Update current move sequence with simulation result 
    """
    while state:
        state.incrementVisits() += 1
        state.increaseSumOutcomes(result)
        state = state.getParent() 
