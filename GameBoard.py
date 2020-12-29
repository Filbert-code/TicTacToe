import os
window_length = os.get_terminal_size().columns
class GameBoard:
    # constructor
    def __init__(self):
        self.board = self.createBoard()
        self.move_positions = self.getMovePositions()
        self.x_pos = []
        self.o_pos = []
        self.fillEmpty()

    # creates the 2D board
    def createBoard(self):
        board = []
        for row in range(3):
            for col in range(3):
                board_row = '     |     |     '
                board.append([value for value in board_row])

            if(row != 2):
                board_row ="-----------------"
                board.append([value for value in board_row])
        return board

    # returns a list of tuples of the coordinates on the board that pertain
    # to the 9 game positions
    def getMovePositions(self):
        move_positions = []
        rows = [1,5,9]
        cols = [2,8,14]
        for row in rows:
            for col in cols:
                move_positions.append((row, col))
        return move_positions

    # fills the board's 9 positions with values 0-8
    def fillEmpty(self):
        count = 0
        for pos in self.move_positions:
            self.board[pos[0]][pos[1]] = str(count)
            count += 1

    # returns true if the move is possible to make, boundary error checks
    def checkMove(self, pos):
        if(not (pos <= 8 and pos >= 0) or (pos in (self.x_pos + self.o_pos))):
            print()
            print('You entered an invalid move, try again.'.center(window_length))
            print()
            return False
        return True

    # updates the 2D array to include the player's new move
    def playMove(self, pos, symbol):
        # update the board with the new move
        self.board[self.move_positions[pos][0]][self.move_positions[pos][1]] = symbol
        # track the position (0-8) that has now been taken for each player
        self.x_pos.append(pos) if symbol == 'X' else self.o_pos.append(pos)

    # updates the 2D array to undo the move at the given position
    def undoMove(self, pos, symbol):
        # update the board with undoing the move
        self.board[self.move_positions[pos][0]][self.move_positions[pos][1]] = str(pos)
        self.x_pos.remove(pos) if symbol == 'X' else self.o_pos.remove(pos)

    # returns true if there are moves left, returns false otherwise
    def isMovesLeft(self):
        return True if (9 - (len(self.x_pos) + len(self.o_pos)) > 0) else False

    # print the state of the board to the console
    def printBoard(self):
        print('====================='.center(window_length))
        for row in self.board:
            rowStr = '||'+''.join(row) + '||'
            print(rowStr.center(window_length))
        print('====================='.center(window_length))
