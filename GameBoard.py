class GameBoard:

    def __init__(self):
        self.board = self.createBoard()
        self.move_positions = self.getMovePositions()
        self.fillEmpty()

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

    def getMovePositions(self):
        move_positions = []
        rows = [1,5,9]
        cols = [2,8,14]
        for row in rows:
            for col in cols:
                move_positions.append((row, col))
        return move_positions

    def fillEmpty(self):
        count = 0
        for pos in self.move_positions:
            self.board[pos[0]][pos[1]] = str(count)
            count += 1

    def printBoard(self):
        for row in self.board:
            print(''.join(row))
