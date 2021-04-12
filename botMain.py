import discord
from discord.ext import commands
import json
import asyncio
import os

# Bot Takes Token, ClientID, and Permissions from JSON File
bot_info_file = open("token.json")
bot_info = json.load(bot_info_file)

# Prints out the Invite Link for the Bot
print("Bot Invite Link: ")
print(f"https://discordapp.com/oauth2/authorize?client_id={bot_info['clientid']}&scope=bot&permissions={bot_info['permissions']}")
print()

# Set Client and Bot Command Prefix
client = discord.Client()
bot = commands.Bot(command_prefix={bot_info['prefix']}, description="Bot to play Minigames.")

# Once Bot is Logged In and Ready on Discord Server Notification
@bot.event
async def on_ready():
    print(f"We have Logged In as {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print()

