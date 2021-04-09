import discord
import os

class TicTacToeGame:

    def __init__(self, user, opponent, userTurn, checkWin, gameEnd, checkTie):
        self.user = user
        self.opponent = opponent
        self.userTurn = userTurn
        self.checkWin = checkWin
        self.gameEnd = gameEnd
        self.checkTie = checkTie

    board = [
        [ '⬜', '⬜', '⬜' ],
        [ '⬜', '⬜', '⬜' ],
        [ '⬜', '⬜', '⬜' ]
    ]

    rowIDs = [ 'A', 'B', 'C' ]
    turn: str = '⭕'
    squaresFilled = 0

    #check each turn if someone won and end game if so
    def checkForVictory(self) -> str:

        for j in range( 0, 3 ):
            #row victory, column victory
            if ( self.board[j][0] != '⬜' and self.board[j][0] == self.board[j][1] and self.board[j][1] == self.board[j][2] ) \
            or ( self.board[0][j] != '⬜' and self.board[0][j] == self.board[1][j] and self.board[1][j] == self.board[2][j]  ):
                self.checkWin = True
                self.gameEnd = True
                return ''.join( '%s wins!' % self.turn )

        #victory by diagonal  top left-> bottom right, or diagonal top right -> bottom left
        if (self.board[0][0] != '⬜' and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]) \
        or (self.board[0][2] != '⬜' and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]):
            self.checkWin = True
            self.gameEnd = True
            return ''.join('%s wins!' % self.turn)


    def makeMove(self, move ) -> str:

        try: #accept move from player; ask again if input is not correct
            # if self.board[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] == '⬜':
            #     self.board[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] = self.turn
            if self.board[ int( move[1] ) - 1][ self.rowIDs.index( move[0].upper() ) ] == '⬜':
                self.board[ int( move[1] ) - 1][ self.rowIDs.index( move[0].upper() ) ] = self.turn
            else:
                return 'Error: This square has already been taken.'

        except (IndexError, ValueError):
            return 'Error: Please input special key \'^\', followed by letter A,B, or C to select row, and integer 1-3 to select column.'
        output = self.initBoard()

        victoryStatus = str(self.checkForVictory())

        #check if tie
        self.squaresFilled += 1
        if self.squaresFilled == 9:
            self.checkTie = True
            self.gameEnd = True
            return output + '\n\nIt\'s a tie!'


        if self.turn == '⭕':
            self.turn = '❌'
        else:
            self.turn = '⭕'

        if victoryStatus == 'None':
            return output

        return output + '\n\n' + victoryStatus

    def initBoard(self):
        output: str = '\n'
        # create text representation of board
        output += ("%s" % ':hash: ')
        output += ("%s" % ':regional_indicator_a:  ')
        output += ('%6s' % ':regional_indicator_b:  ')
        output += ('%7s' % ':regional_indicator_c:  ')
        output += '\n'
        for i in range(0, 3):
            if(i == 0):
                output += ':one: '
            elif(i == 1):
                output += ':two: '
            elif(i == 2):
                output += ':three: '
            output += ('%s  %s  %s' % (self.board[i][0], self.board[i][1], self.board[i][2]))
            if i < 2:
                output += '\n'
        return output

    def clearBoard(self):
        self.board = [
            [ '⬜', '⬜', '⬜' ],
            [ '⬜', '⬜', '⬜' ],
            [ '⬜', '⬜', '⬜' ]
        ]
        return
