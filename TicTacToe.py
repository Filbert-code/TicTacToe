from GameBoard import GameBoard

class TicTacToe:
    # constructor
    def __init__(self):
        # a GameBoard object that contains a 2D board array
        self.gameboard = GameBoard()
        self.x_pos = [] # positions marked by player X
        self.o_pos = [] # positions marked by player O
        self.playersTurn = 0 # used to keep track of who's turn it is

    # updates the GameBoard's 2D array to include the player's new move
    def playMove(self, pos, symbol):
        # row and column indices corresponding to the 9 positions of the game
        positions = self.gameboard.move_positions[pos]
        # update the board with the new move
        self.gameboard.board[positions[0]][positions[1]] = symbol
        # track the position (0-8) that has now been taken for each player
        if(symbol == 'X'):
            self.x_pos.append(pos)
        else:
            self.o_pos.append(pos)


    # returns true if the move is possible to make
    def checkMove(self, pos):
        if((pos > 8 or pos < 0) or (pos in (self.x_pos + self.o_pos))):
            print('You entered an invalid move, try again.')
            return False
        return True

    # checks if each player's chosen positions constitutes a win or not
    def winner(self):
        # all possible winning sets
        wins = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]]
        for positions in wins:
            x_count = 0
            o_count = 0
            for pos in positions:
                # if either count variable reaches 3, then a winning set has been
                # matched and the corresponding player is the winner
                if(pos in self.x_pos):
                    x_count += 1
                    if(x_count == 3):
                        return True
                if(pos in self.o_pos):
                    o_count += 1
                    if(o_count == 3):
                        return True
        return False

    # captures the user's choice, validates and updates the GameBoard. A winner is
    # determined if 3 of either user's chosen positions matches any of the winning
    # sets
    def nextTurn(self, symbol):
        # capture user input
        pos = int(input("What is your move? "))
        # validate user's input
        if(self.checkMove(pos)):
            # updates the GameBoard
            self.playMove(pos, symbol)
            print(self.x_pos)
            # true if either player is found to have won the game
            if(self.winner()):
                print()
                self.gameboard.printBoard()
                print(symbol + ' won!')
                exit()
            self.playersTurn += 1

    # mainloop for the game
    def startGame(self):
        running = True
        while(running):
            # outputs the current state of the board to the console
            self.gameboard.printBoard()
            print()
            # even numbers are X's turn, odd are O's turn
            if(self.playersTurn % 2 == 0):
                # X's turn
                self.nextTurn('X')
            else:
                # O's turn
                self.nextTurn('O')
            print()



taccy = TicTacToe()
taccy.startGame()
