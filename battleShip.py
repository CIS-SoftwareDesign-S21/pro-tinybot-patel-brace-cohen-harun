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



    def putShip( board, sizeOfShip): #put a ship on a board


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

    # check each turn if someone won and end game if so
    def checkVictoryStatus(self) -> str:

        #check the user board to see if the comp won
        #loop through board, if there are no o then comp won
        compWon = 1
        for r in range(0,4):
            for c in range(0,4):
                if(self.userBoard[r][c] == ' o '):
                    compWon=0

        #check the comp board to see if the user won
        #check if there are 9 x because thats how many ship spaces there are
        userWon =1
        numx=0
        for r in range(0,5):
            for c in range(0,5):
                if(self.comBoardToShowUser[r][c] == ' x '):
                    numx += 1

        if numx < 9:
            userWon =0

        if(compWon ==1):#if the computer won
            return "The computer won!"
        elif(userWon == 1):
            return "You won!"
        else: #if neither has won yet
            return "no"

    def makeMove(self, move) -> str:
        output: str = '\n'

        try: #accept move from player; ask again if input is not correct
            #possibilities, repeat spot, hit ship, hit nothing
            if(self.comBoardToShowUser[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] == ' m ' or self.comBoardToShowUser[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] == ' x ' ):#first check if it is a repeat spot
                output+= '\nYou picked a repeat space\n'
            elif self.comBoard[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] == ' - ':#you hit an empty spot
                self.comBoardToShowUser[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] = ' m '#show the user that they hit an empty spot
                output += "\nYou missed\n"
                #self.comBoard[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] = self.turn
            elif(self.comBoard[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] == ' o '):#they hit a part of a ship
                self.comBoardToShowUser[self.rowIDs.index(move[0].upper())][
                    int(move[1]) - 1] = ' x '  # show the user that they hit a ship
                output += "\nYou hit their ship\n"
            else:
                return '\nI did not account for this option in the code.\n'

        except (IndexError, ValueError):
            return 'Please input special key \'#\', followed by letter A,B,C,D or E to select row, and integer 1-5 to select column.'







        # AFTER YOU MAKE YOUR MOVE, THE COMPUTER MAKES A MOVE
        #pick a random row and col and that is the move
        comprow = random.randint(0, 4)
        compcol = random.randint(0, 4)
        output += "\nThe computer picked spot " + self.rowIDs[comprow] + str(compcol+1)+ "\n"

        if (self.userBoard[comprow][compcol] == ' m ' or self.userBoard[comprow][compcol] == ' x '):  # first check if it is a repeat spot
            output+= '\nThe computer picked a repeat space\n'
        elif self.userBoard[comprow][compcol] == ' - ':  # computer hit an empty spot
            self.userBoard[comprow][compcol] = ' m '  # show the computer that they hit an empty spot
            output += "\nThe computer missed\n"
            # self.comBoard[ self.rowIDs.index( move[0].upper() ) ][ int( move[1] ) - 1] = self.turn
        elif (self.userBoard[comprow][compcol] == ' o '):  # computer hit a part of a ship
            self.userBoard[comprow][compcol] = ' x '  # show the user that computer hit a ship
            output += "\nThe computer hit your ship\n"
        else:
            return '\nI did not account for this option in the code.\n'



        # create text representation of the board
        output += "\nWhat you know about the opponent's board: \n"
        for i in range(0, 5):
            output += ('%s %s %s %s %s\n' % (
            self.comBoardToShowUser[i][0], self.comBoardToShowUser[i][1], self.comBoardToShowUser[i][2],
            self.comBoardToShowUser[i][3], self.comBoardToShowUser[i][4]))

        output += "\nYour board: \n"
        for i in range(0, 5):
            output += ('%s %s %s %s %s\n' % (
            self.userBoard[i][0], self.userBoard[i][1], self.userBoard[i][2], self.userBoard[i][3],
            self.userBoard[i][4]))

        output += "\nThe computer's real board: \n"
        for i in range(0, 5):
            output += ('%s %s %s %s %s\n' % (
                self.comBoard[i][0], self.comBoard[i][1], self.comBoard[i][2],
                self.comBoard[i][3], self.comBoard[i][4]))

        #check for victory
        victoryStatus = "no"
        victoryStatus = self.checkVictoryStatus();
        if(victoryStatus != "no"):#if someone has won
            output+= "\n" + str(victoryStatus) + "\n"
            return output

        return output