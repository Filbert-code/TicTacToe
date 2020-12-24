from GameBoard import GameBoard
import math
import random

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
        self.gameboard.printBoard()
        print()
        # capture user input
        pos = int(input("What is your move? "))
        # validate user's input
        if(self.checkMove(pos)):
            # updates the GameBoard
            self.playMove(pos, symbol)
            # true if either player is found to have won the game
            self.winner('The player')

    def compNextTurn(self, symbol):

        computer_move = self.findBestMove(False)
        self.playMove(computer_move, symbol)
        self.winner('The computer')
        print()
        self.gameboard.printBoard()
        print('\nComputer\'s move...\n')

    # updates the GameBoard's 2D array to include the player's new move
    def playMove(self, pos, symbol):
        # row and column indices corresponding to the 9 positions of the game
        positions = self.gameboard.move_positions[pos]
        # update the board with the new move
        self.gameboard.board[positions[0]][positions[1]] = symbol
        # track the position (0-8) that has now been taken for each player
        self.x_pos.append(pos) if symbol == 'X' else self.o_pos.append(pos)

    # returns true if the move is possible to make
    def checkMove(self, pos):
        if((pos > 8 or pos < 0) or (pos in (self.x_pos + self.o_pos))):
            print('You entered an invalid move, try again.')
            return False
        return True

    # returns true if there are moves left, returns false otherwise
    def isMovesLeft(self, x_pos, o_pos):
        return True if (9 - (len(x_pos) + len(o_pos)) > 0) else False

    def winner(self, winner):
        if(self.evaluate(self.x_pos, self.o_pos)):
            print()
            self.gameboard.printBoard()
            print('{} won!'.format(winner))
            exit()
        if(not self.isMovesLeft(self.x_pos, self.o_pos)):
            print()
            self.gameboard.printBoard()
            print('It\'s a tie!')
            exit()

    def findBestMove(self, playerFirst):
        symbol = 'X' if not playerFirst else 'O'

        bestVal = -math.inf if not playerFirst else math.inf
        # the move with the highest score returned at the end of the function
        bestMoves = []
        bestMove = 10
        for pos_index, pos in enumerate(self.gameboard.move_positions):
            # true if the checked position is empty
            pos_sign = self.gameboard.board[pos[0]][pos[1]]
            if(pos_sign != 'X' and pos_sign != 'O'):
                # make the move
                self.gameboard.board[pos[0]][pos[1]] = symbol

                self.o_pos.append(pos_index) if playerFirst else self.x_pos.append(pos_index)
                # find the evaluation number for the move
                moveVal = self.minimax(self.x_pos, self.o_pos, 0, playerFirst)
                print("Move: "+ str(pos_index) + ", moveVal: " + str(moveVal), end=', ')

                # undo the move
                self.gameboard.board[pos[0]][pos[1]] = str(pos_sign)
                self.o_pos.remove(pos_index) if playerFirst else self.x_pos.remove(pos_index)
                # update the best move and highest evaluation score
                if((moveVal, pos_index) not in bestMoves):
                    bestMoves.append((moveVal, pos_index))

                if (playerFirst and moveVal < bestVal):
                    bestMove, bestVal = pos_index, moveVal
                if (not playerFirst and moveVal > bestVal):
                    bestMove, bestVal = pos_index, moveVal

                print("bestMove: " + str(bestMove))
        # creates random moves if there are multiple best evaluations
        bestMove = self.randomMax(bestVal, bestMoves)
        print('The best move is {}'.format(bestMove))
        return bestMove

    def randomMax(self, maxVal, list):
        # a list of all the moves that have the best evaluation scores
        maxMoves = [value for value in list if value[0]==maxVal]
        print('maxMoves: ', end=' ')
        print(maxMoves)
        return random.choice(maxMoves)[1]

    def minimax(self, x_pos, o_pos, depth, isMax):

        score = self.evaluate(x_pos, o_pos)

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

                    best = max(best, self.minimax(x_pos, o_pos, depth+1, not isMax))

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

    # mainloop for the game
    def startGame(self):
        playerFirst = True if input('Would you like to go first? (y/n)').lower()=='yes' else False
        playerSymbol = 'X' if playerFirst else 'O'
        compSymbol = 'O' if playerFirst else 'X'
        running = True
        while(running):
            if(playerFirst):
                self.playerTurn(playerSymbol)
                self.compNextTurn(compSymbol)



taccy = TicTacToe()
taccy.startGame()
