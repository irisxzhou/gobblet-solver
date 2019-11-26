import util.cImage as cImage
import random
import argparse
import time
import ast

from mcts import *

"""
Let White replace "X" as "W" and Black replace "O" as "B".
Save "state" of a tile as just the last piece on top (B0, B1, B2, B3, and white ones).
"Top" of the stack (visible on board to humans)
White is max player, Black is min player - White goes first.
"""


class Gobblet:
    '''Represents a game of Gobblet.'''

    def __init__(self):
        '''Initializes the game with an empty board.'''
        self.__board = [[["." for k in range(4)]
                         for j in range(4)] for i in range(4)]
        self.__turn = 1
        self.__numTurns = 0
        self.__rows = 4
        self.__cols = 4
        self.__num_pieces = 4
        self.__num_each = 3

        # self.__pieces[0] -> pieces left for min player (index = piece size)
        # self.__pieces[1] -> pieces left for max player
        self.__pieces = [[self.__num_each for j in range(
            self.__num_pieces)] for i in range(2)]

    def getState(self):
        '''Returns the state of the game (as a string).'''
        return str(self.__board)

    def setState(self, state):
        '''Takes a state (as returned by getState) and sets the state of the game.'''
        # Compute the new board
        newBoard = ast.literal_eval(state)
        newPieces = [[self.__num_each for j in range(
            self.__num_pieces)] for i in range(2)]

        # Check that we have an appropriately sized board
        if len(newBoard) != self.__rows:
            raise ValueError("Board is wrong size: " +
                             str(len(newBoard)) + " rows, but expected 4")
        numW = 0
        numB = 0

        # Go through all slots
        for i in range(self.__rows):
            if len(newBoard[i]) != self.__cols:
                raise ValueError("Board is wrong size: " + str(
                    len(newBoard[i])) + " columns in row " + str(i) + ", but expected 4")
            for j in range(self.__cols):
                if len(newBoard[i][j]) != self.__num_pieces:
                    raise ValueError("Board is wrong size: " + str(
                        len(newBoard[i][j])) + " spots for pieces" +
                        " in location (" + str(i) + ", " + str(j) +
                        ") but expected 4")

                for k in range(self.__num_pieces):
                    # If this is blank, nothing to do
                    if newBoard[i][j][k] == ".":
                        continue

                    # Extract player and piece
                    player = newBoard[i][j][k][0]
                    num = int(newBoard[i][j][k][1])

                    # Update the state information
                    if player == "W":
                        numW += 1
                        newPieces[1][num] -= 1
                    elif player == "B":
                        numB += 1
                        newPieces[0][num] -= 1

        if numW == numB:
            self.__turn = 1
        elif numW == numB + 1:
            self.__turn = -1
        else:
            raise ValueError("Invalid board configuration. Number of Ws: " +
                             str(numW) + ". Number of Bs: " + str(numB))

        self.__numTurns = numW + numB
        self.__board = newBoard
        self.__pieces = newPieces

        if self.isTerminal():
            self.__turn = 2

    def getSuccessors(self, state):
        '''Takes a state and returns the possible successors as 4-tuples:
        (next state, action to get there, whose turn in the next state, final score).
        For the last two items, see getTurn() and finalSCore().'''
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

    def largestPiece(self, coors):
        ''' Get the size of the largest piece in this location.
        Returns -1 if there are no pieces yet'''
        max_ = -1
        piece = "."
        i, j = coors

        for k in range(self.__num_pieces):
            if self.__board[i][j][k] == ".":
                continue

            if max_ < int(self.__board[i][j][k][1]):
                max_ = int(self.__board[i][j][k][1])
                piece = self.__board[i][j][k]

        return max_, piece

    def legalMoves(self):
        '''Returns the set of legal moves in the current state
        (a move is ie. ((x,y), "W0")).'''

        # Store the color
        if self.__turn == 2:
            return []
        elif self.__turn == -1:
            color = "B"
            pieces = self.__pieces[0]
        else:
            color = "W"
            pieces = self.__pieces[1]

        # Compute all legal moves
        movesCoords = [(i, j) for i in range(4) for j in range(4)]
        moves = [(x, color + str(k)) for x in movesCoords for k in range(4)
                 if (self.largestPiece(x)[0] < k and pieces[k] > 0)]

        return moves

    def insertPiece(self, move):
        ''' Insert a piece into the given location '''
        (i, j), piece = move
        for k in range(self.__num_pieces):
            if self.__board[i][j][k] == ".":
                self.__board[i][j][k] = piece
                return

        raise ValueError("Error inserting " + piece +
                         " at location " + str((i, j)))

    def move(self, action):
        '''Takes an action ie. ((x,y), "W0") and, if it is legal,
        changes the state accordingly.'''
        if action[0] not in [(i, j) for i in range(4) for j in range(4)]:
            raise ValueError("Unrecognized action: " + str(action))
        if self.__board[action[0][0]][action[0][1]] != ".":
            # this if takes the 'list of pieces' on a tile and compares against piece's number
            if self.largestPiece(action[0])[0] >= int(action[1][1]):
                raise ValueError("Illegal move: piece " +
                                 str(action[1]) + " not larger than top piece")

        if self.__turn == 1 and action[1][0] == "W":
            self.insertPiece(action)
            self.__pieces[1][int(action[1][1])] -= 1
            self.__turn = -1
        elif self.__turn == -1 and action[1][0] == "B":
            self.insertPiece(action)
            self.__pieces[0][int(action[1][1])] -= 1
            self.__turn = 1
        else:
            raise ValueError("Illegal move: game is terminated.")

        if self.isTerminal():
            self.__turn = 2

    def finalScore(self):
        '''If the game is not over, returns None. If it is over, returns -1 if min won,
        +1 if max won, or 0 if it is a draw.'''

        wWins = ["W", "W", "W", "W"]
        bWins = ["B", "B", "B", "B"]
        for i in range(4):
            row = [self.largestPiece((i, j))[1][0] for j in range(4)]
            col = [self.largestPiece((j, i))[1][0] for j in range(4)]
            if row == wWins or col == wWins:
                return 1
            elif row == bWins or col == bWins:
                return -1
        diag = [self.largestPiece((i, i))[1][0] for i in range(4)]
        antidiag = [self.largestPiece((i, self.__rows - i - 1))[1][0]
                    for i in range(4)]
        if diag == wWins or antidiag == wWins:
            return 1
        elif diag == bWins or antidiag == bWins:
            return -1
        elif self.legalMoves() == []:
            return 0
        else:
            return None

    def isTerminal(self):
        '''Returns true if the game is over and false otherwise.'''
        return self.finalScore() != None

    def getTile(self, row, column):
        '''Returns the contents of the board at the given position
        ("X" for max, "O" for min, and "." for empty).'''
        return self.__board[row][column]

    def getTurn(self):
        '''Determines whose turn it is. Returns 1 for max, -1 for min,
        0 for chance, or 2 if the state is terminal.'''
        return self.__turn

    def __str__(self):
        '''Returns a string representing the board.'''
        string = ""
        for i in range(self.__rows):
            for j in range(self.__cols):
                piece = self.largestPiece((i, j))[1]
                if piece == ".":
                    piece += " "

                string += piece + " "
            string += "\n"

        return string[:-1]

# completed up to here: NEED TO MAKE GOBBLET DISPLAY constructor


class GobbletDisplay:
    '''Displays a Gobblet game.'''

    def __init__(self, problem):
        '''Takes a Gobblet and initializes the display.'''
        self.__problem = problem

        self.__numCols = 4
        self.__numRows = 4

    # TODO: FIX
    def update(self):
        '''Updates the game display based on the game's current state.'''
        self.__problem.getState()

    def getMove(self):
        '''Allows the user to click to decide which square to move in.'''
        row = int(
            input("Please enter row (integer 0 through 3) you want to move piece to: "))
        col = int(
            input("Please enter col (integer 0 through 3) you want to move piece to: "))
        piece = input("Enter piece you want to put down \
            (aka 'B0', 'W1' etc - B or W for black/white and int between 0 and 3 for size, 0 smallest): ")
        return ((row, col), piece)


def main():
    parser = argparse.ArgumentParser(description='Solve and play gobblet.')
    parser.add_argument('-o', '--opponent', type=str, default='random', choices=[
                        'mcts', 'random', 'human'], help='sets the type of the opponent player (default: random)')
    parser.add_argument('-s', '--strategy', type=str, default='random', choices=[
                        'mcts', 'random'], help='sets the algorithm to generate the strategy of the agent (default: random)')
    # parser.add_argument('-p', '--prune', action='store_true', default=False, help='use alpha-beta pruning in minimax search (has no effect on expectimax)')
    parser.add_argument('-t', '--trials', type=int, default=1,
                        help='plays TRIALS games (has no effect if opponent is human, will not display games if TRIALS > 1, default: 1)')
    parser.add_argument('-nd', '--nodisplay', action='store_true', default=True,
                        help='do not display the game (has no effect if opponent is human)')
    parser.add_argument('-e', '--everyturn', action='store_true', default=False,
                        help='perform the search at every turn, rather than just from the root')

    args = parser.parse_args()

    if args.opponent == "human":
        args.trials = 1
        args.nodisplay = False

    problem = Gobblet()
    initState = problem.getState()

    agentTurn = 1

    if args.trials == 1 and not args.nodisplay:
        display = GobbletDisplay(problem)

    numWins = 0
    numDraws = 0
    avgGameLength = 0
    for t in range(args.trials):
        gameLength = 0
        problem.setState(initState)
        totalTurnTime = 0
        while not problem.isTerminal():
            if problem.getTurn() == agentTurn:
                startT = time.time()

                if args.strategy == "mcts":
                    move = mcts(problem)[0]
                if args.strategy == "random":
                    move = random.choice(problem.legalMoves())

                endT = time.time()
                totalTurnTime += endT-startT
            elif args.opponent == "mcts":
                move = mcts(problem)[0]
            elif args.opponent == "random":
                move = random.choice(problem.legalMoves())
            else:
                move = display.getMove()

            print(problem.getTurn(), move)
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
            whoWon = "B wins!"
        elif problem.finalScore() > 0:
            whoWon = "W wins!"
            numWins += 1

        if args.trials == 1:
            print(whoWon + " (" + str(gameLength) + " turns)")
            print(problem)
            print(
                "Total time in agent turns (ignoring opponent turns): " + str(totalTurnTime))

    if args.trials > 1:
        print("Agent stats:")
        print("Wins:   " + str(numWins))
        print("Draws:  " + str(numDraws))
        print("Losses: " + str(args.trials - numWins - numDraws))
        print("Avg. Length: " + str(avgGameLength/args.trials) + " turns")


if __name__ == "__main__":
    main()
