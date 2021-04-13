import discord
from discord.ext import commands
import json
import asyncio
import os

from coinflip import coinflip
from tic_tac_toe import TicTacToeGame
from leaderboard_impl import leaderb

# Bot Takes Token, ClientID, and Permissions from JSON File
bot_info_file = open("token.json")
bot_info = json.load(bot_info_file)

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
    "Tic-Tac-Toe" : "ttt"

}

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
async def ttt(ctx, user: discord.User):

    # Instantiate the Game unless a Move is being Played
    global game
    opponent = user.id

    # For Testing Purposes
    #print(opponent) 

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
    move = ctx.message.content[5:]
    await ctx.send(game.makeMove(move))

    return


# Command to Play the MicroChess Minigame
#@client.command()
#async def chess(ctx, message=None):

    # Instantiate the Game unless a Move is being Played
#    if not message:
#        global chessGame
#        chessGame = MicrochessGame()
#        path = chessGame.genBoardImage()


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