import praw
import random
import discord
import json
import urllib.request
from discord.ext import commands, tasks
from random import randint
from itertools import cycle
from time import sleep
import sys
sys.path.append("/home/agastya/pythonprojects/discord-bot")
from colors import colors


class AllCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.blackmagicposts = make_posts_lists_title_url('blackmagicfuckery')
        self.memes = make_posts_list('Memes')
        self.wholesomeMemes = make_posts_list('wholesomememes')
        self.Showerthoughts = make_posts_list_title('Showerthoughts')
        self.lifeprotips = make_posts_list_title('LifeProTips')
        self.facts = make_posts_list_title('todayilearned')
        self.minecraftmemes = make_posts_list('MinecraftMemes')
        self.news = make_posts_list_title('news')
        self.jokes = make_posts_lists_title_and_body('jokes')
        self.allowed_channels = ['bot-chat', 'bot-testing-only-agastya']
        self.statuses = cycle([
            'League of Legends', 'Rainbow Six: Siege', 'Among Us', 'Minecraft',
            'Valorant', 'Rocket League', 'Overwatch', 'Genshin Impact',
            'Call of Duty: Modern Warfare', 'Hearthstone',
            'Grand Theft Auto V', 'World of Warcraft', 'Fall Guys', 'Dota 2',
            'Phasmophobia', 'Counter-Strike: Global Offensive', 'Porknight'
        ])

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.online, activity=discord.Game('Minecraft'))
        self.change_status.start()
        print(f"{colors.OKGREEN}I'm ready!{colors.ENDC}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ment = member.mention
        await self.client.get_channel(778271010075705377).send(
            f"{ment} has joined us! Hey!.")
        print(f"{member} has joined the server.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ment = member.mention
        await self.client.get_channel(778271010075705377).send(
            f"{ment} has left! We're sad to see you go")
        print(f"{member} has left the server.")

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
            await channel.send(f"{random.choice(byes)}{ment}!")

    # Loops
    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(
            activity=discord.Game(next(self.statuses)))

    # Hidden Commands
    @commands.command(help='Restart the script', hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        import sys
        import os
        await self.client.get_channel(int(
            ctx.message.channel.id)).send('RESTARTING')
        print(f"{colors.WARNING}RESTARTING{colors.ENDC}")
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(help="Clear the last x messages", hidden=True)
    @commands.has_any_role('Jr Mod', 'Admin', 'Owners')
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount)

    # Commands
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
    client.add_cog(AllCommands(client))


reddit = praw.Reddit(
    client_id='o2ujvP-mm0yGyg',
    client_secret='SwGV0xraPmQxDU-Bmyq3Qbf2umZM1Q',
    user_agent='idk')

reddit.read_only = True


def make_posts_list(subred, length=200, tm='day'):
    print(f"Making posts list for {subred}...")
    post_list = []
    subr = reddit.subreddit(subred)
    top = subr.top(time_filter=tm, limit=length)
    for post in top:
        if post.over_18:
            continue
        post_list.append(post.url)

    return post_list


def make_posts_list_title(subred, length=200):
    print(f"Making posts with titles for {subred}...")
    post_list = []
    subr = reddit.subreddit(subred)
    top = subr.top(time_filter='day', limit=length)
    for post in top:
        if post.over_18:
            continue
        post_list.append(post.title)

    return post_list


def make_posts_lists_title_and_body(subred, length=200):
    print(f"Making posts with titles and body for {subred}...")
    post_list = []
    subr = reddit.subreddit(subred)
    top = subr.top(time_filter='day', limit=length)
    for post in top:
        if post.over_18:
            continue
        post_list.append(f"{post.title}\n\n{post.selftext}")
    return post_list


def make_posts_lists_title_url(subred, length=200):
    print(f"Making posts with titles and url for {subred}...")
    posts_list = []
    subr = reddit.subreddit(subred)
    top = subr.top(time_filter='day', limit=length)
    for p in top:
        if p.over_18:
            continue
        sleep(0.2)
        url = f"https://www.reddit.com{p.permalink}.json"
        print(url)
        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())[0]
            link = data['data']['children'][0]['data']['secure_media'][
                'reddit_video']['fallback_url'].replace('1080', '720')
            posts_list.append(f"{p.title}\n{link}")
        except Exception as e:
            print(e)
        print(
            f"{colors.OKGREEN}Length of {subred} posts: {len(posts_list)}{colors.ENDC}"
        )
        posts_list = list(dict.fromkeys(posts_list))
        return posts_list


"""
    if len(posts_list) < 10:
        print(
            f"Didn't get enough posts for {subred}, getting top posts from this week..."
        )
        top = subr.top(time_filter='week', limit=length)
        for p in top:
            if p.over_18:
                continue
            sleep(0.5)
            url = f"https://www.reddit.com{p.permalink}.json"
            try:
                response = urllib.request.urlopen(url)
                data = json.loads(response.read())[0]
                link = data['data']['children'][0]['data']['secure_media'][
                    'reddit_video']['fallback_url'].replace('1080', '720')
                # print(link)
                posts_list.append(f"{p.title}\n{link}")
            except:
                pass
"""


def give_random_post(post_list):
    while True:
        try:
            if len(post_list) != 0:
                randin = randint(0, len(post_list)+1)
                x = post_list[randin]
                del post_list[randin]
                return x
            else:
                return "Sorry I've run out of content. Maybe try a bit later?"

        except IndexError:
            pass
