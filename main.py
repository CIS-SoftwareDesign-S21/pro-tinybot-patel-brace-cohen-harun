from typing import Any
import discord
import os
from tic_tac_toe import TicTacToeGame
from coinflip import coinflip
from microchess import MicrochessGame

game: TicTacToeGame = TicTacToeGame()
chessGame: MicrochessGame = None
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


client.run('ODIzOTIyODMwOTI4Mzc5OTI0.YFn37g.qBiNOnlxbAgc7n4jfu9GQi2dkQk')
