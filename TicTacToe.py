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
        self.num_of_searches = 0

    # captures the user's choice, validates and updates the GameBoard. A winner is
    # determined if 3 of either user's chosen positions matches any of the winning
    # sets
    def playerTurn(self, symbol):
        # capture user input
        print('What is your move?'.center(window_length))
        pos = input(''.join([' ' for item in range(int(window_length/2)-5)])+'[0-8|exit]: ')
        try:
            pos = int(pos)
        except:
            if(pos.lower() == 'exit'):
                print('GAME TERMINATED'.center(window_length))
                exit()
            print('Please enter an integer between 0 and 8.'.center(window_length))
            self.playerTurn(symbol)
            return
        #pos = int(input("What is your move? "))
        # validate user's input
        if(self.checkMove(pos)):
            # updates the GameBoard
            self.gameboard.playMove(pos, symbol)
            # true if either player is found to have won the game
            self.winner('The player')
        else:
            self.playerTurn(symbol)

    # the computer's turn to play a move, if the computer goes first, it will
    # pick a the center square as its starting position
    def compNextTurn(self, symbol, playerFirst):
        # reset the number of searches
        self.num_of_searches = 0
        # function that calls the Minimax algorithm to find the best move
        computer_move = self.findBestMove(playerFirst)
        # updates the GameBoard
        self.gameboard.playMove(computer_move, symbol)
        # true if the computer wins
        self.winner('The computer')
        print()
        self.gameboard.printBoard()
        print()
        comp_move = 'Computer\'s move...' + str(computer_move) + '\n'
        print(comp_move.center(window_length))

    # returns true if the move is possible to make, boundary error checks
    def checkMove(self, pos):
        if(not (pos <= 8 and pos >= 0) or (pos in (self.gameboard.x_pos + self.gameboard.o_pos))):
            print('You entered an invalid move, try again.'.center(window_length))
            return False
        return True

    # returns true if there are moves left, returns false otherwise
    def isMovesLeft(self, gameboard):
        return True if (9 - (len(gameboard.x_pos) + len(gameboard.o_pos)) > 0) else False

    # prints to the command line the end-state of the game and exits the game
    def winner(self, winner):
        if(self.evaluate(self.gameboard)):
            print()
            self.gameboard.printBoard()
            print('{} won!'.format(winner).center(window_length))
            exit()
        if(not self.isMovesLeft(self.gameboard)):
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
                self.gameboard.playMove(pos_index, symbol)
                # find the evaluation number for the move
                alpha = -math.inf
                beta = math.inf
                moveVal = self.minimax(self.gameboard, 0, playerFirst, alpha, beta)
                print("Move: "+ str(pos_index) + ", moveVal: " + str(moveVal), end=', ')
                # undo the move
                self.gameboard.undoMove(pos_index, symbol)
                # update the best move and highest evaluation score
                if((moveVal, pos_index) not in bestMoves):
                    bestMoves.append((moveVal, pos_index))
                # update the best evaluation (bestVal) and the corresponding position (bestMove)
                if (playerFirst and moveVal < bestVal):
                    bestMove, bestVal = pos_index, moveVal
                if (not playerFirst and moveVal > bestVal):
                    bestMove, bestVal = pos_index, moveVal
                print("bestMove: " + str(bestMove))
        print('Number of Searches: ' + str(self.num_of_searches))
        # creates random moves if there are multiple best evaluations
        bestMove = self.randomMax(bestVal, bestMoves)
        print('The best move is {}'.format(bestMove))
        return bestMove

    # returns a random maximum value from the given list
    def randomMax(self, maxVal, list):
        # a list of all the moves that have the best evaluation scores
        maxMoves = [value for value in list if value[0]==maxVal]
        return random.choice(maxMoves)[1]

    def minimax(self, gameboard, depth, isMax, alpha, beta):
        # the evaluation score
        score = self.evaluate(gameboard)
        # recursive base-case
        if(score == 10):
            return score - depth
        if(score == -10):
            return score + depth
        if(not self.isMovesLeft(gameboard)):
            return 0

        if(isMax):
            best = -math.inf
            # traverse all positions: pos_index are positions (0-8) and
            # pos are the 9 corresponding position coordinates
            for pos_index, pos in enumerate(gameboard.move_positions):
                # check if the position is vacant
                pos_sign = gameboard.board[pos[0]][pos[1]]
                if(pos_sign != 'X' and pos_sign != 'O'):
                    # make a move on the position
                    gameboard.x_pos.append(pos_index)
                    gameboard.board[pos[0]][pos[1]] = 'X'
                    self.num_of_searches += 1
                    # get the max value between the current best evaluation and the new one
                    best = max(best, self.minimax(gameboard, depth+1, not isMax, alpha, beta))
                    alpha = max(alpha, best)
                    # remove the move from the board
                    gameboard.x_pos.remove(pos_index)
                    gameboard.board[pos[0]][pos[1]] = str(pos_sign)
                    if beta <= alpha:
                        break
            return best

        else:
            best = math.inf
            for pos_index, pos in enumerate(gameboard.move_positions):
                pos_sign = gameboard.board[pos[0]][pos[1]]
                if(pos_sign != 'X' and pos_sign != 'O'):
                    # make a move on the position
                    gameboard.o_pos.append(pos_index)
                    gameboard.board[pos[0]][pos[1]] = 'O'
                    self.num_of_searches += 1
                    best = min(best, self.minimax(gameboard, depth+1, not isMax, alpha, beta))
                    beta = min(beta, best)
                    gameboard.o_pos.remove(pos_index)
                    gameboard.board[pos[0]][pos[1]] = str(pos_sign)
                    if beta <= alpha:
                        break
            return best

    # checks if each player's chosen positions constitutes a win or not
    def evaluate(self, gameboard):
        # all possible winning sets
        wins = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]]
        for positions in wins:
            x_count, o_count = 0, 0
            for pos in positions:
                # if either count variable reaches 3, then a winning set has been
                # matched and the corresponding player is the winner
                if(pos in gameboard.x_pos):
                    x_count += 1
                    if(x_count == 3):
                        return 10
                if(pos in gameboard.o_pos):
                    o_count += 1
                    if(o_count == 3):
                        return -10
        return False

    def welcome(self):
        os.system('cls')
        print('====================='.center(window_length))
        print('=====TIC-TAC-TOE====='.center(window_length))
        self.gameboard.printBoard()
        print()

    # mainloop for the game
    def startGame(self):
        self.welcome()
        print('Would you like to go first?'.center(window_length))

        mid_window_spaces = ''.join([' ' for item in range(int(window_length/2)-4)])
        playerInput = input(mid_window_spaces + '(y/n): ').lower()
        playerFirst = True if (playerInput == 'y') or (playerInput == 'yes') else False
        print()
        print('PLAYER Starts'.center(window_length)) if playerFirst else print('COMPUTER Starts'.center(window_length))
        playerSymbol = 'X' if playerFirst else 'O'
        compSymbol = 'O' if playerFirst else 'X'
        print()
        running = True
        while(running):

            if(playerFirst):
                self.playerTurn(playerSymbol)
                self.compNextTurn(compSymbol, playerFirst)
            else:
                self.compNextTurn(compSymbol, playerFirst)
                self.playerTurn(playerSymbol)

if __name__ == "__main__":
    taccy = TicTacToe()
    taccy.startGame()
