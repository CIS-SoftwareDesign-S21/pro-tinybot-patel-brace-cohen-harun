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


# Bot Takes Token, ClientID, and Permissions from JSON File
bot_info_file = open("token.json")
bot_info = json.load(bot_info_file)

c4Games = dict()
tttGames = dict()
btsGames = dict()

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
    "BattleShip" : "battleship",
    "Connect 4" : "c4",
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
        gamesList += game + "\n"

    # Sends the List of Available Sounds to Play to the Discord Channel
    await ctx.send(gamesList)


# Says Hello to User, if Specified, who prompted the Command
@client.command()
async def hello(ctx, message=None):

    # Check if only Hello was Passed if so, Say Hello
    if not message:
        await ctx.send("Hello!")
        return

    # If Tinyboy was Greeted
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
    embedVar.title = ctx.author.mention

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
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")

            elif ctx.author.id == tttGames[ctx.author.id].opponent:
                if tttGames[ctx.author.id].userTurn == False:
                    await ctx.send(tttGames[ctx.author.id].makeMove(move))
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")

            if tttGames[ctx.author.id].checkWin == True or tttGames[ctx.author.id].checkTie == True:
                await ctx.send(embed=goodbyeMessage())
                userId: str = tttGames[ctx.author.id].user
                opId: str = tttGames[ctx.author.id].opponent
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
async def chess(ctx, message=None):

    # Instantiate the Game unless a Move is being Played
    if not message:
        global chessGame
        chessGame = MicrochessGame()
        path = chessGame.genBoardImage()
        await ctx.send(file=discord.File(path))
        await ctx.send('A chess game has started!\nWhite, it\'s your move.')
        await ctx.send('Enter * followed by a letter for your piece: P - Pawn, B- Bishop, K - Knight, R - Rook, S - King')
        await ctx.send('Piece ID should be followed by Column and Row ID')
        await ctx.send('For example, *KB3 is a good opening move.')

    # Make the Move Given
    move = ctx.message.content[7:]
    
    # For Testing Purposes
    print(move)

    updateMessage, playerMoved = chessGame.makeMove(move)
    if playerMoved:
        path = chessGame.genBoardImage()
        await ctx.send(file=discord.File(path))
    await ctx.send(updateMessage)

    return


# Command to Play the Battleship Game
@client.command()
async def bts(ctx, message=None):

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
        print(btsGames.get(ctx.author.id))
        if btsGames.get(ctx.author.id):
            await ctx.send(btsGames[ctx.author.id].makeMove(move))

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
        if c4Games.get(ctx.author.id):
            if ctx.author.id == c4Games[ctx.author.id].user:
                if c4Games[ctx.author.id].userTurn == True:
                    await ctx.send(c4Games[ctx.author.id].makeMove(move))
                else:
                    await ctx.send(f"{ctx.author.mention}, it's not your turn!")

            elif ctx.author.id == c4Games[ctx.author.id].opponent:
                if c4Games[ctx.author.id].userTurn == False:
                    await ctx.send(c4Games[ctx.author.id].makeMove(move))
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

# Error Handler if Invited User Doesn't exist for Tic-Tac-Toe ################################################################

# Command to Create User ID in Leaderboard
@client.command()
async def newUser(ctx):

    lb = leaderb()

    # Obtain the User's ID
    userID = ctx.author.id
    print(userID)

    # Send the User ID to Function
    lb.addNewUser(userID)

    # Open the JSON to be Loaded
#    with open("leaderboard2.json") as lb_file:
#        lb_data = json.load(lb_file)
#        print(lb_data)

#        temp = lb_data['users']

        # Create User to Append to JSON File
#        nUser = {"user_name": f"{userID}",
#                 "wins": "0",
#                 "losses": "0"
#                }

#        temp.append(nUser)

    # Append to JSON File
#    with open("leaderboard2.json", 'w') as file:
#        json.dump(temp, file, indent = 4)

    return

client.run(bot_info['token'])   
