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
from leaderboard_impl import leaderb
from blackJack import blackJack

# Bot Takes Token, ClientID, and Permissions from JSON File
bot_info_file = open("token.json")
bot_info = json.load(bot_info_file)

chessGames = dict()
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
    "Chess" : "ch",
    "BlackJack" : "blackjack"
  
}

# Function to Display a Goodbye Message for when a Game Ends
def goodbyeMessage():

    # Embed an Image
    goodbye = discord.Embed()

    # Define the Variables
    goodbye.title = "Thank you for playing!"

    return goodbye

# 

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
    embedVar.title = result

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
#async def ttt(ctx, *, user: discord.User):
async def ttt(ctx, user: typing.Union[discord.User, str]):

    # Instantiate the Game unless a Move is being Played
    if not isinstance(user, str):
        global game
        opponent = user.id

        # For Testing Purposes
        print(opponent) 

        userTurn = True
        checkWin = False
        gameEnd = False
        checkTie = False
        game = TicTacToeGame(int(ctx.author.id), int(opponent), bool(userTurn), bool(checkWin), bool(gameEnd), bool(checkTie))
        game.clearBoard()
        await ctx.send('Tic-Tac-Toe game started!\nEnter #\'Location\' to Move')
        await ctx.send('Example: #A1')
        await ctx.send(game.initBoard())
        await ctx.send(f"{ctx.author.mention}, Make your move!")
    # Make the Move Given
    else:
        move = user
        print(move)
        if not game.gameEnd:
            if ctx.author.id == game.user:
                if game.userTurn == True:
                    await ctx.send(game.makeMove(move))
                    if game.checkWin == True:
                        await ctx.send(embed = goodbyeMessage())
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")
            elif ctx.author.id == game.opponent:
                if game.userTurn == False:
                    await ctx.send(game.makeMove(move))
                    if game.checkWin == True:
                        await ctx.send(embed = goodbyeMessage())
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")
            else:
                await ctx.send("Didn't recognize player!")
        else:
            await ctx.send("Start a Tic-Tac-Toe game to make a move!")

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
async def battleship(ctx, message=None):

    # Instantiate the Game unless a Game is already being Played
    if not message:
        global battleshipGame
        battleshipGame = BattleShipGame()
        await ctx.send("Battleship game started!")

    # Make the Move Given
    move = ctx.message.content[12:]

    # For Testing Purposes
    print(move)

    await ctx.send(battleshipGame.makeMove(move))

    return

# Command to Play the BlackJack Game
@client.command()
async def blackjack(ctx, message=None):

    # Instantiate the Game unless a Game is already being Played
    if not message:
        global blackjackGame
        blackjackGame = blackJack()
        await ctx.send("BlackJack game started!")
        blackjackGame.start()
        embed = discord.Embed(title="BlackJack", color=0xe60a0a)
        embed.set_thumbnail(
            url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
        embed.add_field(name="Dealer", value=blackjackGame.dealer, inline=False)
        embed.add_field(name="Player", value=blackjackGame.player, inline=False)
        embed.set_footer(text="Enter $blackjack H to Hit or $blackjack S to Stand")
        await ctx.send(embed=embed)

    # Make the Move Given
    if (ctx.message.content[11] == 'H' and blackjackGame.player != []):
        embed = discord.Embed(title="BlackJack", color=0xe60a0a)
        blackjackGame.choice(ctx.message.content[11])
        if (blackjackGame.done == 1):
            result = blackjackGame.result()
            embed.set_thumbnail(
                url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
            embed.add_field(name="Dealer", value=blackjackGame.dealer, inline=False)
            embed.add_field(name="Player", value=blackjackGame.player, inline=False)
            if (result == 1):
                embed.set_footer(text="PLAYER WIN")
            elif (result == 2):
                embed.set_footer(text="DRAW")
            else:
                embed.set_footer(text="PLAYER LOSE")
            await ctx.send(embed=embed)
            blackjackGame.clean()
        else:
            embed.set_footer(text="Enter $blackjack H to Hit or $blackjack S to Stand")
            embed.set_thumbnail(url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
            embed.add_field(name="Dealer", value=blackjackGame.dealer, inline=False)
            embed.add_field(name="Player", value=blackjackGame.player, inline=False)
            await ctx.send(embed=embed)
    elif (ctx.message.content[11] == 'S' and blackjackGame.player != []):
        blackjackGame.choice(ctx.message.content[11])
        blackjackGame.dealerTurn()
        embed = discord.Embed(title="BlackJack", color=0xe60a0a)
        embed.set_thumbnail(
            url="https://previews.123rf.com/images/irrrina/irrrina1611/irrrina161100011/66665304-playing-cards-icon-outline-illustration-of-playing-cards-vector-icon-for-web.jpg")
        embed.add_field(name="Dealer", value=blackjackGame.dealer, inline=False)
        embed.add_field(name="Player", value=blackjackGame.player, inline=False)
        result = blackjackGame.result()

        if (result == 1):
            embed.set_footer(text="PLAYER WIN")
        elif (result == 2):
            embed.set_footer(text="DRAW")
        else:
            embed.set_footer(text="PLAYER LOSE")
        await ctx.send(embed=embed)
        blackjackGame.clean()
    else:
        await ctx.send("Wrong Input")

    return

# Error Handlers Here ######################################################


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


# Test Command to Update the Leaderboard
@client.command()
async def updateLB(ctx):

    # Instantiate the Leaderboard Class
    lb = leaderb()

#    lb.addNewUser(144, "Test1")
#    lb.addNewUser(164, "Test2")
    lb.updateLeaderboard(144, 164, "Test1", "Test2")

    return


client.run(bot_info['token'])   