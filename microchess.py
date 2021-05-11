from PIL import Image
from chess_pieces import *
import io
import copy

#Images for border surrounding the chess board
img_A = Image.open('microchess-assets/BORDER/A.png')
img_B = Image.open('microchess-assets/BORDER/B.png')
img_C = Image.open('microchess-assets/BORDER/C.png')
img_D = Image.open('microchess-assets/BORDER/D.png')
letterImages = [ img_A, img_B, img_C, img_D ]
img_1 = Image.open('microchess-assets/BORDER/ONE.png')
img_2 = Image.open('microchess-assets/BORDER/TWO.png')
img_3 = Image.open('microchess-assets/BORDER/THREE.png')
img_4 = Image.open('microchess-assets/BORDER/FOUR.png')
img_5 = Image.open('microchess-assets/BORDER/FIVE.png')
numImages = [ img_5, img_4, img_3, img_2, img_1 ]

#Images for all of White's pieces
img_whitePawn_onWhite = Image.open('microchess-assets/ON-WHITE/WHITE-PAWN.png')
img_whitePawn_onBlack = Image.open('microchess-assets/ON-BLACK/WHITE-PAWN.png')
img_whiteBishop_onWhite = Image.open('microchess-assets/ON-WHITE/WHITE-BISHOP.png')
img_whiteBishop_onBlack = Image.open('microchess-assets/ON-BLACK/WHITE-BISHOP.png')
img_whiteKnight_onWhite = Image.open('microchess-assets/ON-WHITE/WHITE-KNIGHT.png')
img_whiteKnight_onBlack = Image.open('microchess-assets/ON-BLACK/WHITE-KNIGHT.png')
img_whiteRook_onWhite = Image.open('microchess-assets/ON-WHITE/WHITE-ROOK.png')
img_whiteRook_onBlack = Image.open('microchess-assets/ON-BLACK/WHITE-ROOK.png')
img_whiteKing_onWhite = Image.open('microchess-assets/ON-WHITE/WHITE-KING.png')
img_whiteKing_onBlack = Image.open('microchess-assets/ON-BLACK/WHITE-KING.png')
img_whiteQueen_onWhite = Image.open('microchess-assets/ON-WHITE/WHITE-QUEEN.png')
img_whiteQueen_onBlack = Image.open('microchess-assets/ON-BLACK/WHITE-QUEEN.png')
#Images for all of Black's pieces
img_blackPawn_onWhite = Image.open('microchess-assets/ON-WHITE/BLACK-PAWN.png')
img_blackPawn_onBlack = Image.open('microchess-assets/ON-BLACK/BLACK-PAWN.png')
img_blackBishop_onWhite = Image.open('microchess-assets/ON-WHITE/BLACK-BISHOP.png')
img_blackBishop_onBlack = Image.open('microchess-assets/ON-BLACK/BLACK-BISHOP.png')
img_blackKnight_onWhite = Image.open('microchess-assets/ON-WHITE/BLACK-KNIGHT.png')
img_blackKnight_onBlack = Image.open('microchess-assets/ON-BLACK/BLACK-KNIGHT.png')
img_blackRook_onWhite = Image.open('microchess-assets/ON-WHITE/BLACK-ROOK.png')
img_blackRook_onBlack = Image.open('microchess-assets/ON-BLACK/BLACK-ROOK.png')
img_blackKing_onWhite = Image.open('microchess-assets/ON-WHITE/BLACK-KING.png')
img_blackKing_onBlack = Image.open('microchess-assets/ON-BLACK/BLACK-KING.png')
img_blackQueen_onWhite = Image.open('microchess-assets/ON-WHITE/BLACK-QUEEN.png')
img_blackQueen_onBlack = Image.open('microchess-assets/ON-BLACK/BLACK-QUEEN.png')


#creates object representing game; called upon by bot
class MicrochessGame:

    #class constants
    columnIDs = ['A', 'B', 'C', 'D']
    rowIDs = ['5', '4', '3', '2', '1']
    playerNames = ['White', 'Black']
    emptySquares = {'white': Image.open('microchess-assets/ON-WHITE/EMPTY.png'), 'black': Image.open('microchess-assets/ON-BLACK/EMPTY.png')}

    def __init__(self, whiteUser, blackUser):
        self.userAccounts = [whiteUser, blackUser]
        self.turn = 0
        self.whitePoints = 0
        self.blackPoints = 0
        self.playerScores = [self.whitePoints, self.blackPoints]
        self.gameCompleted = False

        self.white = { 'P': Pawn(img_whitePawn_onWhite, img_whitePawn_onBlack, 0),
                   'B': Bishop(img_whiteBishop_onWhite, img_whiteBishop_onBlack, 0),
                   'K': Knight(img_whiteKnight_onWhite, img_whiteKnight_onBlack, 0),
                   'R': Rook(img_whiteRook_onWhite, img_whiteRook_onBlack, 0),
                   'S': King(img_whiteKing_onWhite, img_whiteKing_onBlack, 0)
        }

        self.black = { 'P': Pawn(img_blackPawn_onWhite, img_blackPawn_onBlack, 1),
                   'B': Bishop(img_blackBishop_onWhite, img_blackBishop_onBlack, 1),
                   'K': Knight(img_blackKnight_onWhite, img_blackKnight_onBlack, 1),
                   'R': Rook(img_blackRook_onWhite, img_blackRook_onBlack, 1),
                   'S': King(img_blackKing_onWhite, img_blackKing_onBlack, 1)
        }

        self.players = [self.white, self.black]

        self.board = [
            [self.black['S'], self.black['K'], self.black['B'], self.black['R']],
            [self.black['P'], None, None, None],
            [None, None, None, None],
            [None, None, None, self.white['P']],
            [self.white['R'], self.white['B'], self.white['K'], self.white['S']]
        ]

        self.queens = [Queen(img_whiteQueen_onWhite, img_whiteQueen_onBlack, 0), Queen(img_blackQueen_onWhite, img_blackQueen_onBlack, 1)]


    def makeMove(self, move: str):
        if move == 'forf':
            self.gameCompleted = True
            return '%s has forfeited! Game over.' % self.userAccounts[self.turn].mention, False

        try:
            selectedPiece = self.players[self.turn][move[0].upper()]
        except:
            return 'This piece doesn\'t exist.', False

        toColumn: int = int(self.columnIDs.index(move[1].upper()))
        toRow: int = self.rowIDs.index(move[2])
        fromRow: int
        fromColumn: int
        fromRow, fromColumn = self.findPiece(move[0].upper())

        output = ''

        if fromRow == None:
            output += 'This piece has been captured.'
            return output, False

        if self.wouldCauseCheck(int(fromRow), int(fromColumn), int(toRow), int(toColumn)):
            return 'You can\'t put/leave your own King in Check!', False

        #print('Attempting to move %s from (%s, %s) to (%s, %s).' % ( selectedPiece.name, fromRow, fromColumn, toRow, toColumn))

        if selectedPiece.canMakeMove(int(fromRow), int(fromColumn), int(toRow), int(toColumn), self.board):
            #if piece is captured, make record of material value
            if self.board[toRow][toColumn] != None:
                self.playerScores[self.turn] += self.board[toRow][toColumn].getCaptured()
                #if king is victim, end game
                #if self.board[toRow][toColumn].getCaptured() == -1:
                    #output += "%s has won the game!" % self.userAccounts[self.turn].mention
                    #self.board[toRow][toColumn] = self.board[fromRow][fromColumn]
                    #self.board[fromRow][fromColumn] = None
                    #self.gameCompleted = True
                    #return output, True

                output += '%s has now captured %d point(s) worth of material.\n' % (self.playerNames[self.turn], self.playerScores[self.turn])
                # if only Kings left, declare stalemate
                if self.playerScores[0] >= 12 and self.playerScores[1] >= 12:
                    output += 'Stalemate! Game over.'
                    self.board[toRow][toColumn] = self.board[fromRow][fromColumn]
                    self.board[fromRow][fromColumn] = None
                    self.gameCompleted = True
                    return output, True

            #if non-king captured or no capture on turn, move pieces & announce next move
            self.board[toRow][toColumn] = self.board[fromRow][fromColumn]
            self.board[fromRow][fromColumn] = None

            #pawns are queened if they reach the end of the board
            if(self.board[toRow][toColumn].color == self.turn and self.board[toRow][toColumn].initial == 'P' and (toRow == 0 or toRow == 4) ):
                self.board[toRow][toColumn] = self.queens[self.turn]
                self.players[self.turn]['Q'] = self.board[toRow][toColumn]
                self.players[self.turn]['P'] = None
                output += '%s has queened their pawn.\n' % self.playerNames[self.turn]

            #if opp. king is in check, add to message
            if self.isInCheck():
                if self.isInCheckmate():
                    output += "Checkmate! %s has won the game!" % self.userAccounts[self.turn].mention
                    self.gameCompleted = True
                    return output, True

                output += 'King is in Check. '
            elif self.isInCheckmate(): #not actually checkmate; this is testing for stalemate with > 2 pieces on board
                output += "Stalemate! Game over."
                self.gameCompleted = True
                return output, True

            self.changeTurn()
            output += '%s\'s move!' % self.userAccounts[self.turn].mention
            return output, True
        else:
            output += 'This is an invalid move.'
            return output, False


    def genBoardImage(self):
        turnResult = Image.new('RGB', (260, 312))
        for column in range(0, 4):
            turnResult.paste(letterImages[column], (52 + column * 52, 0))
        for row in range(0, 5):
            turnResult.paste(numImages[row], (0, 52 + row * 52))

        x = 52
        y = 52
        output = ''
        self.space = 'black'

        for row in self.board:
            for piece in row:
                if piece == None:
                    turnResult.paste(self.emptySquares[self.space], (x, y))
                else:
                    turnResult.paste(piece.icons[self.space], (x, y))
                x += 52  # next spot over
                self.changeSpaceColor()

            x = 52  # next row
            y += 52
            self.changeSpaceColor()

        #return turnResult
        turnResult.save('board.png')
        #with io.BytesIO() as delivery:
            #turnResult.save(delivery, format='PNG')
            #delivery.seek(0)
            ##return delivery
        return 'board.png'

    def changeSpaceColor(self):
        if self.space == 'black':
            self.space = 'white'
        else:
            self.space = 'black'

    def changeTurn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

        #print('It is now %s\'s turn.' % self.playerNames[self.turn])

    def findPiece(self, c):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])): #now allows for deep copy in check protection
                if self.board[i][j] != None and self.board[i][j].color == self.turn and self.board[i][j].initial == c:
                    return i, j
        return None, None

    def isInCheck(self):

        if self.turn == 0:
            defending = 1
        else:
            defending = 0
        kx = -1
        ky = -1
        #find (x,y) coord. of defending side's King
        for i in range(0, 5):
            for j in range(0, 4):
                if self.board[i][j] != None and self.board[i][j].color == defending  and self.board[i][j].initial == 'S':
                    kx = i
                    ky = j

        #for each piece on side that just moved, ID any check condition(s)
        for i in range(0, 5):
            for j in range(0, 4):
                if self.board[i][j] != None and self.board[i][j].initial != 'S' and self.board[i][j].color == self.turn:
                    if self.board[i][j].canMakeMove( i, j, kx, ky, self.board ):
                        return True

        return False


    def wouldCauseCheck(self, fromRow: int, fromColumn: int, toRow: int, toColumn: int ):
        if self.turn == 0:
            otherPlayer = 1
        else:
            otherPlayer = 0

        #if you have nothing left but King, game will let you
        #move him into check so that game does not freeze
        #if self.playerScores[otherPlayer] > 11:
            #return False

        bCopy = copy.deepcopy(self.board)
        self.board[toRow][toColumn] = self.board[fromRow][fromColumn]
        self.board[fromRow][fromColumn] = None

        self.changeTurn()
        output = False
        if self.isInCheck():
            output = True

        self.board = bCopy
        self.changeTurn()
        return output


    def isTurnOf(self, userID):
        return userID == self.userAccounts[self.turn].id


    def isInCheckmate(self):
        if self.turn == 0:
            defending = 1
        else:
            defending = 0

        bCopy = copy.deepcopy(self.board)
        #for each piece on defending side
        for r in range(0, 5):
            for c in range(0, 4):
                if self.board[r][c] != None and self.board[r][c].color == defending:
                    #for every spot on board
                    for x in range(0, 5):
                        for y in range(0, 4):
                            #if there exists a legal move that kills check, not in checkmate
                            if self.board[r][c].canMakeMove( r, c, x, y, bCopy ):
                                self.board[x][y] = self.board[r][c]
                                self.board[r][c] = None
                                if not self.isInCheck():
                                    self.board = bCopy
                                    bCopy = copy.deepcopy(self.board)
                                    return False
                                self.board = bCopy
                                bCopy = copy.deepcopy(self.board)
        #in checkmate if no legal paths out of check
        return True
