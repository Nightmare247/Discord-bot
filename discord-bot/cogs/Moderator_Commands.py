from discord.ext import commands


class ModeratorCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Clear the last x messages", hidden=True)
    @commands.has_any_role('Jr Mod', 'Admin', 'Owners')
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(ModeratorCommands(client))
