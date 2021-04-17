class Connect4Game:

    def __init__(self, user, opponent, userTurn, checkWin, gameEnd, checkTie):
        self.user = user
        self.opponent = opponent
        self.userTurn = userTurn
        self.checkWin = checkWin
        self.gameEnd = gameEnd
        self.checkTie = checkTie

    ROW = 6
    COL = 7
    board = [ # 6*7 board
        #  A     B      C     D      E     F      G
        ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'], # 0
        ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'], # 1
        ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'], # 2
        ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'], # 3
        ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'], # 4
        ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪']  # 5
    ]

    columnIds = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    turn: str = '🔴'
    slotsFilled = 0

    def makeMove(self, move) -> str:
        try: 
            if self.validMove(move):
                row = self.getOpenRow(move)
                print(row)
                self.board[row][self.columnIds.index(move[0].upper())] = self.turn

            else: 
                return 'Error: This Column is Full.'
        except (IndexError, ValueError):
            return 'Error: Please input special key \'-\', followed by letter A to G to select column'

        output = self.initBoard()

        victoryStatus = str(self.checkForVictory())
        if(victoryStatus == self.turn):
            self.checkWin = True
            self.gameEnd = True
            if(self.userTurn == True):
                return output + "\n\n" + victoryStatus + ", <@!" + str(self.user) + ">, Wins!"
            else:
                return output + "\n\n" + victoryStatus + ", <@!" + str(self.opponent) + ">, Wins!"

        self.slotsFilled += 1
        if self.slotsFilled == 42:
            self.gameEnd = True
            self.checkTie = True
            return output + "\n\nIt's a Tie"

        if self.userTurn == True:
            self.userTurn = False
            output = output + "\n\n<@!" + \
                str(self.opponent) + ">, Make your move!"
        else:
            self.userTurn = True
            output = output + "\n\n<@!" + str(self.user) + ">, Make your move!"

        if self.turn == '🔴':
            self.turn = '🔵'
        else:
            self.turn = '🔴'

        return output

    def checkForVictory(self) -> str:
        #victory by Horizontal
        for c in range(self.COL-3):
            for r in range(self.ROW):
                if (self.board[r][c] == self.turn and self.board[r][c+1] == self.turn
                        and self.board[r][c+2] == self.turn and self.board[r][c+3] == self.turn):
                    return self.turn

        #victory by Vertical
        for c in range(self.COL):
            for r in range(self.ROW-3):
                if (self.board[r][c] == self.turn and self.board[r+1][c] == self.turn
                        and self.board[r+2][c] == self.turn and self.board[r+3][c] == self.turn):
                    return self.turn
        
        #victory by Diagonal
        for c in range(self.COL-3):
            for r in range(self.ROW-3):
                if (self.board[r][c] == self.turn and self.board[r+1][c+1] == self.turn
                        and self.board[r+2][c+2] == self.turn and self.board[r+3][c+3] == self.turn):
                    return self.turn

        for c in range(self.COL-3):
            for r in range(3, self.ROW-3):
                if (self.board[r][c] == self.turn and self.board[r-1][c+1] == self.turn
                        and self.board[r-2][c+2] == self.turn and self.board[r-3][c+3] == self.turn):
                    return self.turn

    def validMove(self, move):
        return self.board[5][self.columnIds.index(move[0].upper())] == '⚪'

    def getOpenRow(self, move):
        for r in range(self.ROW):
            if self.board[r][self.columnIds.index(move[0].upper())] == '⚪':
                print("r", r)
                return r

    def initBoard(self):
        output = ""
        for r in range(self.ROW-1,-1,-1):
            for c in range(self.COL):
                output += self.board[r][c] + " "
            output += '\n'
        output += "🇦 🇧 🇨 🇩 🇪 🇫 🇬\n"
        return output
