import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\.env")
DISCORD_ADMIN_IDS = os.getenv("DISCORD_ADMIN_IDS")

def requires_admin():
    """Decorator to check if the user ID is in DISCORD_ADMIN_IDS."""
    def predicate(ctx):
        is_admin = False
        if DISCORD_ADMIN_IDS:
            admin_ids = []
            if isinstance(DISCORD_ADMIN_IDS, str):
                cleaned = DISCORD_ADMIN_IDS.strip("[]")
                admin_ids = []
                for uid in cleaned.split(","):
                    uid = uid.strip()
                    if uid.isdigit():
                        admin_ids.append(int(uid))
            elif isinstance(DISCORD_ADMIN_IDS, list):
                admin_ids = []
                for uid in DISCORD_ADMIN_IDS: # type: ignore
                    if isinstance(uid, int):
                        admin_ids.append(uid)
            is_admin = ctx.author.id in admin_ids
        return is_admin
    return commands.check(predicate)
