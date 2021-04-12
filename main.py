import discord
import os
from coinflip import coinflip

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


client.run('ODIzOTIyODMwOTI4Mzc5OTI0.YFn37g.qBiNOnlxbAgc7n4jfu9GQi2dkQk')
