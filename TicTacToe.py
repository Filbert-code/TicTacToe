from GameBoard import GameBoard
import math
import random
import os
window_length = os.get_terminal_size().columns

class TicTacToe:
    # constructor
    def __init__(self):
        # a GameBoard object that contains a 2D board array
        self.gameboard = GameBoard()
        self.x_pos = [] # positions marked by player X
        self.o_pos = [] # positions marked by player O

    # captures the user's choice, validates and updates the GameBoard. A winner is
    # determined if 3 of either user's chosen positions matches any of the winning
    # sets
    def playerTurn(self, symbol):
        # capture user input
        pos = int(input(''.join([' ' for item in range(int(window_length/2)-11)])+'What is your move? '))
        #pos = int(input("What is your move? "))
        # validate user's input
        if(self.checkMove(pos)):
            # updates the GameBoard
            self.playMove(pos, symbol)
            # true if either player is found to have won the game
            self.winner('The player')

    # the computer's turn to play a move, if the computer goes first, it will
    # pick a random starting position
    def compNextTurn(self, symbol):
        # function that calls the Minimax algorithm to find the best move
        computer_move = self.findBestMove(False)
        # updates the GameBoard
        self.playMove(computer_move, symbol)
        # true if the computer wins
        self.winner('The computer')
        print()
        self.gameboard.printBoard()
        print()
        comp_move = 'Computer\'s move...' + str(computer_move) + '\n'
        print(comp_move.center(window_length))

    # updates the GameBoard's 2D array to include the player's new move
    def playMove(self, pos, symbol):
        # row and column indices corresponding to the 9 positions of the game
        positions = self.gameboard.move_positions[pos]
        # update the board with the new move
        self.gameboard.board[positions[0]][positions[1]] = symbol
        # track the position (0-8) that has now been taken for each player
        self.x_pos.append(pos) if symbol == 'X' else self.o_pos.append(pos)

    # returns true if the move is possible to make, boundary error checks
    def checkMove(self, pos):
        if((pos > 8 or pos < 0) or (pos in (self.x_pos + self.o_pos))):
            print('You entered an invalid move, try again.'.center(window_length))
            return False
        return True

    # returns true if there are moves left, returns false otherwise
    def isMovesLeft(self, x_pos, o_pos):
        return True if (9 - (len(x_pos) + len(o_pos)) > 0) else False

    # prints to the command line the end-state of the game and exits the game
    def winner(self, winner):
        if(self.evaluate(self.x_pos, self.o_pos)):
            print()
            self.gameboard.printBoard()
            print('{} won!'.format(winner).center(window_length))
            exit()
        if(not self.isMovesLeft(self.x_pos, self.o_pos)):
            print()
            self.gameboard.printBoard()
            print('It\'s a tie!'.center(window_length))
            exit()

    # returns the best move for the computer found using a backtracking
    # algorithm called Minimax.
    def findBestMove(self, playerFirst):
        # computer's symbol
        symbol = 'X' if not playerFirst else 'O'
        # variable for helping to find the best evaluation score
        bestVal = -math.inf if not playerFirst else math.inf
        # a list to help randomize the best move selection
        bestMoves = []
        # the move with the highest score returned at the end of the function
        bestMove = 10 # 10 will be overridden
        print('--------------\nAI Evaluations\n--------------')
        for pos_index, pos in enumerate(self.gameboard.move_positions):
            # check if the position is empty
            pos_sign = self.gameboard.board[pos[0]][pos[1]]
            if(pos_sign != 'X' and pos_sign != 'O'):
                # make the move
                self.gameboard.board[pos[0]][pos[1]] = symbol
                # add the move to the corresponding position list
                self.o_pos.append(pos_index) if playerFirst else self.x_pos.append(pos_index)
                # find the evaluation number for the move
                moveVal = self.minimax(self.x_pos, self.o_pos, 0, playerFirst)
                print("Move: "+ str(pos_index) + ", moveVal: " + str(moveVal), end=', ')

                # undo the move
                self.gameboard.board[pos[0]][pos[1]] = str(pos_sign)
                # remove the move to the corresponding position list
                self.o_pos.remove(pos_index) if playerFirst else self.x_pos.remove(pos_index)
                # update the best move and highest evaluation score
                if((moveVal, pos_index) not in bestMoves):
                    bestMoves.append((moveVal, pos_index))
                # update the best evaluation (bestVal) and the corresponding position (bestMove)
                if (playerFirst and moveVal < bestVal):
                    bestMove, bestVal = pos_index, moveVal
                if (not playerFirst and moveVal > bestVal):
                    bestMove, bestVal = pos_index, moveVal
                print("bestMove: " + str(bestMove))
        # creates random moves if there are multiple best evaluations
        bestMove = self.randomMax(bestVal, bestMoves)
        print('The best move is {}'.format(bestMove))
        return bestMove

    # returns a random maximum value from the given list
    def randomMax(self, maxVal, list):
        # a list of all the moves that have the best evaluation scores
        maxMoves = [value for value in list if value[0]==maxVal]
        return random.choice(maxMoves)[1]

    def minimax(self, x_pos, o_pos, depth, isMax):
        # the evaluation score
        score = self.evaluate(x_pos, o_pos)
        # recursive base-case
        if(score == 10):
            return score - depth
        if(score == -10):
            return score + depth
        if(not self.isMovesLeft(x_pos, o_pos)):
            return 0

        if(isMax):
            best = -math.inf
            # traverse all positions: pos_index are positions (0-8) and
            # pos are the 9 corresponding position coordinates
            for pos_index, pos in enumerate(self.gameboard.move_positions):
                # check if the position is vacant
                pos_sign = self.gameboard.board[pos[0]][pos[1]]
                if(pos_sign != 'X' and pos_sign != 'O'):
                    # make a move on the position
                    x_pos.append(pos_index)
                    self.gameboard.board[pos[0]][pos[1]] = 'X'
                    # get the max value between the current best evaluation and the new one
                    best = max(best, self.minimax(x_pos, o_pos, depth+1, not isMax))
                    # remove the move from the board
                    x_pos.remove(pos_index)
                    self.gameboard.board[pos[0]][pos[1]] = str(pos_sign)
            return best

        else:
            best = math.inf
            for pos_index, pos in enumerate(self.gameboard.move_positions):
                pos_sign = self.gameboard.board[pos[0]][pos[1]]
                if(pos_sign != 'X' and pos_sign != 'O'):
                    # make a move on the position
                    o_pos.append(pos_index)
                    self.gameboard.board[pos[0]][pos[1]] = 'O'

                    best = min(best, self.minimax(x_pos, o_pos, depth+1, not isMax))

                    o_pos.remove(pos_index)
                    self.gameboard.board[pos[0]][pos[1]] = str(pos_sign)
            return best

    # checks if each player's chosen positions constitutes a win or not
    def evaluate(self, x_pos, o_pos):
        # all possible winning sets
        wins = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]]
        for positions in wins:
            x_count, o_count = 0, 0
            for pos in positions:
                # if either count variable reaches 3, then a winning set has been
                # matched and the corresponding player is the winner
                if(pos in x_pos):
                    x_count += 1
                    if(x_count == 3):
                        return 10
                if(pos in o_pos):
                    o_count += 1
                    if(o_count == 3):
                        return -10
        return False

    def welcome(self):
        os.system('cls')
        print('========================='.center(window_length))
        print('=======TIC-TAC-TOE======='.center(window_length))
        self.gameboard.printBoard()

    # mainloop for the game
    def startGame(self):
        self.welcome()
        print('Would you like to go first?'.center(window_length))

        playerFirst = True if input(''.join([' ' for item in range(int(window_length/2)-4)])+'(y/n): ').lower()=='y' else False
        playerSymbol = 'X' if playerFirst else 'O'
        compSymbol = 'O' if playerFirst else 'X'
        print()
        running = True
        while(running):

            if(playerFirst):
                self.playerTurn(playerSymbol)
                self.compNextTurn(compSymbol)
            else:
                self.compNextTurn(compSymbol)
                self.playerTurn(playerSymbol)

if __name__ == "__main__":
    taccy = TicTacToe()
    taccy.startGame()
