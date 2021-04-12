from PIL import Image
from chess_pieces import *

#image for border surrounding the chess board
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


class MicrochessGame:

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

    emptySquares = { 'white': Image.open('microchess-assets/ON-WHITE/EMPTY.png'), 'black': Image.open('microchess-assets/ON-BLACK/EMPTY.png')}

    board = [
        [black['S'], black['K'], black['B'], black['R']],
        [black['P'], None, None, None],
        [None, None, None, None],
        [None, None, None, white['P']],
        [white['R'], white['B'], white['K'], white['S']]
    ]

#main - init
game = MicrochessGame()
turn = 0
columnIDs = ['A', 'B', 'C', 'D']
rowIDs = [ '5', '4', '3', '2', '1' ]

#utility functions for managing MicrochessGame obj.
def changeSpaceColor():
    global space
    if space == 'black':
        space = 'white'
    else:
        space = 'black'


def changeTurn():
    global turn
    if turn == 0:
        turn = 1
    else:
        turn = 0


def findPiece(c):
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            if game.board[i][j] == game.players[turn][c]:
                return i, j
    return None, None


#game loop
while True:
    turnResult = Image.new('RGB', (260, 312))
    for column in range(0, 4):
        turnResult.paste( letterImages[column], (52 + column * 52, 0) )
    for row in range(0, 5):
        turnResult.paste( numImages[row], (0, 52 + row * 52) )

    x = 52
    y = 52
    output = ''
    space = 'black'

    for row in game.board:
        for piece in row:
            if piece == None:
                turnResult.paste( game.emptySquares[space], (x, y) )
            else:
                turnResult.paste( piece.icons[space], (x, y) )
            x += 52 #next spot over
            changeSpaceColor()

        x = 52 #next row
        y += 52
        changeSpaceColor()

    turnResult.save( 'board.png' )

    while True:
        playerNames = ['White', 'Black']
        move = input( '%s\'s move: ' % playerNames[turn] )
        selectedPiece = game.players[turn][move[0].upper()]
        toColumn: int = int( columnIDs.index(move[1].upper() ))
        toRow: int = rowIDs.index(move[2])

        fromRow, fromColumn = findPiece( move[0].upper() )
        if fromRow == None:
            print("This piece has been captured.")
            continue

        print('Attempting to move %s from (%s, %s) to (%s, %s).' % (selectedPiece.name, fromRow, fromColumn, toRow, toColumn))

        if selectedPiece.canMakeMove( int(fromRow), int(fromColumn), int(toRow), int(toColumn), game.board):
            game.board[toRow][toColumn] = game.board[fromRow][fromColumn]
            game.board[fromRow][fromColumn] = None
            changeTurn()
            break
        else:
            print( 'This is an invalid move.' )