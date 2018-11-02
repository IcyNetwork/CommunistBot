#py -u "bot.py"
import discord
import youtube_dl
from discord.ext import commands
import asyncio

TOKEN = 'NDQ4NDI1MjIzNDQwNTY0MjM0.Dr13NQ.lMEEfivaQQX3NDD2ePYR4nTa-pc'

client = commands.Bot(command_prefix = "c!" or "C!")
client.remove_command('help')

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = play
        player.start()

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="c!help"))
    print("Bot is ready!")


@client.command(pass_context=True)
async def help(ctx):
    
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    
    embed.set_author(name="Help")
    embed.add_field(name="Ping", value="Returns Pong!", inline=False)
    embed.add_field(name="clear", value="Deletes messages based on amount!", inline=False)

    await client.send_message(author, embed=embed)


@client.command()
async def ping():
    await client.say("Pong!")

@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say("Deleted messages!")

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    
@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    
@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    
@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say("Your song has been added to the queue.")

    

client.run(TOKEN)