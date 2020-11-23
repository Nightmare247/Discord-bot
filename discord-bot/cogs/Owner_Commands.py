import colors
from discord.ext import commands
import sys
import os
sys.path.append("/home/username/pythonprojects/discord-bot")


class OwnerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Restart the script', hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        await self.client.get_channel(int(
            ctx.message.channel.id)).send('RESTARTING')
        print(f"{colors.ERROR}RESTARTING{colors.ENDC}")
        os.execv(sys.executable, ['python'] + sys.argv)


def setup(client):
    client.add_cog(OwnerCommands(client))
