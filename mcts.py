import math, random 


class StateNode:
    def __init__:

        
def mcts(problem):
    """
    Takes a 2-player game and uses Monte Carlo Tree Search to calculate and return
    a strategy for the game.

    Adapted from https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
    """

    # 
    strategy = {}
    # tree :: state : [sum of outcomes, # visits, explored actions, unexplored actions]
    # tree = StateNode()

    savestate = problem.getState() 
    strategy[savestate] = 0




    problem.setState(savestate)
    return strategy



def selection(problem, strategy, tree):
    # tree
    return

def expansion():
    return

def rollout(state, action):
    if state.isTerminal():
        return state.getValue()
    Ai = random.choice(state.getActions())
    # return rollout(new State, new Action)
    return

def backprop():
    return 
