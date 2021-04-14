import random


class blackJack:
    def __init__(self):
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        self.symbol = ['♡', '♢', '♤', '♧']
        self.player = []
        self.dealer = []
        self.bust = 0
        self.total = 0
        self.totalDealer = 0
        self.done = 0
        self.isACE = 0

    def start(self):
        random.shuffle(self.cards)
        self.dealer.append(self.cards.pop() + random.choice(self.symbol))
        for i in range (0,2):
            self.player.append(self.cards.pop() + random.choice(self.symbol))


    def choice(self,move):
        self.total = self.sum(self.player)

        if(move == "H"):
            self.player.append(self.cards.pop() + random.choice(self.symbol))
            self.total = self.sum(self.player)
            if(self.total > 21):
                self.done = 1
                self.bust = 1
        elif(move == "S"):
            self.total = self.sum(self.player)
            self.done = 1
        return self.checkBoard()
            # self.result()

    def result(self):
        output = ''
        if (self.bust == 1):
            output += "\nBUST!"
            output += "\nPLAYER LOSE"
            return 3
        self.totalDealer = self.sum(self.dealer)
        if(len(self.player) > 4 and self.total<=21):
            output += "\n5 CARDS"
            output += "\nPLAYER WIN"
        if(self.totalDealer > 21):
            output += "\nDEALER BUST!"
            output += "\nPLAYER WIN"
            return 1
        if(self.total < self.totalDealer):
            self.totalDealer = self.sum(self.dealer)
            self.total = self.sum(self.player)
            print("DEALER HAVE: ", self.totalDealer)
            print("PLAYER HAVE: ", self.total)
            output += "\nPLAYER LOSE"
            return output
        elif(self.total == self.totalDealer):
            output += "\nDRAW"
            return 2
        else:
            if(self.total == 21):
                output += "\nBLACKJACK"
            output += "\nPLAYER WIN"
            return 1

    def dealerTurn(self):
        self.totalDealer = self.sum(self.dealer)
        while (self.totalDealer < 21 and self.totalDealer <= self.total and self.bust == 0):
            self.dealer.append(self.cards.pop() + random.choice(self.symbol))
            self.totalDealer = self.sum(self.dealer)
            self.checkBoard()

    def clean(self):
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        self.player = []
        self.dealer = []
        self.bust = 0
        self.total = 0
        self.totalDealer = 0
        self.done = 0
        self.isACE = 0

    def checkBoard(self):
        output = ''
        output += 'DEALER: \n'
        for i in self.dealer:
            output += i
            output += ' | '
        output += '\n'
        output += 'PLAYER: \n'
        for i in self.player:
            output += i
            output += ' | '
        output += '\n\n'
        return output

    def sum(self,arr):
        sum = 0
        for i in range (0,len(arr)):
            if(arr[i][0] == 'J' or arr[i][0] == 'Q' or arr[i][0] == 'K'):
                sum = sum + 10
            elif(arr[i][0] == 'A'):
                sum = sum + 1
                self.isACE = self.isACE + 1
            elif(arr[i][:2] == '10'):
                sum = sum + 10
            else:
                sum = sum + int(arr[i][0])
        while(self.isACE):
            print("ACE HERE")
            if (sum + 10 <= 21):
                sum = sum + 10
                print("ACE CHANGED")
            self.isACE = self.isACE - 1

        return (sum)
