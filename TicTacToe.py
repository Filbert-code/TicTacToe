from GameBoard import GameBoard

class TicTacToe:

    def __init__(self):
        self.gameboard = GameBoard()
        self.positionsTaken = []

    # pos will be a number in range (0-8), we know the position given is valid
    def playMove(self, pos, symbol):
        positions = self.gameboard.move_positions[pos]
        self.gameboard.board[positions[0]][positions[1]] = symbol

    # returns true if the move is possible to make
    def checkMove(self, pos):
        if((pos > 8 or pos < 0) or (pos in self.positionsTaken)):
            print('You entered an invalid move, try again.')
            return False
        self.positionsTaken.append(pos)
        return True

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
                    playersTurn += 1
            # O's turn
            else:
                pos = int(input("What is your move? "))
                if(self.checkMove(pos)):
                    self.playMove(pos, 'O')
                    playersTurn += 1
            print()



taccy = TicTacToe()
taccy.startGame()
