from discord.ext import tasks, commands
import discord


class Loops(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(
            activity=discord.Game(next(self.statuses)))

def setup(client):
    client.add_cog(Loops(client))