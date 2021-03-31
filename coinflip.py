import discord
import os
import random

client = discord.Client(command_prefix="-")

coin = random.randint(0, 1)
if coin == 0:
    print( 'Heads' )
else:
    print( 'Tails' )

@client.command()
async def coinflip(ctx):
    result = ["HEADS", "TAILS"]
    randomFlip = random.choice(result)
    await ctx.channel.send(randomFlip)

client.run('ODIzOTIyODMwOTI4Mzc5OTI0.YFn37g.qBiNOnlxbAgc7n4jfu9GQi2dkQk')