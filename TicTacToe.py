from GameBoard import GameBoard

class TicTacToe:

    def __init__(self):
        self.gameboard = GameBoard()
        self.x_pos = []
        self.o_pos = []

    # pos will be a number in range (0-8), we know the position given is valid
    def playMove(self, pos, symbol):
        positions = self.gameboard.move_positions[pos]
        self.gameboard.board[positions[0]][positions[1]] = symbol
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

    def winner(self):
        # all possible winning sets
        wins = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]]
        for positions in wins:
            x_count = 0
            o_count = 0
            for pos in positions:
                if(pos in self.x_pos):
                    x_count += 1
                    if(x_count == 3):
                        return True
                if(pos in self.o_pos):
                    o_count += 1
                    if(o_count == 3):
                        return True
        return False

    def startGame(self):
        playersTurn = 0
        running = True
        while(running):
            self.gameboard.printBoard()
            print()
            # X's turn
            if(playersTurn % 2 == 0):
                pos = int(input("What is your move? "))
                if(self.checkMove(pos)):
                    self.playMove(pos, 'X')
                    print(self.x_pos)
                    if(self.winner()):
                        print('X won!')
                        exit()
                    playersTurn += 1
            # O's turn
            else:
                pos = int(input("What is your move? "))
                if(self.checkMove(pos)):
                    self.playMove(pos, 'O')
                    print(self.o_pos)
                    if(self.winner()):
                        print('O won!')
                        exit()
                    playersTurn += 1
            print()



taccy = TicTacToe()
taccy.startGame()
