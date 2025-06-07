import os
import discord
from dotenv import load_dotenv
from utils.query_ollama import query_ollama
from utils.helpers import text_to_speech, play_audio_in_voice
from discord.ext import commands
from typing import Optional
import asyncio
import re
import logging

load_dotenv(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_ADMIN_IDS = os.getenv("DISCORD_ADMIN_IDS")
EMERGENCY_CODE = os.getenv("EMERGENCY_CODE")

intents = discord.Intents.default()
intents.members = True

GUILD_IDS = [1379620830077517824]

bot = commands.Bot(command_prefix="/", intents=intents, guild_ids=GUILD_IDS)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@bot.event
async def on_ready():
    logging.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})") # type: ignore

    # Notify approved users that the bot is back online
    if DISCORD_ADMIN_IDS:
        user_ids = []
        if isinstance(DISCORD_ADMIN_IDS, str):
            cleaned = DISCORD_ADMIN_IDS.strip("[]")
            user_ids = [uid.strip() for uid in cleaned.split(",")]
        elif isinstance(DISCORD_ADMIN_IDS, list):
            user_ids = DISCORD_ADMIN_IDS
        for user_id_str in user_ids:
            try:
                user_id = int(user_id_str)
                user = await bot.fetch_user(user_id)
                if user is not None and hasattr(user, "id"):
                    try:
                        await user.send(
                            f"🟢 Bot restarted and is now online.\n"
                            f"📶 Latency: `{round(bot.latency * 1000)}ms`\n"
                        )
                    except discord.Forbidden:
                        logging.warning(f"Could not DM user {user_id}")
            except Exception as e:
                logging.error(f"Error fetching user {user_id_str}: {e}")

@bot.event
async def on_command(ctx):
    logging.info(f"Command invoked: {ctx.command} by {ctx.author} in {ctx.guild}")

# Load cogs
bot.load_extension("cogs.creative")
bot.load_extension("cogs.modding")
bot.load_extension("cogs.developer")
bot.load_extension("cogs.community")
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.ai_integration")
bot.load_extension("cogs.github_stats")
bot.load_extension("cogs.info")
bot.load_extension("cogs.afk_manager")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not set in env variables")
bot.run(DISCORD_TOKEN)
