from typing import Any
import discord
import os
from tic_tac_toe import TicTacToeGame
from battleShip import BattleShipGame
from coinflip import coinflip
from microchess import MicrochessGame
from blackJack import blackJack

user = ""
opponent = ""
userTurn = True
checkWin = False
gameEnd = False
checkTie = False
game: TicTacToeGame = TicTacToeGame(user, opponent, userTurn, checkWin, gameEnd, checkTie)
game2: BattleShipGame = BattleShipGame()
chessGame: MicrochessGame = None

client = discord.Client()

def getUserFromMention(opponent):
    if opponent.startswith('<@') and opponent.endswith('>'):
        opponent = opponent[2:-1]
        if opponent.startswith('!'):
            opponent = opponent[1:]
    return opponent

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Simple Bot commands
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith( 'i am' ):
        await message.channel.send( 'Hello, ' + message.content.split( ' ' )[2] )

    # Shutdown the bot
    elif message.content.startswith( '$bye' ):
        await message.channel.send('Bye!')
        await client.logout()
        await client.close()

    #Handles the start of a Tic-Tac-Toe game with invite function
    elif message.content.startswith('ttt <@'):
        opponent = message.content.replace('ttt ', '')
        opponent = getUserFromMention(opponent)
        userTurn = True
        checkWin = False
        gameEnd = False
        checkTie = False
        global game
        game = TicTacToeGame(int(message.author.id),
                             int(opponent), bool(userTurn), bool(checkWin), bool(gameEnd), bool(checkTie))
        game.clearBoard()
        await message.channel.send('Tic-Tac-Toe game started!\nEnter #\'Location\' to Move')
        await message.channel.send('Example: #A1')
        await message.channel.send(game.initBoard())
        await message.channel.send("<@!" + str(game.user) + ">, Make your move!")

    # Handels making moves in Tic-Tac-Toe game
    elif message.content.startswith('^'):
        if(not game.gameEnd):
            if message.author.id == game.user:
                if game.userTurn == True:
                    validMove = game.makeMove(message.content[1:])
                    if "Error" in validMove:
                        await message.channel.send(validMove)
                    else:
                        await message.channel.send(validMove)
                        game.userTurn = False
                        if game.checkWin == False and game.checkTie == False:
                            await message.channel.send("<@!" + str(game.opponent) + ">, Make your move!")
                        elif game.checkWin == True:
                            await message.channel.send("<@!" + str(game.user) + ">, Wins!")
                else:
                    await message.channel.send("<@!" + str(game.user) + "> it's not your turn!")
            elif message.author.id == game.opponent:
                if game.userTurn == False:
                    validMove = game.makeMove(message.content[1:])
                    if "Error" in validMove:
                        await message.channel.send(validMove)
                    else:
                        await message.channel.send(validMove)
                        game.userTurn = True
                        if game.checkWin == False and game.checkTie == False:
                            await message.channel.send("<@!" + str(game.user) + ">, Make your move!")
                        elif game.checkWin == True:
                            await message.channel.send("<@!" + str(game.opponent) + ">, Wins!")
                else:
                    await message.channel.send("<@!" + str(game.opponent) + "> it's not your turn!")
            else:
                await message.channel.send("Didn't recognize player!")
        # if someone won or it tied
        else:
            await message.channel.send("Start a Tic-Tac-Toe game to make a move!")

    # Handles Coin flip game
    elif message.content.startswith( '$coin' ):
        embed = discord.Embed()
        result = coinflip()
        # embed.title = result
        if(result == "HEADS"):
            embed.set_image(
                url="https://media1.tenor.com/images/20f12dfa0e544b7c1045c903c572f9ec/tenor.gif?itemid=20771728")
        else:
            embed.set_image(
                url="https://media1.tenor.com/images/51e09c7f9e8051ab944f0aaeed426e80/tenor.gif?itemid=20771732")
        await message.channel.send(embed = embed)
    elif message.content.startswith( '$how are you' ):
        await message.channel.send('I am good! Thank you for asking')
    elif message.content.startswith('chess'):
        global chessGame
        chessGame = MicrochessGame()
        path = chessGame.genBoardImage()
        await message.channel.send(file=discord.File(path))
        await message.channel.send('A chess game has started!\nWhite, it\'s your move.')
        await message.channel.send('Enter * followed by a letter for your piece: P - Pawn, B- Bishop, K - Knight, R - Rook, S - King')
        await message.channel.send('Piece ID should be followed by Column and Row ID')
        await message.channel.send('For example, *KB3 is a good opening move.')
    elif message.content.startswith('*'):
        updateMessage, playerMoved = chessGame.makeMove(message.content[1:])
        if playerMoved:
            path = chessGame.genBoardImage()
            await message.channel.send(file=discord.File(path))
        await message.channel.send(updateMessage)

    elif message.content.startswith('battleship'):
        global game2  
        game2 = BattleShipGame()
        await message.channel.send('BattleShip game started!')

    elif message.content.startswith('#'):
        await message.channel.send(game2.makeMove(message.content[1:]))
    #BlackJack
    elif message.content.startswith('&blackjack'):
        global blackjackGame
        blackjackGame = blackJack()
        blackjackGame.start()
        await message.channel.send("Welcome to Black Jack")
        await message.channel.send(blackjackGame.checkBoard())
        await message.channel.send("Enter &H to Hit or &S to Stand")
        # blackjackGame.checkBoard()
        # await message.channel.send("BlackJack Start")
        # embed = discord.Embed()
        # embed.title = "Black Jack Game"
        # embed.add_field(name="Dealer", value=blackjackGame.dealer)
        # embed.add_field(name="Player", value=blackjackGame.player)
        # embed.description = "Enter &H to Hit or &S to Stand"
        # await message.channel.send(embed= embed)

    elif message.content.startswith('&'):
        if(message.content[1:] == 'H'):
            blackjackGame.choice(message.content[1:])
            await message.channel.send(blackjackGame.checkBoard())
            if(blackjackGame.done == 1):
                await message.channel.send(blackjackGame.result())
            await message.channel.send("Enter &H to Hit or &S to Stand")
        elif( message.content[1:] == 'S'):
            blackjackGame.choice(message.content[1:])
            blackjackGame.dealerTurn()
            await message.channel.send(blackjackGame.checkBoard())
            await message.channel.send(blackjackGame.result())
        else:
            await message.channel.send("Wrong Input")



client.run('ODIzOTIyODMwOTI4Mzc5OTI0.YFn37g.qBiNOnlxbAgc7n4jfu9GQi2dkQk')
