import discord
import os
import random

class BattleShipGame:
    comBoard = [
        [' - ', ' - ', ' - ',' - ', ' - '],
        [' - ', ' - ', ' - ',' - ', ' - '],
        [' - ', ' - ', ' - ',' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - ']
    ]

    comBoardToShowUser = [
        [' - ', ' - ', ' - ', ' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - ']
    ]


    userBoard = [
        [' - ', ' - ', ' - ',' - ', ' - '],
        [' - ', ' - ', ' - ',' - ', ' - '],
        [' - ', ' - ', ' - ',' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - '],
        [' - ', ' - ', ' - ', ' - ', ' - ']
    ]

    rowIDs = ['A', 'B', 'C', 'D', 'E']



    def putShip( board, sizeOfShip):


        orientation = 0
        #choose a random number 1 or 2, 1 for horizontal 2 for vertical
        orientation = random.randint(1, 2)
        #choose a location for the first space of the ship
        row = random.randint(0,4)
        col = random.randint(0,4)
        validSpot =0

        while(validSpot == 0):#keep choosing until it finds a valid spot
            row = random.randint(0, 4)
            col = random.randint(0, 4)
            validSpot = 1
            #check each spot of the ship to see if it is out of bounds or intersecting another ship
            for i in range(0, sizeOfShip):
                if(orientation == 1):#if horizontal
                    if((col + i) >=5):#if out of bounds
                        validSpot = 0
                    elif(board[row][col+i] != ' - '):#if spot is taken by another ship
                        validSpot = 0
                elif(orientation == 2):# if vetical
                    if((row + i) >= 5 ):
                        validSpot = 0
                    elif (board[row+i][col] != ' - '):  # if spot is taken by another ship
                        validSpot = 0

        #now that we checked the spot, we can put the ship in
        for i in range(0,sizeOfShip):
            if(orientation ==1): #if horizontal
                board[row][col +i] = ' o '
            elif(orientation ==2): #if vertical
                board[row+i][col] = ' o '



    # fill the comBoard with three ships randomly
    # one ship length 2, one length 3, one length 4 no overlapping!
    putShip(comBoard, 4)  # put in length 4 ship
    putShip(comBoard, 3)  # put in length 3 ship
    putShip(comBoard, 2)  # put in length 2 ship

    # i guess fill the user board with three ships randomly
    putShip(userBoard, 4)  # put in length 4 ship
    putShip(userBoard, 3)  # put in length 3 ship
    putShip(userBoard, 2)  # put in length 2 ship

    def makeMove(self, move) -> str:

        #try: #accept move from player; ask again if input is not correct
            #if self.comBoard[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] == ' - ':
                #self.comBoard[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] = self.turn
            #else:
                #return 'This square has already been taken.'

        #except (IndexError, ValueError):
            #return 'Please input special key \'#\', followed by letter A,B,C,D or E to select row, and integer 1-5 to select column.'


        output: str = '\n'
        #create text representation of the board
        output += "\nWhat you know about the opponent's board: \n"
        for i in range(0,5):
            output += ('%s %s %s %s %s\n' % (self.comBoardToShowUser[i][0],self.comBoardToShowUser[i][1], self.comBoardToShowUser[i][2], self.comBoardToShowUser[i][3], self.comBoardToShowUser[i][4] ))

        output += "\nYour board: \n"
        for i in range(0, 5):
            output += ('%s %s %s %s %s\n' % (self.userBoard[i][0], self.userBoard[i][1], self.userBoard[i][2],self.userBoard[i][3], self.userBoard[i][4]))

        output += "\nThe computer's real board: \n"
        for i in range(0, 5):
            output += ('%s %s %s %s %s\n' % (
            self.comBoard[i][0], self.comBoard[i][1], self.comBoard[i][2],
            self.comBoard[i][3], self.comBoard[i][4]))

        return output