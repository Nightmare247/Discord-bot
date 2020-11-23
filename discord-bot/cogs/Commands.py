import discord
from discord.ext.commands.core import command
import random
from itertools import cycle
from reddit_scraper import *
from discord.ext import commands
import sys
from datetime import date
months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
          '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
Month = months[str(date.today()).split('-')[1]]
Date = str(date.today()).split('-')[-1]

sys.path.append("/home/username/pythonprojects/discord-bot")


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        """
        self.blackmagicposts = make_posts_lists_title_url('blackmagicfuckery')
        self.memes = make_posts_list('Memes')
        self.wholesomeMemes = make_posts_list('wholesomememes')
        self.Showerthoughts = make_posts_list_title('Showerthoughts')
        self.lifeprotips = make_posts_list_title('LifeProTips')
        self.facts = make_posts_list_title('todayilearned')
        self.minecraftmemes = make_posts_list('MinecraftMemes')
        self.news = make_posts_list_title('news')
        self.jokes = make_posts_lists_title_and_body('jokes')
        """
        self.statuses = cycle([
            'League of Legends', 'Rainbow Six: Siege', 'Among Us', 'Minecraft',
            'Valorant', 'Rocket League', 'Overwatch', 'Genshin Impact',
            'Call of Duty: Modern Warfare', 'Hearthstone',
            'Grand Theft Auto V', 'World of Warcraft', 'Fall Guys', 'Dota 2',
            'Phasmophobia', 'Counter-Strike: Global Offensive', 'Porknight'
        ])

    @commands.command(aliases=['tt'])
    async def schedule(self, ctx):
        area = ctx.message.channel
        await area.send(file=discord.File(f'cogs/{Month}{Date}.jpg'))

    @commands.command(
        help="Get the latency between your input and the bot's output")
    async def ping(self, ctx):
        await ctx.send(f"Latency - {self.client.latency}")

    @commands.command(help='Get a greeting')
    async def hello(self, ctx):
        await ctx.send('Hey! Type .help for a list of commands ')

    @commands.command(aliases=['m'], help='(m)Get a Meme')
    async def meme(self, ctx):
        url = give_random_post(self.memes)
        await ctx.send('Meme- (Type .help for a list of commands)')
        await ctx.send(url)

    @commands.command(aliases=['wm'], help='(wm)Get a Wholesome Meme')
    async def wholesomememe(self, ctx):
        url = give_random_post(self.wholesomeMemes)
        await ctx.send('Wholesome Meme(Type .help for a list of commands)')
        await ctx.send(url)

    @commands.command(aliases=['st'], help='(st)Get a perplexing thought')
    async def showerthought(self, ctx):
        title = give_random_post(self.Showerthoughts)
        await ctx.send(title)

    @commands.command(help='(lpt)Get a Life Pro Tip to make your life easier')
    async def lpt(self, ctx):
        title = give_random_post(self.lifeprotips)
        await ctx.send('Life Pro Tip-')
        await ctx.send(title)

    @commands.command(
        aliases=['8ball'],
        help="(8ball)Ask a question and get a random answer. Type '.8ball' and any question after it"
    )
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Don't count on it.",
            "My reply is no.", "My sources say no.", "Outlook not so good.",
            "Very doubtful."
        ]
        await ctx.send(f"{random.choice(responses)}")

    @commands.command(aliases=['f'], help='(f)Get an interesting Fact')
    async def fact(self, ctx):
        title = give_random_post(self.facts)
        title = title[3:]
        if title.split()[0] == 'that':
            title = ' '.join(title.split()[1:])
        await ctx.send('A cool fact-')
        await ctx.send(title)

    @commands.command(aliases=['mm'], help='(mm)Get a Minecraft Meme')
    async def minecraftmeme(self, ctx):
        url = give_random_post(self.minecraftmemes)
        await ctx.send('A Minecraft Meme')
        await ctx.send(url)

    @commands.command(aliases=['j'], help='(j)Get a Joke')
    async def joke(self, ctx):
        jk = give_random_post(self.jokes)
        await ctx.send(jk)

    @commands.command(
        aliases=['bm'],
        help='(bm)Get some confusing phenomena that makes you wonder if reality is broken'
    )
    async def blackmagic(self, ctx):
        post = give_random_post(self.blackmagicposts)
        await ctx.send('Black Magic!')
        await ctx.send(post)

    @commands.command(aliases=['n'], help='(n)Get a news headline')
    async def news(self, ctx):
        title = give_random_post(self.news)
        await ctx.send('News Headline-')
        await ctx.send(title)


def setup(client):
    client.add_cog(Commands(client))
