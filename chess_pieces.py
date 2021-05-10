from PIL import Image

class ChessPiece:

    global initial
    name: str
    global icons
    value: int
    global color #0 for white, 1 for black

    def __init__(self, initial: str, name: str, onWhiteIcon: Image, onBlackIcon: Image, value: int, color: int ):
        self.initial = initial
        self.name = name
        self.icons = {'white': onWhiteIcon, 'black': onBlackIcon}
        self.value = value
        self.color = color

    #returns true if move is legal; contains rules that apply to every piece,
    #and each type of piece overrides to provide rules specific to subclass
    def canMakeMove( self, fromRow: int, fromColumn: int, toRow: int, toColumn: int, board ) -> bool:
        if board[toRow][toColumn] != None and board[fromRow][fromColumn].color == board[toRow][toColumn].color:
            return False #can't take own piece

    def getCaptured(self):
        return self.value


class Pawn(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Pawn, self).__init__( "P", "Pawn", onWhiteIcon, onBlackIcon, 1, color )

    def canMakeMove( self, fromRow: int, fromColumn: int, toRow: int, toColumn: int, board ) -> bool:
        if super(Pawn, self).canMakeMove( fromRow, fromColumn, toRow, toColumn, board ) == False:
            return False
        #pawns need to move forward
        multiplier = -1
        if self.color == 0:
            multiplier = 1

        distColumn = fromColumn - toColumn
        distRow = fromRow - toRow
        #MOVE: one forward, no horizontal: move to empty space
        if distRow == 1 * multiplier and distColumn == 0 and board[toRow][toColumn] == None:
            return True
        #ATTACK: one forward, horizontal by one: capture piece in destination space
        if distRow == 1 * multiplier and abs(distColumn) == 1 and board[toRow][toColumn] != None:
            return True

        return False #no other valid pawn moves



class Bishop(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Bishop, self).__init__( "B", "Bishop", onWhiteIcon, onBlackIcon, 3, color )

    def canMakeMove( self, fromRow: int, fromColumn: int, toRow: int, toColumn: int, board ) -> bool:
        if super(Bishop, self).canMakeMove( fromRow, fromColumn, toRow, toColumn, board ) == False:
            return False

        distColumn = fromColumn - toColumn
        distRow = fromRow - toRow
        #Bishop must move diagonally
        if abs(distRow) != abs(distColumn):
            return False

        #check for pieces blocking path
        addColumn: int = distColumn / int(abs(distColumn))
        addRow: int = distRow / int(abs(distRow))
        toColumn += addColumn
        toRow += addRow
        while toRow != fromRow:
            #print('checking path at (%s, %s)' % (toRow, toColumn) )

            if board[int(toRow)][int(toColumn)] != None:
                return False
            toColumn += addColumn
            toRow += addRow

        return True



class Knight(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Knight, self).__init__( "K", "Knight", onWhiteIcon, onBlackIcon, 3, color )

    def canMakeMove( self, fromRow: int, fromColumn: int, toRow: int, toColumn: int, board ) -> bool:
        if super(Knight, self).canMakeMove( fromRow, fromColumn, toRow, toColumn, board ) == False:
            return False

        distColumn = abs(fromColumn - toColumn)
        distRow = abs(fromRow - toRow)
        #2,1 jump
        if( distRow == 2 and distColumn == 1 or distRow == 1 and distColumn == 2 ):
            return True
        return False




class Rook(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Rook, self).__init__( "R", "Rook", onWhiteIcon, onBlackIcon, 5, color )

    def canMakeMove( self, fromRow: int, fromColumn: int, toRow: int, toColumn: int, board ) -> bool:
        if super(Rook, self).canMakeMove( fromRow, fromColumn, toRow, toColumn, board ) == False:
            return False

        distColumn = fromColumn - toColumn
        distRow = fromRow - toRow

        #move horizontally
        if distRow == 0 and distColumn != 0:
            # check for pieces blocking path
            addColumn: int = distColumn / int(abs(distColumn))
            toColumn += addColumn
            while toColumn != fromColumn:
                if board[int(toRow)][int(toColumn)] != None:
                    return False
                toColumn += addColumn

            return True

        #move vertically
        if distColumn == 0 and distRow != 0:
            # check for pieces blocking path
            addRow: int = distRow / int(abs(distRow))
            toRow += addRow
            while toRow != fromRow:
                if board[int(toRow)][int(toColumn)] != None:
                    return False
                toRow += addRow

            return True

        #not horizontal or vertical move
        return False



class King(ChessPiece):
    #'K' is initial for knight, so we'll use 'S' for sovereign
    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(King, self).__init__( "S", "King", onWhiteIcon, onBlackIcon, -1, color )

    def canMakeMove( self, fromRow: int, fromColumn: int, toRow: int, toColumn: int, board ) -> bool:
        if super(King, self).canMakeMove( fromRow, fromColumn, toRow, toColumn, board ) == False:
            return False
        #can't move King next to opponent's King
        #handled here as opposed to isInCheck to avoid endless recursion call
        for i in range(-1, 2):
            for j in range(-1, 2):
                r = toRow + i
                c = toColumn + j
                if r >= 0 and r <= 4 and c >= 0 and c <= 3:
                    if board[r][c] != None and board[r][c].value == -1 and board[r][c].color != self.color:
                        return False

        distColumn = abs(fromColumn - toColumn)
        distRow = abs(fromRow - toRow)
        #one space in any direction
        return (distRow <= 1 and distColumn <= 1) and (distRow == 1 or distColumn == 1)


class Queen(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Queen, self).__init__( "Q", "Queen", onWhiteIcon, onBlackIcon, 9, color)

    def canMakeMove( self, fromRow: int, fromColumn: int, toRow: int, toColumn: int, board ) -> bool:
        distColumn = fromColumn - toColumn
        distRow = fromRow - toRow

        # move horizontally
        if distRow == 0 and distColumn != 0:
            # check for pieces blocking path
            addColumn: int = distColumn / int(abs(distColumn))
            toColumn += addColumn
            while toColumn != fromColumn:
                if board[int(toRow)][int(toColumn)] != None:
                    return False
                toColumn += addColumn

            return True

        # move vertically
        if distColumn == 0 and distRow != 0:
            # check for pieces blocking path
            addRow: int = distRow / int(abs(distRow))
            toRow += addRow
            while toRow != fromRow:
                if board[int(toRow)][int(toColumn)] != None:
                    return False
                toRow += addRow

            return True

        #move diagonally
        if abs(distColumn) == abs(distRow):
            addColumn: int = distColumn / int(abs(distColumn))
            addRow: int = distRow / int(abs(distRow))
            toColumn += addColumn
            toRow += addRow
            while toRow != fromRow:
                # print('checking path at (%s, %s)' % (toRow, toColumn) )

                if board[int(toRow)][int(toColumn)] != None:
                    return False
                toColumn += addColumn
                toRow += addRow

            return True
        #illegal move
        return False