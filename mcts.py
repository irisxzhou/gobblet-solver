import math 


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
    tree = TreeNode()

    savestate = problem.getState() 
    strategy[savestate] = 0




    problem.setState(savestate)
    return strategy



def selection(problem, strategy, tree):
    # tree
    return

def expansion():
    return

def simulation():
    return

def backprop():
    return 
