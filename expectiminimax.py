def minimax(problem, prune=False):
    '''
    Takes a 2-player game and uses minimax search to calculate and return
    a strategy for the game. The strategy is a dictionary that maps states
    to pairs. The first element is an optimal action in that state. The
    second element of the pair is the minimax score of the state. If the
    prune parameter is True, the algorithm uses alpha-beta pruning. In that
    case, pruned states do not appear in the strategy. After this function
    executes, the state of problem should be the same as when it was passed in.
    '''
    strategy = {}
    ####YOUR CODE HERE
    savestate = problem.getState() # save so it isn't modified

    # recurse with helper function
    alpha = -float('inf')
    beta = float('inf')
    minimaxH(problem, strategy, prune, alpha, beta)
    ####(you'll probably want to define one or more helper functions as well)
    

    problem.setState(savestate)
    return strategy



def minimaxH(problem, strategy, prune, alpha, beta):
    # Should never get called on a terminal state 
    currentTurn = problem.getTurn()
    currentState = problem.getState()
    successors = problem.getSuccessors(currentState)

    options = []
    for (nextState, action, nextTurn, score) in successors:
        # next state is terminal state
        if score is not None:
            options += [(action, score)]
        else: # recurse to get to terminal state
            problem.setState(nextState)
            options += [(action,minimaxH(problem,strategy, prune, alpha, beta))]
        if prune:
            if currentTurn == 1: # max's turn -- best choice at a lowest node
                if options[-1][1] > alpha:
                    alpha = options[-1][1]
            else:
                if options[-1][1] < beta:
                    beta = options[-1][1]
            if alpha >= beta:
                break

    if currentTurn == 1: # max's turn, take the
        strategy[currentState] = max(options, key=lambda x:x[1])
    else:
        strategy[currentState] = min(options, key=lambda x:x[1])

    return strategy[currentState][1]
    

def expectiminimax(problem):
    '''
    Takes a 2-player game of chance and uses expectiminimax to calculate
    and return a strategy for the game. The strategy is a dictionary that
    maps states to pairs. The first element is an optimal action in that state.
    The second element of the pair is the minimax score of the state. After
    this function executes, the state of problem should be the same as when it
    was passed in.
    '''
    strategy = {}
    savestate = problem.getState() # save so it isn't modified

    emmH(problem, strategy)

    problem.setState(savestate)
    return strategy

def emmH(problem, strategy):
    # Should never get called on a terminal state 
    currentTurn = problem.getTurn()
    currentState = problem.getState()
    successors = problem.getSuccessors(currentState)

    options = []
    for (nextState, action, nextTurn, score) in successors:
        # next state is terminal state
        if score is not None:
            options += [(action, score)]
        else: # recurse to get to terminal state
            problem.setState(nextState)
            options += [(action,emmH(problem,strategy))]

    if currentTurn == 1: # max's turn, take the
        strategy[currentState] = max(options, key=lambda x:x[1])
    elif currentTurn == -1:
        strategy[currentState] = min(options, key=lambda x:x[1])
    else:
        sum = 0
        for option in options:
            sum += option[1]
        average = sum / len(options)
        strategy[currentState] = (options[0][0], average)

    return strategy[currentState][1]
