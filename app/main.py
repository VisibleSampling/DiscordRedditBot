import os
import discord
import asyncpraw
import praw
import asyncio
from discord.ext import commands
from pathlib import Path
import logging

## Validate required environment variables
required_vars = [
    'DISCORD_TOKEN', 'DISCORD_CHANNEL_ID', 'REDDIT_CLIENT', 
    'REDDIT_SECRET', 'REDDIT_USER_AGENT', 'REDDIT_USERNAME', 
    'REDDIT_PASSWORD', 'REDDIT_SUBREDDIT'
]
for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

## Load exclusions from file if exists
exclusions_file = Path("excluded_keywords.txt")
if exclusions_file.exists():
    exclusions = set()
    with open('excluded_keywords.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                exclusions.add(line)
else:
    exclusions = ()

## Reddit API keys
reddit_read_only = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT'),
                               client_secret=os.getenv('REDDIT_SECRET'),
                               user_agent=os.getenv('REDDIT_USER_AGENT'),
                               username=os.getenv('REDDIT_USERNAME'),
                               password=os.getenv('REDDIT_PASSWORD'),
                               timeout=60,
                               check_for_async=False)

## Discord API connection
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

## Function for sending messages for new posts 
async def monitor_subreddit(subreddit, channel):
     async for submission in subreddit.stream.submissions(skip_existing=True):
        try:
            print(submission.title)
            print(submission.url)
            if any(exclusion.lower() in submission.title.lower() for exclusion in exclusions):
                    continue
            await channel.send(submission.title)
            await channel.send(submission.url)
        except Exception as e:
            logger.error(f"Exception while processing submission {e}")

## Function for monitoring posts
async def monitor_posts():
    await client.wait_until_ready()

    reddit = asyncpraw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT'),
        client_secret=os.getenv('REDDIT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD')
)

    monitored_subreddit = await reddit.subreddit(os.getenv('REDDIT_SUBREDDIT'))
    channel = client.get_channel(int(os.getenv('DISCORD_CHANNEL_ID')))
    await monitor_subreddit(monitored_subreddit, channel)

## Start bot functions
@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')
    logger.info(f"Bot prefix is: '{os.getenv('BOT_PREFIX')}'")
    await monitor_posts()

@client.event
## Discord command recent_posts - returns the latest post from the subreddit
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(f"{os.getenv('BOT_PREFIX')}recent"):
        subreddit = reddit_read_only.subreddit(os.getenv('REDDIT_SUBREDDIT'))
        latest_post = None
        for posts in subreddit.new(limit=1):
            if any(exclusion.lower() in posts.title.lower() for exclusion in exclusions):
                await message.channel.send("Exclusion found")
                await message.delete()
                continue
            latest_post = posts
            break
        if latest_post:
            await message.channel.send(posts.title)
            await message.channel.send(posts.url)
        await message.delete()

    ## Discord command top5 - returns the current top 5 posts
    elif message.content.startswith(f"{os.getenv('BOT_PREFIX')}top5"):
        subreddit = reddit_read_only.subreddit(os.getenv('REDDIT_SUBREDDIT'))
        top_posts = subreddit.hot(limit=5)
        for post in top_posts:
            if any(exclusion.lower() in post.title.lower() for exclusion in exclusions):
                await message.channel.send("Exclusion found")
                await message.delete()
                continue
            await message.channel.send(post.title)
            await message.channel.send(post.url)
        await message.delete()

    ## Discord command help - returns the list of commands
    elif message.content.startswith(f"{os.getenv('BOT_PREFIX')}help"):
        prefix = os.getenv('BOT_PREFIX')
        await message.channel.send(f"Commands: {prefix}recent, {prefix}top5")
        await message.delete()

if __name__ == '__main__':
    client.run(os.getenv('DISCORD_TOKEN'))
