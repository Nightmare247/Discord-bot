import praw
from random import randint
from time import sleep
import urllib
import json
from colors import colors

reddit = praw.Reddit(
    client_id='YOUR-ID',
    client_secret='YOUR-SECRET',
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
