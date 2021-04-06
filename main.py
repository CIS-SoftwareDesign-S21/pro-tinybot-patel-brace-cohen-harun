from typing import Any

import discord
import os
from random import randint
from tic_tac_toe import TicTacToeGame

user = ""
opponent = ""
game: TicTacToeGame = TicTacToeGame(user, opponent)
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
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith( 'i am' ):
        await message.channel.send( 'Hello, ' + message.content.split( ' ' )[2] )
    elif message.content.startswith( '$bye' ):
        await message.channel.send('Bye!')
        await client.logout()
        await client.close()
    # elif message.content.startswith( 'ttt' ):
    #     global game #holy fuck python just be normal
    #     game = TicTacToeGame()
    #     await message.channel.send( 'Tic-Tac-Toe game started!' )

    elif message.content.startswith('ttt <@'):
        opponent = message.content.replace('ttt ', '')
        opponent = getUserFromMention(opponent)
        global game
        game = TicTacToeGame(message.author.id, opponent)
        await message.channel.send('Tic-Tac-Toe game started')

    elif message.content.startswith('^'):
        if message.author.id == game.user or message.author.id == game.opponent:
            await message.channel.send(game.makeMove( message.content[1:]) )
        else:
            await message.channel.send("Didn't recognize player!")



client.run('ODIzOTIyODMwOTI4Mzc5OTI0.YFn37g.qBiNOnlxbAgc7n4jfu9GQi2dkQk')
