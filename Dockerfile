FROM python:3.11-slim

# Docker Specific ARG
ARG BOT_PREFIX="!"
ARG DISCORD_CHANNEL_ID=${DISCORD_CHANNEL_ID}

# Reddit Specific ARG
ARG REDDIT_CLIENT=${REDDIT_CLIENT}
ARG REDDIT_SECRET=${REDDIT_SECRET}
ARG REDDIT_USER_AGENT=${REDDIT_USER_AGENT}
ARG REDDIT_USERNAME=${REDDIT_USERNAME}
ARG REDDIT_PASSWORD=${REDDIT_PASSWORD}
ARG REDDIT_SUBREDDIT=${REDDIT_SUBREDDIT}

# Optional ARG
ARG DEBUG_MODE="false"
ARG LOG_LEVEL="INFO"

# Discord Specific ENV
ENV DISCORD_CHANNEL_ID=${DISCORD_CHANNEL_ID}
ENV BOT_PREFIX=${BOT_PREFIX}

# Reddit Specific 
ENV REDDIT_CLIENT=${REDDIT_CLIENT}
ENV REDDIT_SECRET=${REDDIT_SECRET}
ENV REDDIT_USER_AGENT=${REDDIT_USER_AGENT}
ENV REDDIT_USERNAME=${REDDIT_USERNAME}
ENV REDDIT_PASSWORD=${REDDIT_PASSWORD}
ENV REDDIT_SUBREDDIT=${REDDIT_SUBREDDIT}

# Optional ENV
ENV DEBUG_MODE=${DEBUG_MODE}
ENV LOG_LEVEL=${LOG_LEVEL}

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' appuser

RUN pip install --upgrade pip

WORKDIR /app

# Copy the app directory
COPY app/ .

# Install base requirements during build
RUN pip install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod +x entrypoint.sh

USER appuser

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
