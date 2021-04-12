from typing import Any
import discord
import os
from tic_tac_toe import TicTacToeGame
from battleShip import BattleShipGame
from coinflip import coinflip

game: TicTacToeGame = TicTacToeGame()
game2: BattleShipGame = BattleShipGame()
client = discord.Client()


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
    elif message.content.startswith( 'ttt' ):
        global game #holy fuck python just be normal
        game = TicTacToeGame()
        await message.channel.send( 'Tic-Tac-Toe game started!' )
    elif message.content.startswith('^'):
        await message.channel.send( game.makeMove( message.content[1:] ) )
    elif message.content.startswith( '$coin' ):
        embed = discord.Embed()
        result = coinflip()
        embed.title = result
        if(result == "HEADS"):
            embed.set_image(url="https://bjc.edc.org/June2017/bjc-r/img/5-algorithms/img_flipping-a-coin/Heads.png")
        else:
            embed.set_image(url="https://bjc.edc.org/June2017/bjc-r/img/5-algorithms/img_flipping-a-coin/Tails.png")
        await message.channel.send(embed = embed)
    elif message.content.startswith( '$how are you' ):
        await message.channel.send('I am good! Thank you for asking')

    elif message.content.startswith('battleship'):
        global game2  # holy fuck python just be normal
        game2 = BattleShipGame()
        await message.channel.send('BattleShip game started!')

    elif message.content.startswith('#'):
        await message.channel.send(game2.makeMove(message.content[1:]))


client.run('ODIzOTIyODMwOTI4Mzc5OTI0.YFn37g.qBiNOnlxbAgc7n4jfu9GQi2dkQk')
