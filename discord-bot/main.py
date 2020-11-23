import sys
sys.path.append("/home/username/pythonprojects/discord-bot/cogs")
from colors import colors
import os
import discord
from discord.ext import commands
#from keep_alive import keep_alive

intents = discord.Intents(
    messages=True, guilds=True, reactions=True, members=True, presences=True)

client = commands.Bot(command_prefix='.', intents=intents)


@client.command(hidden=True)
@commands.has_role('Owners')
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command(hidden=True)
@commands.has_role('Owners')
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for c in os.listdir("./cogs"):
    if c.endswith('.py') and 'Schedule' not in c and 'colors' not in c:
        client.load_extension(f"cogs.{c[:-3]}")
        print(f"{colors.OKGREEN}loaded {c}{colors.ENDC}")


for guild in client.guilds:
    for channel in guild.text_channels:
        print(channel)

# keep_alive()
token = 'YOUR-TOKEN'
client.run(token)
