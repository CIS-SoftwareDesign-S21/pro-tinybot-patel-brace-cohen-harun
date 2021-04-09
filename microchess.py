from PIL import Image
from chess_pieces import *

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
img_whiteKing_onBlack = Image.open('microchess-assets/ON-BLACK/WHITE-ROOK.png')
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
img_blackKing_onBlack = Image.open('microchess-assets/ON-BLACK/BLACK-ROOK.png')


class MicrochessGame:

    white = { 'P': Pawn(img_whitePawn_onWhite, img_whitePawn_onBlack, 0),
               'B': Bishop(img_whiteBishop_onWhite, img_whiteBishop_onBlack, 0),
               'K': Knight(img_whiteKnight_onWhite, img_whiteKnight_onBlack, 0),
               'R': Rook(img_whiteRook_onWhite, img_whiteRook_onBlack, 0 ),
               'K!': King(img_whiteKing_onWhite, img_whiteKing_onBlack, 0 )
    }

    black = { 'P': Pawn(img_blackPawn_onWhite, img_blackPawn_onBlack, 1),
               'B': Bishop(img_blackBishop_onWhite, img_blackBishop_onBlack, 1),
               'K': Knight(img_blackKnight_onWhite, img_blackKnight_onBlack, 1),
               'R': Rook(img_blackRook_onWhite, img_blackRook_onBlack, 1),
               'K!': King(img_blackKing_onWhite, img_blackKing_onBlack, 1)
    }

    emptySquares = { 'white': Image.open('microchess-assets/ON-WHITE/EMPTY.png'), 'black': Image.open('microchess-assets/ON-BLACK/EMPTY.png')}

    board = [
        [black['K!'], black['K'], black['B'], black['R']],
        [black['P'], None, None, None],
        [None, None, None, None],
        [None, None, None, white['P']],
        [white['R'], white['B'], white['K'], white['K!']]
    ]

#main
game = MicrochessGame()
turnResult = Image.new('RGB', (208, 260))
x= 0
y = 0
output = ''
space = 'black'

def changeSpaceColor():
    global space
    if space == 'black':
        space = 'white'
    else:
        space = 'black'

#main cont.
for row in game.board:
    for piece in row:
        if piece == None:
            turnResult.paste(game.emptySquares[space], (x, y))
        else:
            turnResult.paste(piece.icons[space], (x, y))
        x += 52 #next spot over
        changeSpaceColor()

    x = 0 #next row
    y += 52
    changeSpaceColor()

turnResult.save('board.png')