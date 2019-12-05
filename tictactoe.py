''' Source: CS 151 Project 2 Starter Code '''

import util.cImage as cImage
import random
import argparse
import time
from expectiminimax import *
from mcts import * 

class TicTacToe:
    '''Represents a game of Tic-Tac-Toe.'''

    def __init__(self, randomO=False, randomX=False):
        '''Initializes the game with an empty board.'''
        self.__board = [["."]*3, ["."]*3, ["."]*3]
        self.__turn = 1
        self.__randomO = randomO
        self.__randomX = randomX
        self.__numTurns = 0

    def getState(self):
        '''Returns the state of the game (as a string).'''
        rows = [" ".join(self.__board[i]) +
                "\n" for i in range(len(self.__board))]
        return "".join(rows)

    def setState(self, state):
        '''Takes a state (as returned by getState) and sets the state of the game.'''
        rows = state.split("\n")[:-1]
        newBoard = [rows[i].split() for i in range(len(rows))]
        if len(newBoard) != 3:
            raise ValueError("Board is wrong size: " +
                             str(len(newBoard)) + " rows, but expected 3")
        numX = 0
        numO = 0
        for i in range(3):
            if len(newBoard[i]) != 3:
                raise ValueError("Board is wrong size: " + str(
                    len(newBoard[i])) + " columns in row " + str(i) + ", but expected 3")
            for j in range(3):
                if newBoard[i][j] == "X":
                    numX += 1
                elif newBoard[i][j] == "O":
                    numO += 1
                elif newBoard[i][j] != ".":
                    raise ValueError(
                        "Unrecognized board symbol: " + newBoard[i][j] + " (must be ., X, or O)")

        if numX == numO:
            self.__turn = 1
        elif numX == numO + 1:
            self.__turn = -1
        else:
            raise ValueError("Invalid board configuration. Number of Xs: " +
                             str(numX) + ". Number of Os: " + str(numO))

        self.__numTurns = numX + numO
        self.__board = newBoard
        if self.isTerminal():
            self.__turn = 2

    def getSuccessors(self, state):
        '''Takes a state and returns the possible successors as 4-tuples: (next state, action to get there, whoe turn in the next state, final score). For the last two items, see getTurn() and finalSCore().'''
        currentState = self.getState()
        succ = []
        self.setState(state)
        for a in self.legalMoves():
            self.move(a)
            succ.append(
                (self.getState(), a, self.getTurn(), self.finalScore()))
            self.setState(state)
        self.setState(currentState)
        random.shuffle(succ)
        return succ

    def legalMoves(self):
        '''Returns the set of legal moves in the current state (a move is row, column tuple).'''
        if self.__turn == 2:
            return []
        else:
            return [(i, j) for i in range(3) for j in range(3) if self.__board[i][j] == "."]

    def move(self, action):
        '''Takes an action (a row, column tuple) and, if it is legal, changes the state accordingly.'''
        if action not in [(i, j) for i in range(3) for j in range(3)]:
            raise ValueError("Unrecognized action: " + str(action))
        if self.__board[action[0]][action[1]] != ".":
            raise ValueError("Illegal move: position " + str(action) +
                             " is already occupied (" + self__board[action[0]][action[1]] + ")")

        if self.__turn == 2:
            raise ValueError("Illegal move: game is terminated.")
        elif self.__turn == 1:
            self.__board[action[0]][action[1]] = "X"
            self.__turn = -1
        elif self.__turn == -1:
            self.__board[action[0]][action[1]] = "O"
            self.__turn = 1

        if self.isTerminal():
            self.__turn = 2

    def finalScore(self):
        '''If the game is not over, returns None. If it is over, returns -1 if min won, +1 if max won, or 0 if it is a draw.'''
        xWins = ["X", "X", "X"]
        oWins = ["O", "O", "O"]
        for i in range(3):
            row = [self.__board[i][j] for j in range(3)]
            col = [self.__board[j][i] for j in range(3)]
            if row == xWins or col == xWins:
                return 1
            elif row == oWins or col == oWins:
                return -1
        diag = [self.__board[i][i] for i in range(3)]
        antidiag = [self.__board[i][2-i] for i in range(3)]
        if diag == xWins or antidiag == xWins:
            return 1
        elif diag == oWins or antidiag == oWins:
            return -1

        for i in range(3):
            if "." in self.__board[i]:
                return None
        return 0

    def isTerminal(self):
        '''Returns true if the game is over and false otherwise.'''
        return self.finalScore() != None

    def getTile(self, row, column):
        '''Returns the contents of the board at the given position ("X" for max, "O" for min, and "." for empty).'''
        return self.__board[row][column]

    def getTurn(self):
        '''Determines whose turn it is. Returns 1 for max, -1 for min, 0 for chance, or 2 if the state is terminal.'''
        if self.__randomO and self.__turn == -1:
            return 0
        elif self.__randomX and self.__turn == 1:
            return 0
        else:
            return self.__turn

    def __str__(self):
        '''Returns a string representing the board (same as getState()).'''
        return self.getState()


class TicTacToeDisplay:
    '''Displays a Tic-Tac-Toe game.'''

    def __init__(self, problem):
        '''Takes a TicTacToe and initializes the display.'''
        self.__problem = problem

        self.__numCols = 3
        self.__numRows = 3

        self.__images = []
        for r in range(self.__numRows):
            self.__images.append([])
            for c in range(self.__numCols):
                self.__images[r].append([])
                self.__images[r][c].append(
                    cImage.FileImage("images/tttBlank.gif"))
                self.__images[r][c].append(
                    cImage.FileImage("images/tttMax.gif"))
                self.__images[r][c].append(
                    cImage.FileImage("images/tttMin.gif"))
                for i in range(3):
                    img = self.__images[r][c][i]
                    img.setPosition(c*img.getWidth(), r*img.getHeight())

        self.__tileWidth = self.__images[0][0][0].getWidth()
        self.__tileHeight = self.__images[0][0][0].getHeight()
        self.__win = cImage.ImageWin(
            "Tic-Tac-Toe!", self.__numCols*self.__tileWidth, self.__numRows*self.__tileHeight)

        backgroundImage = cImage.FileImage("images/tttBackground.gif")
        backgroundImage.draw(self.__win)
        self.update()

    def update(self):
        '''Updates the game display based on the game's current state.'''
        for r in range(self.__numRows):
            for c in range(self.__numCols):
                t = self.__problem.getTile(r, c)
                if t == ".":
                    self.__images[r][c][0].draw(self.__win)
                elif t == "X":
                    self.__images[r][c][1].draw(self.__win)
                else:  # "O"
                    self.__images[r][c][2].draw(self.__win)

    def getMove(self):
        '''Allows the user to click to decide which square to move in.'''
        print("Please click on an empty space.")
        pos = self.__win.getMouse()
        col = pos[0]//self.__tileWidth
        row = pos[1]//self.__tileHeight
        while (row, col) not in self.__problem.legalMoves():
            print("Illegal move! Please click on an empty space.")
            pos = self.__win.getMouse()
            col = pos[0]//self.__tileWidth
            row = pos[1]//self.__tileHeight
        return (row, col)

    def exitonclick(self):
        self.__win.exitonclick()


def main():
    parser = argparse.ArgumentParser(description='Solve and play tic-tac-toe.')
    parser.add_argument('-o', '--opponent', type=str, default='minimax', choices=[
                        'minimax', 'random', 'human', 'mcts'], help='sets the type of the opponent player (default: minimax)')
    parser.add_argument('-s', '--strategy', type=str, default='minimax', choices=[
                        'minimax', 'random', 'expectimax', 'mcts'], help='sets the algorithm to generate the strategy of the agent (default: minimax)')
    parser.add_argument('-p', '--prune', action='store_true', default=False,
                        help='use alpha-beta pruning in minimax search (has no effect on expectimax)')
    parser.add_argument('-t', '--trials', type=int, default=1,
                        help='plays TRIALS games (has no effect if opponent is human, will not display games if TRIALS > 1, default: 1)')
    parser.add_argument('-O', '--playO', action='store_true',
                        default=False, help='makes the agent play O instead of X')
    parser.add_argument('-nd', '--nodisplay', action='store_true', default=False,
                        help='do not display the game (has no effect if opponent is human)')
    parser.add_argument('-e', '--everyturn', action='store_true', default=False,
                        help='perform the search at every turn, rather than just from the root, has no effect on mcts')
    parser.add_argument('-i', '--iterations', default=1000,
                        help='number of iterations for MCTS (has no effect if' +
                        ' agent is not MCTS), default: 1000')

    args = parser.parse_args()

    if args.opponent == "human":
        args.trials = 1
        args.nodisplay = False

    problem = TicTacToe()
    initState = problem.getState()
    if args.playO:
        randomProblem = TicTacToe(randomX=True)
    else:
        randomProblem = TicTacToe(randomO=True)

    if not args.everyturn:
        if args.strategy == "minimax" or args.opponent == "minimax":
            print("Pre-calculating minimax strategy...")
            startT = time.time()
            minimaxStrategy = minimax(problem, args.prune)
            endT = time.time()
            print("Finished in {0:.5f}".format(endT-startT) + " seconds.")
            if args.strategy == "minimax":
                strategy = minimaxStrategy

        if args.strategy == "expectimax":
            print("Pre-calculating expectimax strategy...")
            startT = time.time()
            expectimaxStrategy = expectiminimax(randomProblem)
            endT = time.time()
            print("Finished in {0:.5f}".format(endT-startT) + " seconds.")
            strategy = expectimaxStrategy

    agentTurn = 1
    if args.playO:
        agentTurn = -1

    if args.trials == 1 and not args.nodisplay:
        display = TicTacToeDisplay(problem)

    numWins = 0
    numDraws = 0
    avgGameLength = 0
    totalTurnTime = 0
    for t in range(args.trials):
        gameLength = 0
        problem.setState(initState)
        while not problem.isTerminal():
            if problem.getTurn() == agentTurn:
                startT = time.time()
                if args.everyturn:
                    if args.strategy == "minimax":
                        strategy = minimax(problem, args.prune)
                    if args.strategy == "expectimax":
                        strategy = expectiminimax(randomProblem)
                if args.strategy == "mcts":
                    move = mcts(problem, args.iterations)[0]
                elif args.strategy == "random":
                    move = random.choice(problem.legalMoves())
                else: # minimax/expectimax
                    move = strategy[problem.getState()][0]
                endT = time.time()
                totalTurnTime += endT-startT
            # otherwise, it is the opponent's turn
            elif args.opponent == "minimax":
                if args.everyturn:
                    minimaxStrategy = minimax(problem, args.prune)

                move = minimaxStrategy[problem.getState()][0]
            elif args.opponent == "random":
                move = random.choice(problem.legalMoves())
            elif args.opponent == "mcts":
                move = mcts(problem, args.iterations)[0]
            else:  # human player
                move = display.getMove()
            problem.move(move)
            avgGameLength += 1
            gameLength += 1
            if args.trials == 1 and not args.nodisplay:
                display.update()
                time.sleep(1)

        if problem.finalScore() == 0:
            whoWon = "Draw"
            numDraws += 1
        elif problem.finalScore() < 0:
            whoWon = "O wins!"
            if args.playO:
                numWins += 1
        elif problem.finalScore() > 0:
            whoWon = "X wins!"
            if not args.playO:
                numWins += 1

        if args.trials == 1:
            print(whoWon + " (" + str(gameLength) + " turns)")
            print(
                "Total time in agent turns (ignoring opponent turns): " + str(totalTurnTime))

    if args.trials > 1:
        print("Agent stats:")
        print("Wins:   " + str(numWins))
        print("Draws:  " + str(numDraws))
        print("Losses: " + str(args.trials - numWins - numDraws))
        print("Avg. Length: " + str(avgGameLength/args.trials) + " turns")
        print("Average time in agent turns (ignoring opponent turns): " + str(totalTurnTime / args.trials))


    if args.trials == 1 and not args.nodisplay:
        print("Click on the window to exit")
        display.exitonclick()


if __name__ == "__main__":
    main()
