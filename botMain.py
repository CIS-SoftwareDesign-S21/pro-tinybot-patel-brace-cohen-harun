import discord
from discord.ext import commands
import json
import asyncio
import typing
import os

from coinflip import coinflip
from tic_tac_toe import TicTacToeGame
from microchess import MicrochessGame
from battleShip import BattleShipGame
from connect4 import Connect4Game
from leaderboard_impl import leaderb
from blackJack import blackJack


# Bot Takes Token, ClientID, and Permissions from JSON File
bot_info_file = open("token.json")
bot_info = json.load(bot_info_file)

c4Games = dict()
tttGames = dict()
btsGames = dict()
chessGames = dict()
bjGames = dict()
cLock = asyncio.Lock()

# Prints out the Invite Link for the Bot
print("Bot Invite Link: ")
# print(f"https://discordapp.com/oauth2/authorize?client_id={bot_info['clientid']}&scope=bot&permissions={bot_info['permissions']}")
print("https://discord.com/api/oauth2/authorize?client_id=823922830928379924&permissions=2151152704&scope=bot")
print()

# Set Client and Bot Command Prefix
# client = discord.Client()
client = commands.Bot(command_prefix={bot_info['prefix']}, description="Bot to play Minigames.")

# Game Dictionary
gameDictionary = {

    "Hello" : "hello",
    "Mood" : "mood",
    "Coinflip" : "coinf",
    "Tic-Tac-Toe" : "ttt",
    "BattleShip" : "bts",
    "Connect 4" : "c4",
    "Chess" : "ch",
    "BlackJack" : "bj"
}

# Function to Display a Goodbye Message for when a Game Ends
def goodbyeMessage():

    # Embed an Image
    goodbye = discord.Embed()

    # Define the Variables
    goodbye.title = "Thank you for playing!"

    return goodbye


# Once Bot is Logged In and Ready on Discord Server Notification
@client.event
async def on_ready():
    print(f"We have Logged In as {client.user}")
    print(f"Bot ID: {client.user.id}")
    print()


# Display a List of Commands to Use
@client.command()
async def games(ctx):

    # Variable to Hold the List
    gamesList = ""

    # Appends all Available Commands/Games to Play to a String (Acting as a List to Display)
    for game in gameDictionary:
        gamesList += game + ':\t$' + gameDictionary[game] + "\n"

    # Sends the List of Available Sounds to Play to the Discord Channel
    await ctx.send(gamesList)


# Says Hello to User, if Specified, who prompted the Command
@client.command()
async def hello(ctx, message=None):

    # Check if only Hello was Passed if so, Say Hello
    if not message:
        await ctx.send("Hello!")
        return

    # If Tinybot was Greeted
    if (message.lower() == "tinybot"):
        await ctx.send(f'Hello, {ctx.author.mention}!')
        return


# Says Goodbye and Shuts Down the Bot
@client.command()
async def bye(ctx, message=None):

    # Check if only Bye was Passed if so, Say Goodbye
    if not message:
        await ctx.send("Goodbye!")
        await client.logout()
        await client.close()

# Bot tells you its Mood
@client.command()
async def mood(ctx):
    await ctx.send('I am good! Thank you for asking!')
    return

# Command to Make a Coin Flip
@client.command()
async def coinf(ctx):

    # Embed an Image
    embedVar = discord.Embed()

    # Generate Result and Embed Title
    result = coinflip()
    embedVar.title = "@"+str(ctx.author)


    # Display Appropriate Image
    if result == "HEADS":
        embedVar.set_image(url="https://media1.tenor.com/images/20f12dfa0e544b7c1045c903c572f9ec/tenor.gif?itemid=20771728")
    else:
        embedVar.set_image(url="https://media1.tenor.com/images/51e09c7f9e8051ab944f0aaeed426e80/tenor.gif?itemid=20771732")

    # Send the Image
    await ctx.send(embed = embedVar)

    return


# Command to Play the Tic-Tac-Toe Minigame
@client.command()
async def ttt(ctx, user: typing.Union[discord.User, str]):

    lb = leaderb()

    # Instantiate the Game unless a Move is being Played
    if not isinstance(user, str):

        if not tttGames.get(ctx.author.id) and not tttGames.get(user.id):
            tttGames[ctx.author.id] = TicTacToeGame(ctx.author.id, user.id)
            tttGames[user.id] = tttGames[ctx.author.id]
            print(tttGames)
        else:
            error1 = discord.Embed(
                title="You or the player you invited are already in a game!")
            await ctx.channel.send(embed=error1)
            return

        start = discord.Embed(title="Tic-Tac-Toe Game Started!",
                              description="Enter $ttt \'Location\' To Make A Move\nExample: $ttt a1", color=15158332)
        await ctx.send(embed=start)
        await ctx.channel.send(tttGames[ctx.author.id].initBoard())
        await ctx.send(f"{ctx.author.mention}, Make your move!")

    else:
        move = user
        if(move == 'help'):
            help = discord.Embed(
                title="Tic-Tac-Toe Commands!",
                description="Use command '$ttt @user' to start the game\nThe game is played on a 3x3 board, use A-C and 1-3 to select a column and row\nUse command '$ttt [col][row]' to make a move, for example '$ttt a1'")
            await ctx.send(embed=help)
            return

        if tttGames.get(ctx.author.id):
            if ctx.author.id == tttGames[ctx.author.id].user:
                if tttGames[ctx.author.id].userTurn == True:
                    await ctx.send(tttGames[ctx.author.id].makeMove(move))
                    if tttGames[ctx.author.id].checkWin == True:
                        winner = tttGames[ctx.author.id].user
                        loser = tttGames[ctx.author.id].opponent
                        winnerName = await client.fetch_user(int(winner))
                        loserName = await client.fetch_user(int(loser))
                        print(winnerName)
                        print(loserName)
                        lb.updateLeaderboard(winner, loser, str(winnerName), str(loserName))
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")

            elif ctx.author.id == tttGames[ctx.author.id].opponent:
                if tttGames[ctx.author.id].userTurn == False:
                    await ctx.send(tttGames[ctx.author.id].makeMove(move))
                    if tttGames[ctx.author.id].checkWin == True:
                        winner = tttGames[ctx.author.id].opponent
                        loser = tttGames[ctx.author.id].user
                        winnerName = await client.fetch_user(int(winner))
                        loserName = await client.fetch_user(int(loser))
                        print(winnerName)
                        print(loserName)
                        lb.updateLeaderboard(winner, loser, str(winnerName), str(loserName))
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")

            if tttGames[ctx.author.id].checkWin == True or tttGames[ctx.author.id].checkTie == True:
                await ctx.send(embed=goodbyeMessage())
                userId = tttGames[ctx.author.id].user
                opId = tttGames[ctx.author.id].opponent
                del tttGames[userId]
                del tttGames[opId]
                print(tttGames)
        else:
            error2 = discord.Embed(
                title="Start a Tic Tac Toe game ($ttt @user) to make a move!")
            await ctx.send(embed=error2)
    return


# Command to Play the MicroChess Minigame
@client.command()
async def ch(ctx, user: typing.Union[discord.User, str]):
    if not isinstance(user, str):
        # Check if the user or opponent is already in a game, and create new one if not
        if not chessGames.get(str(ctx.author.id)) and not chessGames.get(str(user.id)):
            chessGames[str(ctx.author.id)] = MicrochessGame(ctx.author, user)
            chessGames[str(user.id)] = chessGames[f'{ctx.author.id}']
            path = chessGames[str(ctx.author.id)].genBoardImage()
            await ctx.send(file=discord.File(path))
            await ctx.send(f'A chess game has started!\n{ctx.author.mention}, it\'s your move.\n' +
                           'Enter a letter for your piece: P - Pawn, B- Bishop, K - Knight, R - Rook, S - King, Q - Queen\n' +
                           'Piece ID should be followed by Column and Row ID\n' +
                           'For example, \'$ch KB3\' is a good opening move.')
        else:
            await ctx.send(f'{ctx.author.mention}, you or the player you invited are already in a game!')


    else: #if the message is a move, not a username:
        move = user
        if move.startswith('help'):
            await ctx.send('To start a chess game, use command \'$ch @opponent\'\n' +
                           'To make a move, enter a letter for your piece: P - Pawn, B- Bishop, K - Knight, R - Rook, S - King, Q - Queen\n' +
                           'Piece ID should be followed by Column and Row ID\nFor example, \'$ch BD3\' moves the Bishop to D3, if possible.')
            return

        try:
            game = chessGames[f'{ctx.author.id}']
        except:
            await ctx.send(f'{ctx.author.mention}, you are not currently in a chess game.\nUse command \'$ch @opponent\' to start game.')
            return

        if not game.isTurnOf(ctx.author.id):
            await ctx.send(f'{ctx.author.mention}, it\'s not your turn!')
            return

        #attempt to make move and send result to channel
        updateMessage, playerMoved = game.makeMove(move)
        if playerMoved:
            async with cLock:
                path = game.genBoardImage()
                await ctx.send(file=discord.File(path))
        await ctx.send(updateMessage)

        if game.gameCompleted:
            whitePlayer = game.userAccounts[0]
            blackPlayer = game.userAccounts[1]
            del chessGames[str(whitePlayer.id)]
            del chessGames[str(blackPlayer.id)]

    return


# Command to Play the Battleship Game
@client.command()
async def bts(ctx, message=None):

    lb = leaderb()

    # Instantiate the Game unless a Game is already being Played
    if not message:
        if not btsGames.get(ctx.author.id):
            btsGames[ctx.author.id] = BattleShipGame(ctx.author.id)
            print(btsGames)
        else:
            error1 = discord.Embed(
                title="You are already in a game!")
            await ctx.channel.send(embed=error1)
            return

        start = discord.Embed(title="Battleship Game Started!",
                              description="Enter $bts \'Location\' To Make A Move\nExample: $bts a1", color=15158332)
        await ctx.send(embed=start)

    # Make the Move Given
    else:
        move = message
        # For Testing Purposes
        print(move)

        if(move == 'help'):
            help = discord.Embed(
                title="Battleship Commands!",
                description="Use command '$bts' to start the game\nThe game is played on a 5x5 board, use A-E and 1-5 to select a row and column\nUse command '$bts [row][col]' to make a move, for example '$bts a1'\nUse command '$bts end' to end the game")
            await ctx.send(embed=help)
            return

        if btsGames.get(ctx.author.id):

            if(move == 'end'):
                btsGames[ctx.author.id].endGame = True
            else:
                await ctx.send(btsGames[ctx.author.id].makeMove(move))
#                if btsGames[ctx.author.id].checkWin == True:

            if btsGames[ctx.author.id].checkWin == True or btsGames[ctx.author.id].endGame == True:
                await ctx.send(embed=goodbyeMessage())
                userId = btsGames[ctx.author.id].user
                del btsGames[userId]
                print(btsGames)
        else:
            error2 = discord.Embed(
                title="Start a Battleship game ($bts) to make a move!")
            await ctx.send(embed=error2)
    return

@client.command()
async def c4(ctx, user: typing.Union[discord.User, str]):
    
    lb = leaderb()
    
    if not isinstance(user, str):
        # Check if the user or opponent is already in a game
        if not c4Games.get(ctx.author.id) and not c4Games.get(user.id):
            c4Games[ctx.author.id] = Connect4Game(ctx.author.id, user.id)
            c4Games[user.id] = c4Games[ctx.author.id]
            print(c4Games)
        else:
            error1 = discord.Embed(title="You or the player you invited are already in a game!")
            await ctx.channel.send(embed = error1)
            return

        start = discord.Embed(title="Connect 4 Game Started!",
                              description="Enter $c4 \'Location\' To Make A Move\nExample: $c4 a", color=15158332)
        await ctx.send(embed=start)
        await ctx.channel.send(c4Games[ctx.author.id].initBoard())
        await ctx.send(f"{ctx.author.mention}, Make your move!")
    else:
        move = user
        if(move == 'help'):
            help = discord.Embed(
                title="Connect 4 Commands!",
                description="Use command '$c4 @user' to start the game\nThe game is played on a 6X7 board, use A-G to select a column\nUse command '$c4 [col]' to make a move, for example '$c4 a'")
            await ctx.send(embed=help)
            return
        if c4Games.get(ctx.author.id):
            if ctx.author.id == c4Games[ctx.author.id].user:
                if c4Games[ctx.author.id].userTurn == True:
                    await ctx.send(c4Games[ctx.author.id].makeMove(move))
                    if c4Games[ctx.author.id].checkWin == True:
                        winner = c4Games[ctx.author.id].user
                        loser = c4Games[ctx.author.id].opponent
                        winnerName = await client.fetch_user(int(winner))
                        loserName = await client.fetch_user(int(loser))
                        lb.updateLeaderboard(winner, loser, str(winnerName), str(loserName))
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")

            elif ctx.author.id == c4Games[ctx.author.id].opponent:
                if c4Games[ctx.author.id].userTurn == False:
                    await ctx.send(c4Games[ctx.author.id].makeMove(move))
                    if c4Games[ctx.author.id].checkWin == True:
                        winner = c4Games[ctx.author.id].opponent
                        loser = c4Games[ctx.author.id].user
                        winnerName = await client.fetch_user(int(winner))
                        loserName = await client.fetch_user(int(loser))
                        lb.updateLeaderboard(winner, loser, str(winnerName), str(loserName))
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")

            if c4Games[ctx.author.id].checkWin == True or c4Games[ctx.author.id].checkTie == True:
                await ctx.send(embed=goodbyeMessage())
                userId = c4Games[ctx.author.id].user
                opId = c4Games[ctx.author.id].opponent
                del c4Games[userId]
                del c4Games[opId]
                print(c4Games)
        else:
            error2 = discord.Embed(title = "Start a Connect 4 game to make a move!")
            await ctx.send(embed = error2)
    return

# Command to Play the BlackJack Game
@client.command()
async def bj(ctx, message=None):

    lb = leaderb()

    # Instantiate the Game unless a Game is already being Played
    if not message:
        if not bjGames.get(ctx.author.id):
            bjGames[ctx.author.id] = blackJack()
            print(bjGames)
        else:
            error1 = discord.Embed(
                title="You are already in a game!")
            await ctx.channel.send(embed=error1)
            return

        # global blackjackGame
        # blackjackGame = blackJack()
        await ctx.send("BlackJack game started!")
        bjGames[ctx.author.id].start()
        embed = discord.Embed(title="BlackJack", color=0xe60a0a)
        embed.set_thumbnail(
            url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
        embed.add_field(
            name="Dealer", value=bjGames[ctx.author.id].dealer, inline=False)
        embed.add_field(
            name="Player", value=bjGames[ctx.author.id].player, inline=False)
        embed.set_footer(text="Enter $bj H to Hit or $bj S to Stand")
        await ctx.send(embed=embed)
        return

    # Make the Move Given
    move = message.upper()
    if move == 'HELP':
            help = discord.Embed(
                title="Black Jack Commands!",
                description="Use command '$bj' to start the game\nUse command '$bj h' to get another card or '$bj s' to keep your cards'")
            await ctx.send(embed=help)
            return

    if (move == 'H' and bjGames[ctx.author.id].player != []):
        embed = discord.Embed(title="BlackJack", color=0xe60a0a)
        bjGames[ctx.author.id].choice(move)
        if (bjGames[ctx.author.id].done == 1):
            result = bjGames[ctx.author.id].result()
            embed.set_thumbnail(
                url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
            embed.add_field(
                name="Dealer", value=bjGames[ctx.author.id].dealer, inline=False)
            embed.add_field(
                name="Player", value=bjGames[ctx.author.id].player, inline=False)
            if (result == 1):
                embed.set_footer(text="PLAYER WIN")
                winner = ctx.author.id
                winnerName = ctx.author
                loser = 0
                loserName = "Computer"
            elif (result == 2):
                embed.set_footer(text="DRAW")
            else:
                embed.set_footer(text="PLAYER LOSE")
                winner = 0
                winnerName = "Computer"
                loser = ctx.author.id
                loserName = ctx.author
            await ctx.send(embed=embed)
            if result != 2:
                lb.updateLeaderboard(winner, loser, str(winnerName), str(loserName))
            bjGames[ctx.author.id].clean()
            await ctx.send(embed = goodbyeMessage())
            del bjGames[ctx.author.id]
            print(bjGames)

        else:
            embed.set_footer(text="Enter $bj H to Hit or $bj S to Stand")
            embed.set_thumbnail(url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
            embed.add_field(
                name="Dealer", value=bjGames[ctx.author.id].dealer, inline=False)
            embed.add_field(
                name="Player", value=bjGames[ctx.author.id].player, inline=False)
            await ctx.send(embed=embed)

    elif (move == 'S' and bjGames[ctx.author.id].player != []):
        bjGames[ctx.author.id].choice(move)
        bjGames[ctx.author.id].dealerTurn()
        embed = discord.Embed(title="BlackJack", color=0xe60a0a)
        embed.set_thumbnail(
            url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
        embed.add_field(name="Dealer", value=bjGames[ctx.author.id].dealer, inline=False)
        embed.add_field(
            name="Player", value=bjGames[ctx.author.id].player, inline=False)
        result = bjGames[ctx.author.id].result()

        if (result == 1):
            embed.set_footer(text="PLAYER WIN")
            winner = ctx.author.id
            winnerName = ctx.author
            loser = 0
            loserName = "Computer"
        elif (result == 2):
            embed.set_footer(text="DRAW")
        else:
            embed.set_footer(text="PLAYER LOSE")
            winner = 0
            winnerName = "Computer"
            loser = ctx.author.id
            loserName = ctx.author
        await ctx.send(embed=embed)
        if result != 2:
            lb.updateLeaderboard(winner, loser, str(winnerName), str(loserName))
        bjGames[ctx.author.id].clean()
        await ctx.send(embed=goodbyeMessage())
        del bjGames[ctx.author.id]
        print(bjGames)

    else:
        await ctx.send("Wrong Input")

    return

# Error Handlers Here ######################################################

# Old Command to Create a New User in Leaderboard; now is Automated
'''
# Command to Create User ID in Leaderboard
@client.command()
async def newUser(ctx):

    lb = leaderb()

    # Obtain the User's ID
    userID = ctx.author.id
    userName = ctx.author
    print(userID)
    print(userName)

    # Send the User ID to Function
    lb.addNewUser(userID, userName)

    return
'''

# Command to Display the Leaderboard
@client.command()
async def leaderboard(ctx):

    # Instantiate the Leaderboard Class
    lb = leaderb()

    # Create an Embedded Variable for Formatting
    embedVar = discord.Embed(title = "__**Leaderboard**__", timestamp = ctx.message.created_at)

    # Take the Leaderboard Data in as a Variable
    data = lb.displayLeaderboard()

    # Add the Leaderboard Data as a Field in the Embed
    embedVar.add_field(name = "Most Wins", value = f'```{data}```', inline = False)

    await ctx.send(embed = embedVar)

    return

# Old Test Command to Update the Leaderboard with wins and losses; now handled Automatically once game is finished
'''
# Test Command to Update the Leaderboard
@client.command()
async def updateLB(ctx):

    # Instantiate the Leaderboard Class
    lb = leaderb()

#    lb.addNewUser(144, "Test1")
#    lb.addNewUser(164, "Test2")
    lb.updateLeaderboard(144, 164, "Test1", "Test2")

    return
'''

client.run(bot_info['token'])
