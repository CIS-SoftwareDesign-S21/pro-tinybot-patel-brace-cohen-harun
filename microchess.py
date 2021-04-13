from PIL import Image
from chess_pieces import *
import io

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


#creates object representing game; called upon by bot
class MicrochessGame:

    turn = 0
    columnIDs = ['A', 'B', 'C', 'D']
    rowIDs = ['5', '4', '3', '2', '1']

    white = { 'P': Pawn(img_whitePawn_onWhite, img_whitePawn_onBlack, 0),
               'B': Bishop(img_whiteBishop_onWhite, img_whiteBishop_onBlack, 0),
               'K': Knight(img_whiteKnight_onWhite, img_whiteKnight_onBlack, 0),
               'R': Rook(img_whiteRook_onWhite, img_whiteRook_onBlack, 0),
               'S': King(img_whiteKing_onWhite, img_whiteKing_onBlack, 0)
    }

    black = { 'P': Pawn(img_blackPawn_onWhite, img_blackPawn_onBlack, 1),
               'B': Bishop(img_blackBishop_onWhite, img_blackBishop_onBlack, 1),
               'K': Knight(img_blackKnight_onWhite, img_blackKnight_onBlack, 1),
               'R': Rook(img_blackRook_onWhite, img_blackRook_onBlack, 1),
               'S': King(img_blackKing_onWhite, img_blackKing_onBlack, 1)
    }

    players = [white, black]
    playerNames = ['White', 'Black']

    emptySquares = { 'white': Image.open('microchess-assets/ON-WHITE/EMPTY.png'), 'black': Image.open('microchess-assets/ON-BLACK/EMPTY.png')}

    board = [
        [black['S'], black['K'], black['B'], black['R']],
        [black['P'], None, None, None],
        [None, None, None, None],
        [None, None, None, white['P']],
        [white['R'], white['B'], white['K'], white['S']]
    ]


    def makeMove(self, move: str):
        try:
            selectedPiece = self.players[self.turn][move[0].upper()]
        except:
            return 'This piece doesn\'t exist.', False

        toColumn: int = int(self.columnIDs.index(move[1].upper()))
        toRow: int = self.rowIDs.index(move[2])
        fromRow, fromColumn = self.findPiece(move[0].upper())

        output = ''

        if fromRow == None:
            output += "This piece has been captured."
            return output, False

        #print('Attempting to move %s from (%s, %s) to (%s, %s).' % ( selectedPiece.name, fromRow, fromColumn, toRow, toColumn))

        if selectedPiece.canMakeMove(int(fromRow), int(fromColumn), int(toRow), int(toColumn), self.board):
            self.board[toRow][toColumn] = self.board[fromRow][fromColumn]
            self.board[fromRow][fromColumn] = None
            self.changeTurn()
            output += "%s\'s move!" % self.playerNames[self.turn]
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

    def findPiece(self, c):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == self.players[self.turn][c]:
                    return i, j
        return None, None