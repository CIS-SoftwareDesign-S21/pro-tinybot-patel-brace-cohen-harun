
board = [
    [ '-', '-', '-' ],
    [ '-', '-', '-' ],
    [ '-', '-', '-' ]
]

rowIDs = [ 'A', 'B', 'C' ]

turn = 'O'
squaresFilled = 0

#check each turn if someone won and end game if so
def checkForVictory():

    for j in range( 0, 3 ):
        #row victory, column victory, diagonal  top left-> bottom right, and diagonal top right -> bottom left, respectively
        if ( board[j][0] != '-' and board[j][0] == board[j][1] and board[j][1] == board[j][2] ) \
        or ( board[0][j] != '-' and board[0][j] == board[1][j] and board[1][j] == board[2][j]  )\
        or ( board[0][0] != '-' and board[0][0] == board[1][1] and board[1][1] == board[2][2] )\
        or ( board[0][2] != '-' and board[0][2] == board[1][1] and board[1][1] == board[2][0] ):
            print( '%s wins!' % turn )
            exit(0)



#main
while True:

    try: #accept move from player; ask again if input is not correct
        move = input( '%c\'s move: ' % turn )
        if board[ rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] == '-':
            board[ rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] = turn
        else:
            print( 'This square has already been taken.' )
            continue

    except (IndexError, ValueError):
        print( 'Please input a letter A,B, or C to select row, followed by integer 1-3 to select column.' )
        continue

    print()
    #print board to screen
    for i in range(0, 3):
        print( '%c | %c | %c' % (board[i][0], board[i][1], board[i][2]) )
        if i < 2:
            print( '----------' )

    print()
    checkForVictory()

    squaresFilled += 1
    if squaresFilled == 9:
        print( 'It\'s a tie!' )
        exit(0)

    if turn == 'O':
        turn = 'X'
    else:
        turn = 'O'


