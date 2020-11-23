from colors import colors
from discord.ext import commands
from random import choice
import sys
import discord
from discord.ext import tasks
sys.path.append("/home/username/pythonprojects/discord-bot")
from itertools import cycle
import os
import Schedule_Downloader

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.statuses = cycle([
            'League of Legends', 'Rainbow Six: Siege', 'Among Us', 'Minecraft',
            'Valorant', 'Rocket League', 'Overwatch', 'Genshin Impact',
            'Call of Duty: Modern Warfare', 'Hearthstone',
            'Grand Theft Auto V', 'World of Warcraft', 'Fall Guys', 'Dota 2',
            'Phasmophobia', 'Counter-Strike: Global Offensive', 'Porknight'
        ])

    # Say something when bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.online, activity=discord.Game('Minecraft'))
        self.change_status.start()
        print(f"{colors.OKGREEN}I'm ready!{colors.ENDC}")

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(
            activity=discord.Game(next(self.statuses)))

    # Say something when a user joins

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ment = member.mention
        await self.client.get_channel(778271010075705377).send(
            f"{ment} has joined us! Hey!.")
        print(f"{colors.OKGREEN}{member} has joined the server{colors.ENDC}")

    # Say something when a user leaves
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ment = member.mention
        await self.client.get_channel(778271010075705377).send(
            f"{ment} has left! We're sad to see you go")
        print(f"{colors.ERROR}{member} has left the server{colors.ENDC}")

    # Say bye when any user says bye
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or str(message.channel) == 'announcements':
            return
        if 'bye' in str(message.content).lower() or '👋' in str(
                message.content).lower():
            byes = [
                'Catch you later ', 'Bye ', 'See you later ', 'Godspeed, ',
                'Bye bye ', 'Ciao ', 'So long, ', 'Farewell, ', 'Bon voyage, '
            ]
            ment = message.author.mention
            channel = self.client.get_channel(message.channel.id)
            await channel.send(f"{choice(byes)}{ment}!")


def setup(client):
    client.add_cog(Events(client))
