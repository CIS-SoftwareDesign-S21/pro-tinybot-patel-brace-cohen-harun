import discord
from discord.ext import commands
import json
import asyncio
import os

# Bot Takes Token, ClientID, and Permissions from JSON File
bot_info_file = open("token.json")
bot_info = json.load(bot_info_file)

# Prints out the Invite Link for the Bot
print("Bot invite link:")
print(f"https://discordapp.com/oauth2/authorize?client_id={bot_info['clientid']}&scope=bot&permissions={bot_info['permissions']}")
print()

# Set Client and Bot Command Prefix
client = discord.Client()
bot = commands.Bot(command_prefix="!", description="Plays sound bites")

# Store the Name of the Sound Files Directory
soundFileLoc = "SoundFiles"

# Directory to Map Nicknames to Specified Sound File
nicknameDictionary = {

    "bell" : "service-bell_daniel_simion.mp3",
    "ronnie" : "Ronnie.mp3",
    "john cena" : "JohnCena.mp3",
    "ronnie come" : "RonnieCome.mp3"

}

# Once Bot is Logged In and Ready on Discord Server
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(f"Bot id: {bot.user.id}")
    print()

# Plays (Shouts) the Specified Sound using the given Nickname
@bot.command()
async def shout(ctx):
    
    # Ensures something was passed besides "!shout "
    if len(ctx.message.content) < 8:
        await ctx.send("Type: '!shout <Sound Name>' to Play the Sound.")
        return

    # Takes the Rest of the Input and makes it a String (Represents the Nickname Passed) 
    # Then makes sure the Nickname Passed Exists in the Dictionary 
    nickname = ctx.message.content[7:]
    if nickname not in nicknameDictionary:
        await ctx.send("No Sound Found.")
        return

    # Get the Audio File Name attached to Specified Nickname
    file_name = nicknameDictionary[nickname]

    # Connects Bot to the Voice Channel the Author (Sender) is in
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    # Attempts to Play the Specified Sound File
    try:
        voice_client.play(discord.FFmpegPCMAudio(source=f"{soundFileLoc}/{file_name}"))
        while voice_client.is_playing():
            await asyncio.sleep(2)
    except Exception as e:
        print(e)

    # Disconnects Bot from the Voice Channel
    await voice_client.disconnect()


# Displays the Current List of Available Sounds to Play
@bot.command()
async def sounds(ctx):
    soundsList = ""

    # Appends all Available Sounds to Play to a String (Acting as List to Display)
    for nickname in nicknameDictionary:
        soundsList += nickname + "\n"

    # Sends the List of Available Sounds to Play to the Discord Channel
    await ctx.send(soundsList) 

# Sets up the Link between Nickname and Stored Sound File
@bot.command()
async def set(ctx, nickname, file_name):
    
    # Get Number of Characters in File Name and Modify to Ensure File is a .mp3
    file_name_len = len(file_name)
    ending_len = file_name_len - 4  # Subtract 4 for the Number of Characters in .mp3

    # Get the Ending of the File Name
    file_ending = file_name[ending_len:]

    # Ensure the File is a .mp3
    if file_ending != ".mp3":
        await ctx.send("Type: '!set <Nickname> <FileName.mp3>' to setup and save nickname ensure a .mp3 Sound File is used.")
        print(file_ending)
        return 

    # Ensure the Sound File Exists in Directory
    if os.path.exists(f"{soundFileLoc}/{file_name}"):
        # Set the Nickname as the Key and File Name as the Value in the Dictionary
        nicknameDictionary[nickname] = file_name
        await ctx.send(nickname + " Saved")
    else:
        ctx.send("No Sound File Named: " + file_name + " Was Found in the Directory.")
        return


bot.run(bot_info['token'])