# Anonymous Message Bot

A Telegram bot that allows users to send and receive anonymous messages with unique links.

## Features

- **Anonymous messaging** with unique user links
- **Reply functionality** for full conversations  
- **Admin-only username visibility** for specified user IDs
- **Group logging** to evidence channel with sender details
- **All media types** supported (text, photos, videos, voice, stickers, documents)
- **Supabase database** integration for user management

## Deployment to Railway

This bot is configured for deployment on Railway.com with the following files:
- `railway.json` - Railway configuration
- `Dockerfile` - Container configuration
- `.railwayignore` - Files to ignore during deployment

## Environment Variables

Set these in Railway dashboard:
- `BOT_TOKEN` - Your Telegram bot token
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `ADMIN_USER_IDS` - Comma-separated admin user IDs
- `LOG_GROUP_ID` - Telegram group ID for logging messages

## Requirements

- Python 3.11+
- aiogram 3.x
- Supabase

#### Installation
```bash
git clone https://github.com/Fsoky/anonimchatbot-aiogram3.git
```
#### Change directory
```bash
cd anonimchatbot-aiogram3
```
#### Use [poetry](https://python-poetry.org/docs/) for install dependencies (`pip install poetry`)
```bash
poetry install
```
#### Run
```bash
python src/__main__.py
```

> [!TIP]
> Make sure you modify the .env file before running this script!


#### Installation in Docker
```bash
docker compose up
```
**This will output the logs of your docker containers:**
1) anonchat-telegram
2) mongo
3) mongo-express

**To access admin panel of your database go to `localhost:8081` in your browser and enter your credentials in the prompt**

#### Set containers to run as daemons

After checking that everything works as expected, you can set those containers to run as daemons by stopping previous docker command with ctrl + c and running it again with:
```bash
docker compose up -d
```