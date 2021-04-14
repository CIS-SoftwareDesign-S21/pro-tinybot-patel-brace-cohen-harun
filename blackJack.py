import random

class blackJack:
    symbol = ['♠', '♣', '♥', '♦']

    def __init__(self):
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        # self.symbol = ['♠', '♣', '♥', '♦']
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


    def choice(self):
        self.total = self.sum(self.player)
        while(self.done == 0):
            playerChoice = input("Enter H to Hit or S to Stand :")
            if(playerChoice == "H"):
                self.player.append(self.cards.pop() + random.choice(self.symbol))
                self.total = self.sum(self.player)
                if(self.total > 21):
                    self.done = 1
                    self.bust = 1
                self.checkBoard()
            elif(playerChoice == "S"):
                self.total = self.sum(self.player)
                self.done = 1
            else:
                print("WRONG INPUT")

    def result(self):
        if (self.bust == 1):
            print("BUST!")
            print("PLAYER LOSE")
            return 0
        self.totalDealer = self.sum(self.dealer)
        while(self.totalDealer < 21 and self.totalDealer <= self.total and self.bust == 0):
            self.dealer.append(self.cards.pop() + random.choice(self.symbol))
            self.totalDealer = self.sum(self.dealer)
            self.checkBoard()
        if(len(self.player) > 4 and self.total<=21):
            print("5 CARDS")
            print("PLAYER WIN")
        if(self.totalDealer > 21):
            print("DEALER BUST!")
            print("PLAYER WIN")
            return 1
        if(self.total < self.totalDealer):
            self.totalDealer = self.sum(self.dealer)
            self.total = self.sum(self.player)
            print("DEALER HAVE: ", self.totalDealer)
            print("PLAYER HAVE: ", self.total)
            print("PLAYER LOSE")
            return 0
        elif(self.total == self.totalDealer):
            print("DRAW")
            return 2
        else:
            if(self.total == 21):
                print("BLACKJACK")
            print("PLAYER WIN")
            return 1

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
        print("DEALER: ")
        for i in self.dealer:
            print(i,end=" ")
        print("")
        print("PLAYER: ")
        for i in self.player:
            print(i,end=" ")
        print("")
        print("")

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

print("WELCOME TO BLACKJACK")
game = blackJack()
game.start()
game.checkBoard()
game.choice()
game.result()