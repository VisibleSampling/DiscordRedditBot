# Reddit to Discord Bot

A Discord bot that monitors a subreddit and posts new submissions to a specified Discord channel. Also responds to commands for recent and top posts.

## Features
- Monitors subreddit for new posts in real-time
- Exclusion list for filtering unwanted content
- Commands:
  - recent - Shows latest subreddit post
  - top5 - Shows top 5 hot posts
  - help - Lists available commands

## Setup
1. Clone the repository
2. Create a docker-compose.yml:
```
services:
  discord_bot:
    build: .
    volumes:
      - ./exclusionlist.txt:/app/excluded_keywords.txt
    environment:
      - DISCORD_TOKEN=your_token
      - DISCORD_CHANNEL_ID=your_channel
      - BOT_PREFIX=!
      - REDDIT_CLIENT=your_client_id
      - REDDIT_SECRET=your_secret
      - REDDIT_USER_AGENT=your_user_agent
      - REDDIT_USERNAME=your_username
      - REDDIT_PASSWORD=your_password
      - REDDIT_SUBREDDIT=subreddit_name
    restart: unless-stopped
```
3. (Optional) Create exclusionlist.txt with keywords to filter, one per line

## Running
`docker compose up -d`

## Requirements
- Docker
- Discord Bot Token
- Reddit API Credentials
