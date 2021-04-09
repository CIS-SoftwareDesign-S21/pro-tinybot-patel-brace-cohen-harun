from PIL import Image

class ChessPiece:

    initial: str
    name: str
    global icons
    value: int
    color: int #0 for white, 1 for black

    def __init__(self, initial: str, name: str, onWhiteIcon: Image, onBlackIcon: Image, value: int, color: int ):
        self.initial = initial
        self.name = name
        self.icons = {'white': onWhiteIcon, 'black': onBlackIcon}
        self.value = value
        self.color = color

    def makeMove( x: int, y: int ):
        pass

    def getCaptured():
        pass

class Pawn(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Pawn, self).__init__( "P", "Pawn", onWhiteIcon, onBlackIcon, 1, color )


class Bishop(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Bishop, self).__init__( "B", "Bishop", onWhiteIcon, onBlackIcon, 3, color )

class Knight(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Knight, self).__init__( "K", "Knight", onWhiteIcon, onBlackIcon, 3, color )

class Rook(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(Rook, self).__init__( "R", "Rook", onWhiteIcon, onBlackIcon, 5, color )

class King(ChessPiece):

    def __init__(self, onWhiteIcon: Image, onBlackIcon: Image, color: int ):
        super(King, self).__init__( "K!", "King", onWhiteIcon, onBlackIcon, -1, color )